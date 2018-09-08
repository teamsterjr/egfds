# For Python 3.4
FROM amazon/aws-eb-python:3.4.2-onbuild-3.5.1
ENV FLASK_APP=ninty
RUN ./bin/flask init-db
COPY refs/todo ninty/static/todo.txt
COPY .secret /etc/profile.d/
EXPOSE 8080

