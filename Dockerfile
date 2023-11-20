# Dockerfile
FROM python:3.11.6-alpine3.18

# Set work directory
WORKDIR /app

# Install dependencies
COPY requirements.txt /app
RUN pip3 install -r requirements.txt

# Copy app files
COPY . /app

# Port
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]
