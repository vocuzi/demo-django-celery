FROM python:3.7-buster

RUN apt-get update && apt-get install nginx nano rabbitmq-server -y --no-install-recommends
COPY nginx.default /etc/nginx/sites-available/atlan
RUN ln -s /etc/nginx/sites-available/atlan /etc/nginx/sites-enabled/


WORKDIR /usr/src/app

RUN pip install --upgrade pip
COPY . .
RUN pip install -r requirements.txt
RUN python manage.py collectstatic --noinput


EXPOSE 8000
STOPSIGNAL SIGTERM
CMD ["/usr/src/app/start.sh"]