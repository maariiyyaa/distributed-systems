FROM python:3.7
COPY requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install --no-cache-dir -r /app/requirements.txt
RUN   echo "__version__ = '5.1'" >> /usr/local/lib/python3.7/site-packages/hazelcast/__init__.py
CMD python /app/main.py