FROM python:latest

ADD server /posts/server/
ADD db /posts/db

WORKDIR /posts/
ENV PYTHONPATH="${PYTHONPATH}:/posts"

RUN pip install -r server/requirements.txt
