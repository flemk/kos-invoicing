FROM python:3.12.4-bookworm

ARG KOS_INVOICING_WEB_VERSION

EXPOSE 80 443

WORKDIR /app
ADD . /app

RUN pip install --no-cache-dir -r requirements.txt
RUN python ./kos_invoice/manage.py collectstatic --noinput

RUN sed -i 's/%KOS_INVOICING_WEB_VERSION%/'"$KOS_INVOICING_WEB_VERSION"'/g' ./kos_invoice/invoicing/templates/html/base.html

RUN openssl req -x509 -newkey rsa:4096 -keyout ./crt/key.pem -out ./crt/cert.pem -days 365 -nodes -subj '/CN=localhost'
RUN apt-get update && apt-get install -y nginx && rm -rf /var/lib/apt/lists/*
COPY nginx.conf /etc/nginx/sites-available/default

CMD python ./kos_invoice/manage.py migrate && nginx -c /app/nginx.conf && cd ./kos_invoice && waitress-serve --listen=*:8000 kos_invoice.wsgi:application
