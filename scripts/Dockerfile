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
RUN pipenv install gunicorn
RUN pipenv install Flask
RUN pipenv install pandas
RUN pipenv install joblib
RUN pipenv install numpy
RUN pipenv install scikit-learn
RUN pipenv install lightgbm
RUN pipenv install youtube-dlc
#RUN pipenv shell

CMD pipenv run gunicorn --bind 0.0.0.0:$PORT wsgi 
