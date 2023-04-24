FROM python:3.10-slim
COPY . /app
WORKDIR /app
RUN apt-get update &&\
    apt-get install -y --no-install-recommends \
    ca-certificates \
    cmake \
    build-essential \
    gcc \
    g++ 

RUN pip install pipenv
RUN pipenv install

CMD gunicorn --bind 0.0.0.0:$PORT wsgi 
