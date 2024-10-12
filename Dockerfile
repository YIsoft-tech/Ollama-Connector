# Use the official Python 3.8 image as the base image
FROM python:3.8-slim

# Set the working directory in the container to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install Flask (since there are no other requirements)
RUN pip install Flask

# Expose the port that Flask will run on
EXPOSE 5000

# Define environment variables for Python
ENV PYTHONUNBUFFERED=1

# Command to run your Flask app
CMD ["python", "manage_server.py"]
