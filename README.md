```⚠️ This project is in development and not validated. Proceed with caution while using.```

# KOS Invoicing
`KOS Invoicing` is an open-source invoice managing tool which allows the processing and creation of _UBL peppol_ based invoices - aiming to empower small businesses with free digital invoicing capabilities.

##### Yet another CRM accounting software?
Yes, but focusing on accessibility, openness and ease of use.

## Screenshots
tba.

## Documentation
tba.

## Installation
### Docker-compose (recommended)
#### Using github packages
Use the following template for your `docker-compose.yml`. Be aware that you might want to change the environment variables with your own desired values. Please refer to `./.env` for inspiration.
```yaml
version: '3.8'
services:
  web:
    image: ghcr.io/flemk/kos-invoicing:latest
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_HOST=${POSTGRES_HOST}
      - POSTGRES_PORT=${POSTGRES_PORT}
      - HOST=${HOST}
      - ALLOWED_HOST=${ALLOWED_HOST}
      - CSRF_TRUSTED_ORIGIN=${CSRF_TRUSTED_ORIGIN}
    ports:
      - "${WEB_PORT}:80"
      - "${WEB_SSL_PORT}:443"
    volumes:
      - ./web-crt:/app/crt  # Use your own certificates

  db:
    image: postgres:13
    environment:
      - POSTGRES_DB=${POSTGRES_DB}
      - POSTGRES_USER=${POSTGRES_USER}
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
    volumes:
      - ./db-data:/var/lib/postgresql/data

```

#### Building locally
Replace the web service `image` with the following `build` directive:
```yaml
  web:
    build:
      context: .
      dockerfile: Dockerfile
      args:
        - KOS_INVOICING_WEB_VERSION=${KOS_INVOICING_WEB_VERSION}
```

#### Using Docker hub
This Docker image has not been yet uploaded to the Docker hub.

### Docker
Pull or locally build the image and run it with `docker run kos-invoicing`.

### Bare metal
The service can be run bare metal with its's corresponding python command, executed in the respective directory (the one, where `manage.py` is located).

```python
waitress-serve --listen=*:8000 kos_invoice.wsgi:application
```

Or using Djangos development server:
```python
python manage.py runserver
```
