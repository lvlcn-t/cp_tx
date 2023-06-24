FROM python:3.10.12-alpine3.18@sha256:e1d7fc61bb8a17c5a366c7a63c156e0ba1215e4d0dcee71ee85010be64bc51a0

ENV PYTHONUNBUFFERED 1
RUN apk update && apk add --no-cache gcc musl-dev libffi-dev openssl-dev

COPY ./ /app
WORKDIR /app

RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]