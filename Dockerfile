FROM python:3.10-bullseye

ENV PYTHONUNBUFFERED 1
RUN apt-get update && apt-get install -y

COPY ./ /CasualProgress
WORKDIR /CasualProgress

RUN pip3 install -r requirements.txt
CMD ["python3", "main.py"]