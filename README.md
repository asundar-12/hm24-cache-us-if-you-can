# hm24-cache-us-if-you-can

Authors: 
Arjun Sundaram,
Aditya Krishnamoorthy,
Venkat Praneeth Uppari,
Amber Oliver,
Sahil Sinha,
Gavin Bassett

# PL/SQL → Python Translator (AWS Lambda + Bedrock)
**For Legacy PL/SQL Chess Engine Code**

This project processes **Oracle PL/SQL package files** (`.pkb`, `.pks`)—specifically from a **legacy chess engine system**—and translates them into modern Python. It also generates documentation for the translated code.

The legacy PL/SQL source comes from the open-source **PL/SQL Chess Engine** written in PL/SQL for Oracle Database (see: [PL-SQL-Chess Releases on GitHub](https://github.com/EgonMadsen/PL-SQL-Chess/releases)). That engine includes core game logic, evaluation functions, and data implemented purely as Oracle PL/SQL packages and has been released historically with multiple `.pkb` and `.pks` files representing chess-engine components such as evaluation, engine logic, and book data. :contentReference[oaicite:1]{index=1}

---

## What this project does

- Takes a **ZIP upload** containing legacy `.pkb` / `.pks` PL/SQL source files (from the chess engine).
- Splits large PL/SQL bodies into chunks (to fit model contexts).
- Uses **Amazon Bedrock** LLMs to:  
  - Translate PL/SQL logic to **Python**.
  - Create **English documentation** describing logic and structure.
- Outputs results to an S3 output bucket:
  - `processed/concatenated_translated.py`
  - `processed/concatenated_documentation.txt`
- Any other files in the ZIP are passed through unmodified.

---

## Architecture

1. **Upload ZIP**  
   Users upload a ZIP file of legacy PL/SQL source (e.g., from the chess engine) to an S3 input bucket.

2. **S3 Trigger (Lambda)**  
   AWS Lambda is triggered on new object creation.

3. **Processing**
   - Extract ZIP
   - Identify `.pkb` and `.pks` files
   - Split large PL/SQL bodies
   - Feed into Bedrock translation + documentation models
   - Collect results, clean with `parso`
   - Upload final artifacts to output bucket

---

## Repository Structure

- **`lambda_function.py`** – Main AWS Lambda handler with S3 and Bedrock logic.
- **`split_file.py`** – Splits .pkb bodies into manageable chunks.
- **`index.html` / `styles.css`** – A minimal static upload UI to upload files to S3.
- **`upload.py`** – Local Streamlit uploader (optional).
- **Example outputs**:
  - `concatenated_translated.py`
  - `concatenated_documentation.txt`

---

## How the Lambda Works

### Input Handling
- Expects a ZIP upload containing `.pkb` and `.pks` PL/SQL files (e.g., from the legacy chess engine code).
- Extracts ZIP into `/tmp`.

### Translation & Documentation
- For each PL/SQL part:
  - Calls Amazon Bedrock to **translate logic to Python**.
  - Calls Amazon Bedrock to **generate documentation** in English.
  - Cleans Python output with `parso` before concatenation.

### Output
- Uploads:
  - `processed/concatenated_translated.py`
  - `processed/concatenated_documentation.txt`
- Non-PL/SQL files are uploaded under `processed/` unchanged.

---

## S3 Buckets

- **Input bucket** – the trigger source
- **Output bucket** – hardcoded (changeable):
  - Default: `amzn-s3-cuiyc-output-bucket`
- Output paths:
  - `processed/concatenated_translated.py`
  - `processed/concatenated_documentation.txt`

---

## AWS Setup Essentials

- **S3 Buckets** – create input/output buckets.
- **Lambda Trigger** – S3 `ObjectCreated:*` event (ZIP suffix filter).
- **IAM Role for Lambda** – with permissions:
  - `s3:GetObject`
  - `s3:PutObject`
  - `bedrock:InvokeModel`
  - CloudWatch Logs.

---

## Dependencies

Ensure your Lambda package includes:

- `boto3` / `botocore`
- `parso` (for Python AST cleaning)

---

## Usage Notes

- Customize prompt design for higher quality code translation.
- Consider secure upload UI with pre-signed URLs (instead of unauthenticated PUT).
- Tune `split_file.py` thresholds for your PL/SQL size characteristics.

---

## Limitations & Future Improvements

- Current documentation generated from original PL/SQL; you may instead generate docs from translated Python.
- Improve error reporting to S3.
- Support configuration of Bedrock models via environment variables.

---

## Example

Given a ZIP containing PL/SQL files from the legacy chess engine (e.g., `pl_pig_chs_engine.pkb`, `pl_pig_chs_interface.pks`, etc.), this Lambda will produce:

```bash
printed: processed/concatenated_translated.py
printed: processed/concatenated_documentation.txt
