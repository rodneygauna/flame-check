# Dockerfile
FROM python:3.11.6-slim-bookworm

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy app files
COPY . /app