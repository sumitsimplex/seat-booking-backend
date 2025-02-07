# Use a smaller base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy only necessary files first (improves caching)
COPY requirements.txt /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . /app/

# Expose the application port
EXPOSE 5000

# Define environment variables
ENV FLASK_APP=src/api_local.py
ENV FLASK_RUN_HOST=0.0.0.0

# Run the application
CMD ["flask", "run"]
