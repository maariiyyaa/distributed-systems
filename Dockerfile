from python:3.7-bullseye
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN apt update & apt upgrade & apt install gcc
RUN pip install --no-cache-dir -r /app/requirements.txt
CMD python /app/main.py