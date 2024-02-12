# Use an official Python runtime as a parent image
FROM python:3.9-slim

ARG OPENAI_API_KEY
ARG FRONTEND_URL

ENV OPENAI_API_KEY=${OPENAI_API_KEY}
ENV FRONTEND_URL=${FRONTEND_URL}

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the dependencies file to the working directory
COPY requirements.txt .

# Install any dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the content of the local src directory to the working directory
COPY . .

# Specify the command to run on container start
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8080"]
