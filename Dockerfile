# For Python 3.4
FROM tiangolo/uwsgi-nginx-flask:python3.7

COPY requirements.txt /app
RUN pip install -r requirements.txt
COPY conf/uwsgi.ini /app
ENV FLASK_APP=egfds
COPY TODO /app
COPY egfds /app/egfds
RUN flask assets build;rm -r instance requirements.txt prestart.sh main.py
