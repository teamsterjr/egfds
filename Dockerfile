# For Python 3.4
FROM tiangolo/uwsgi-nginx-flask:python3.7
ENV FLASK_APP=egfds
COPY requirements.txt /app

RUN pip install -r requirements.txt; rm requirements.txt

COPY . /app
RUN flask assets build;rm -r instance requirements.txt prestart.sh main.py
