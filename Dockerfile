FROM python:3.8.2-slim-buster
ENV PYTHONUNBUFFERED=1

RUN apt-get update && rm -rf /var/lib/apt/lists/*

RUN mkdir /pollen
COPY . /pollen

WORKDIR /pollen
RUN pip install -r requirements.txt

ENTRYPOINT ["python", "/pollen/src/app.py"]
