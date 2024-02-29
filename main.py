import tempfile

import boto3
import httpx
import uvicorn
from dotenv import load_dotenv
from fastapi import FastAPI, UploadFile, File
from openai import OpenAI
from requests.auth import HTTPProxyAuth
from ultralytics import YOLO

from json_schemas import Resume
from parsing import *
from prompts import ENGLISH_PROMPT, RUSSIAN_PROMPT

load_dotenv()

API_KEY = os.getenv('API_KEY')
GPT_MODEL = os.getenv('GPT_MODEL')

# create client with proxy
proxy_url = os.environ.get('OPENAI_PROXY_URL')
proxy_log = os.environ.get('PROXY_LOGIN')
proxy_pass = os.environ.get('PROXY_PASS')
proxy_auth = HTTPProxyAuth(proxy_log, proxy_pass)
client = OpenAI(api_key=API_KEY) if proxy_url is None or proxy_url == "" else OpenAI(api_key=API_KEY,
                                                                                     http_client=httpx.Client(
                                                                                         proxy=proxy_url))

MODEL = YOLO('yolov8s.pt')
EXTRACTED_IMG_FOLDER = os.getenv('EXTRACTED_IMG_FOLDER')

BUCKET_HOST = os.getenv('BUCKET_HOST')
BUCKET_KEY_ID = os.getenv('BUCKET_KEY_ID')
BUCKET_KEY = os.getenv('BUCKET_KEY')
BUCKET_SERVICE = os.getenv('BUCKET_SERVICE')
BUCKET_NAME = os.getenv('BUCKET_NAME')

S3 = boto3.session.Session().client(
    service_name=BUCKET_SERVICE,
    endpoint_url=BUCKET_HOST,
    aws_access_key_id=BUCKET_KEY_ID,
    aws_secret_access_key=BUCKET_KEY
)

app = FastAPI()


def get_filename_extension(filename: str) -> str:
    """
    Extracts the file extension from a filename.

    Parameters:
        filename (str): The name of the file.

    Returns:
        str: The file extension.
    """
    return filename.split('.')[-1]


@app.post("/extract_text", response_model=ParserOutput)
async def extract_text(file: UploadFile = File(...)):
    """
   Extracts text from an uploaded file.

   Parameters:
       file (UploadFile): The uploaded file containing the document.

   Returns:
       ParserOutput: The parsed output containing extracted text and metadata.
    """
    global MODEL

    # Get file extension
    file_extension = get_filename_extension(file.filename)

    # Create a temporary file and save the uploaded file to it
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    shutil.copyfileobj(file.file, temp_file)
    file_path = temp_file.name

    # Parse the file
    data = parse(file_path, file_extension)

    # Close and remove the temporary file
    temp_file.close()

    return data


@app.post("/parse_text", response_model=Resume)
async def parse_text_with_llm(text: str, prompt_language: str):
    """
    Parses text using a language model and returns a Resume object containing the extracted information.

    Parameters:
        text (str): The text of resume to be parsed.
        prompt_language (str): The language of the text prompt ('ru' for Russian, 'en' for English).

    Returns:
        Resume: The parsed resume object.
    """
    if prompt_language == 'ru':
        d = {"messages": [{"role": "system", "content": f"{RUSSIAN_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}
    else:
        d = {"messages": [{"role": "system", "content": f"{ENGLISH_PROMPT}"},
                          {"role": "user", "content": f"{text}"}]}

    response = client.chat.completions.create(
        model=GPT_MODEL,
        messages=d['messages']
    )

    content = response.choices[0].message.content

    return eval(content)


@app.post("/parse_file", response_model=Resume)
async def parse_file(file: UploadFile = File(...)):
    """
    Parses a file uploaded via the API and returns a Resume object containing the extracted information.

    Parameters:
        file (UploadFile): The uploaded file containing the document.

    Returns:
        Resume: The parsed resume object.
    """
    data = await extract_text(file)
    result = await parse_text_with_llm(data.text, data.language)

    result['resume']['photo_path'] = data.photo_path

    return result


# @app.get("/download_file")
# async def download_file(local_file_path: str):
#     """
#     Returns a locally stored file to the user via API.
#     The file_path can be taken from JSON returned by the parse_file or parse_text method.
#     """
#     return FileResponse(local_file_path, media_type='application/octet-stream', filename='file.jpg')


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
