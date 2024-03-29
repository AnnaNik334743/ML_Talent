FROM python:3.10

ENV PYTHONUNBUFFERED=1

COPY . /app/

WORKDIR /app

RUN apt-get update
RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y
RUN pip install --upgrade pip

RUN pip install -r requirements.txt