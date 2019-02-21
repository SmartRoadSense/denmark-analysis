FROM frolvlad/alpine-python-machinelearning 

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
COPY ./requirements.txt .

RUN pip install -r requirements.txt

ENV PYTHONUNBUFFERED 1

COPY . .
