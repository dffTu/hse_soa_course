FROM python:latest

ADD server /gateway/server/

WORKDIR /gateway/
ENV PYTHONPATH="${PYTHONPATH}:/gateway"

RUN pip install -r server/requirements.txt