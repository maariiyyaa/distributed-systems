from python:3.11.0b3-alpine3.16
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apk update & apk upgrade & apk add curl
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD python /app/main.py