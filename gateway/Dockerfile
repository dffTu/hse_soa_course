FROM python:latest

ADD server /gateway/server/
ADD db /gateway/db

WORKDIR /gateway/
ENV PYTHONPATH="${PYTHONPATH}:/gateway"

RUN pip install -r server/requirements.txt