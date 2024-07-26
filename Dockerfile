# Use the official Python image from the Docker Hub
FROM python:3.11.9-slim

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Copy the requirements file to the container
COPY requirements.txt /code/

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies
RUN pip install -r requirements.txt

# Copy the current directory contents into the container at /code
COPY . /code/

# Copy sample.env to .env
RUN cp /code/sample.env /code/.env

# Run the entrypoint script
ENTRYPOINT ["sh", "-c", "python3 manage.py migrate && python3 manage.py runserver 0.0.0.0:8000"]
