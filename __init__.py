import os
import boto3
from ultralytics import YOLO
from openai import OpenAI
from dotenv import load_dotenv
from prompts import ENGLISH_PROMPT, RUSSIAN_PROMPT

load_dotenv()

API_KEY = os.getenv('API_KEY')

GPT_MODEL = os.getenv('GPT_MODEL')
CLIENT = OpenAI(api_key=API_KEY)

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
