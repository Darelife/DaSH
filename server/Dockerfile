# server/Dockerfile

# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . .

# Install the required Python packages
RUN pip install --no-cache-dir requests python-dotenv

# Expose port 6942 for the server
EXPOSE 6942

# Run server.py when the container launches
CMD ["python", "server.py"]
