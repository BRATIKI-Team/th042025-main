FROM python:3.11.9-slim
WORKDIR /usr/app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
VOLUME /usr/app/logs /usr/app/data /usr/app/db
