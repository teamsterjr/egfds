# For Python 3.4
FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt /app
RUN pip install -r /app/requirements.txt;rm /app/*
COPY uwsgi.ini /app
COPY egfds /app/egfds
COPY TODO /app
ENV FLASK_APP=egfds
RUN flask assets build
