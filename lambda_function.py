import json
import boto3
import os
import zipfile
import tempfile
from botocore.config import Config
import parso

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


def extract_code_with_parso(input_file_path):
    with open(input_file_path, 'r', encoding='utf-8', errors='ignore') as file:
        content = file.read()
    print(content)
    # Parse the translated content using parso
    tree = parso.parse(content)

    # Collect all translated Python code nodes
    valid_code = []
    for node in tree.children:
        if node.type in ('funcdef', 'classdef', 'simple_stmt'):
            valid_code.append(node.get_code())

    print(valid_code)
    # Write the valid Python code to the output file
    with open(input_file_path, 'w', encoding='utf-8', errors='ignore') as file:
        file.writelines(valid_code[1:])
    print("WROTE FILE SUCESSFULLY")

def lambda_handler(event, context):
    # Get the uploaded file's details from the event
    source_bucket = event['Records'][0]['s3']['bucket']['name']
    source_key = event['Records'][0]['s3']['object']['key']
    
    # Define the output bucket
    output_bucket = 'amzn-s3-cuiyc-output-bucket'
    
    try:
        # Download the zip file from the source bucket
        download_path = os.path.join('/tmp', os.path.basename(source_key))
        s3.download_file(source_bucket, source_key, download_path)

        # Extract the zip file
        extract_path = tempfile.mkdtemp()
        with zipfile.ZipFile(download_path, 'r') as zip_ref:
            zip_ref.extractall(extract_path)

        # Traverse the extracted files, translate or pass through, and upload results
        for root, dirs, files in os.walk(extract_path):
            for file_name in files:
                # Check the file extension
                file_extension = os.path.splitext(file_name)[1].lower()
                file_path = os.path.join(root, file_name)

                # Define the output file name and path
                relative_path = os.path.relpath(file_path, extract_path)
                dir_name = os.path.dirname(relative_path)
                processed_file_name = f"translated-{os.path.basename(file_name)}.py"
                documentation_name = f"documentation-{os.path.basename(file_name)}.txt"
                docs_relative_path = os.path.join(dir_name, documentation_name) if dir_name else documentation_name
                processed_relative_path = os.path.join(dir_name, processed_file_name) if dir_name else processed_file_name
                docs_output_key = f"processed/{docs_relative_path}"
                output_key = f"processed/{processed_relative_path}"

                if file_extension in ['.pkb', '.pks']:
                    # Read the content and translate
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as file:
                        original_code = file.read()
                    #TODO: remove comments; split code by functions
                    translated_code = translate_code_with_bedrock(original_code)
                    #this block: writing the translated code
                    # Save the translated code to a temporary file
                    translated_file_path = os.path.join('/tmp', processed_file_name)
                    with open(translated_file_path, 'w', encoding='utf-8', errors='ignore') as translated_file:
                        translated_file.write(translated_code)
                    
                    #Calls the helper method for removing the generated comments and non-python code in the translated python file
                    extract_code_with_parso(translated_file_path)

                    #This block: docs creation
                    with open(translated_file_path, 'r', encoding='utf-8', errors='ignore') as file_new:
                        new_code_clean = file_new.read()
                    
                    docs = write_docs_with_bedrock(new_code_clean)
                    docs_file_path = os.path.join('/tmp', documentation_name)
                    with open(docs_file_path, 'w', encoding='utf-8', errors='ignore') as docs_file:
                        docs_file.write(docs)



                    print("REACHED STATEMENT")
                    # Upload the translated file
                    s3.upload_file(translated_file_path, output_bucket, output_key)
                    s3.upload_file(docs_file_path, output_bucket, docs_output_key)

                else:
                    # Pass through non-source files without changes
                    s3.upload_file(file_path, output_bucket, output_key)
        #TODO: Ask llm for unit tests 
       
        return {
            'statusCode': 200,
            'body': json.dumps(f"Files processed and uploaded to {output_bucket}/processed/")
        }
    
    except Exception as e:
        print(f"Error processing zip file: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps("Error processing zip file.")
        }