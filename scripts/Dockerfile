FROM python:3.7-slim
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
RUN pipenv sync 

CMD gunicorn --bind 0.0.0.0:$PORT wsgi 