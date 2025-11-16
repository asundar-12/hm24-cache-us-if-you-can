import json
import boto3
import os
import zipfile
import tempfile
from botocore.config import Config
import parso
from split_file import split_file

# Initialize AWS services
s3 = boto3.client('s3')


config = Config(read_timeout=1000)
bedrock_client = boto3.client('bedrock', region_name='us-east-1')  # Update to your AWS region
  # Bedrock Runtime client used to invoke and question the models
bedrock_runtime = boto3.client(
     service_name='bedrock-runtime', 
     region_name='us-east-1',
     config=config
    )
print("bedrock client variable set")
def translate_code_with_bedrock(input_text):
    """Uses AWS Bedrock's Titan Text Lite model to translate the given source code to Python."""
    model_id = "amazon.titan-text-premier-v1:0"
    body = json.dumps({
        "inputText":  f"Be a PL/SQL expert. convert the logic in this PL/SQL code into simple Python, and only reply with the python code. you may not use prose in your response.: \n{input_text}\n",
        "textGenerationConfig":{
            "maxTokenCount":3072,
            "stopSequences":[],
            "temperature":0.7,
            "topP":0.9
            }
    })

    try:
        print("beofre invoking")
        response = bedrock_runtime.invoke_model(
             modelId=model_id,
             body=body,
             contentType='application/json'
         )
        print("after invoking")
        print(response)
        result = json.loads(response['body'].read())
        print(result)
        res = result.get('results', 'Failed')[0].get('outputText')
        return res
    except Exception as e:
        print(f"Error invoking Bedrock: {e}")
        return "Translation failed."

def write_docs_with_bedrock(input_text):
    """Uses AWS Bedrock's Titan Text Lite model to translate the given source code to Python."""
    model_id = "amazon.titan-text-premier-v1:0"
    body = json.dumps({
        "inputText":  f"Please write thorough documentation about the functionality of this code and how to utilize it. Please do not include examples, just English explanations.\n{input_text}\n",
        "textGenerationConfig":{
            "maxTokenCount":3072,
            "stopSequences":[],
            "temperature":0.7,
            "topP":0.9
            }
    })

    try:
        print("beofre invoking docs")
        response = bedrock_runtime.invoke_model(
             modelId=model_id,
             body=body,
             contentType='application/json'
         )
        print("after invoking")
        print(response)
        result = json.loads(response['body'].read())
        print(result)
        res = result.get('results', 'Failed')[0].get('outputText')
        return res
    except Exception as e:
        print(f"Error invoking Bedrock: {e}")
        return "Translation failed."


def extract_code_with_parso(content):
    # with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
    #     content = file.read()
    # print(content)
    # Parse the translated content using parso
    tree = parso.parse(content)

    # Collect all translated Python code nodes
    valid_code = []
    for node in tree.children:
        if node.type in ('funcdef', 'classdef', 'simple_stmt'):
            valid_code.append(node.get_code())

    print(valid_code)
    # Write the valid Python code to the output file
    # with open(input_file_path, 'w', encoding='utf-8', errors='ignore') as file:
    #     file.writelines(valid_code[1:])
    print("WROTE FILE SUCESSFULLY")
    return "".join(valid_code)

def lambda_handler(event, context):
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    output_bucket = 'amzn-s3-cuiyc-output-bucket'

    try:
        # Download the ZIP file
        download_path = os.path.join('/tmp', os.path.basename(source_key))
        s3.download_file(source_bucket, source_key, download_path)

        # Extract the ZIP file
        extract_path = tempfile.mkdtemp()
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Initialize containers for concatenated content
        concatenated_translated_code = ""
        concatenated_documentation = ""

        # Process each extracted file
        for root, dirs, files in os.walk(extract_path):
            for file_name in files:
                file_extension = os.path.splitext(file_name)[1].lower()
                file_path = os.path.join(root, file_name)

                # Only process PL/SQL files
                if file_extension in ['.pkb','.pks']:
                    # Step 1: Split the file into smaller parts
                    if file_extension in ['.pkb']:
                        split_files = split_file(file_path)
                    else: 
                        split_files = [file_path]

                    # Step 2: Translate each part and generate documentation
                    for split_file_path in split_files:
                        with open(split_file_path, 'r', encoding='iso-8859-1', errors='ignore') as file:
                            original_code = file.read()

                        translated_code = translate_code_with_bedrock(original_code)

                        # Append translated code to the concatenated content
                        concatenated_translated_code += extract_code_with_parso(translated_code) + "\n"

                        # Clean the translated Python code for documentation
                        # extract_code_with_parso(split_file_path)  # Assuming this step modifies the file directly

                        with open(split_file_path, 'r', encoding='iso-8859-1', errors='ignore') as file_new:
                            clean_code = file_new.read()

                        documentation = write_docs_with_bedrock(clean_code)

                        # Append documentation to the concatenated content
                        concatenated_documentation += f"\n# Documentation for {os.path.basename(split_file_path)}\n"
                        concatenated_documentation += documentation + "\n"

                else:
                    # Pass through non-PL/SQL files
                    pass_through_key = f"processed/{os.path.basename(file_name)}"
                    s3.upload_file(file_path, output_bucket, pass_through_key)

        # Save the concatenated translated code and documentation as single files
        concatenated_translated_path = "/tmp/concatenated_translated.py"
        concatenated_documentation_path = "/tmp/concatenated_documentation.txt"

        with open(concatenated_translated_path, 'w', encoding='iso-8859-1', errors='ignore') as translated_file:
            translated_file.write(concatenated_translated_code)

        with open(concatenated_documentation_path, 'w', encoding='iso-8859-1', errors='ignore') as docs_file:
            docs_file.write(concatenated_documentation)

        # Upload the concatenated files to S3
        translated_key = "processed/concatenated_translated.py"
        documentation_key = "processed/concatenated_documentation.txt"
        s3.upload_file(concatenated_translated_path, output_bucket, translated_key)
        s3.upload_file(concatenated_documentation_path, output_bucket, documentation_key)

        return {
            'statusCode': 200,
            'body': json.dumps(f"Files processed and uploaded to {output_bucket}/processed/")
        }

    except Exception as e:
        print(f"Error processing file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps("Error processing file.")
        }