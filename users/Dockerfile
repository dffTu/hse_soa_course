FROM python:latest

ADD server /users/server/
ADD db /users/db

WORKDIR /users/
ENV PYTHONPATH="${PYTHONPATH}:/users"

RUN pip install -r server/requirements.txt
