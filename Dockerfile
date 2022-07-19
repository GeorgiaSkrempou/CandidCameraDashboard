FROM python:3.10

WORKDIR /app

COPY requirements.txt .

RUN apt-get update && apt-get install ffmpeg libsm6 libxext6  -y && \
    pip install -r requirements.txt

COPY . .

ENV MEDIA_URL='/app/CandidCameraDashboard/media/'

CMD python CandidCameraDashboard/manage.py runserver 0.0.0.0:8000
