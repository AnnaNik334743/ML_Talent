import os
import boto3
from ultralytics import YOLO
from openai import OpenAI
from dotenv import load_dotenv


load_dotenv()


OPENAI_API_KEY = os.getenv('OPEN_API_KEY')
OPENAI_MODEL_NAME = os.getenv('OPENAI_MODEL_NAME')
OPENAI_CLIENT = OpenAI(api_key=OPENAI_API_KEY)


YOLO_MODEL_NAME = os.getenv('YOLO_MODEL_NAME')
YOLO_MODEL = YOLO(YOLO_MODEL_NAME)


BUCKET_HOST = os.getenv('BUCKET_HOST')
BUCKET_KEY_ID = os.getenv('BUCKET_KEY_ID')
BUCKET_KEY = os.getenv('BUCKET_KEY')
BUCKET_SERVICE = os.getenv('BUCKET_SERVICE')
BUCKET_NAME = os.getenv('BUCKET_NAME')
EXTRACTED_IMG_FOLDER = os.getenv('EXTRACTED_IMG_FOLDER')
S3 = boto3.session.Session().client(
    service_name=BUCKET_SERVICE,
    endpoint_url=BUCKET_HOST,
    aws_access_key_id=BUCKET_KEY_ID,
    aws_secret_access_key=BUCKET_KEY
)