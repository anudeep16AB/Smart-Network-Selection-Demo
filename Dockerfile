# Use lightweight official Python image
FROM python:3.9-slim

# Force Python unbuffered logging so prints appear instantly in Podman
ENV PYTHONUNBUFFERED=1

# Set working directory inside the container
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy dataset, app, and HTML templates
COPY fully_extended_processed_data.csv .
COPY app_extended.py .
COPY templates/ ./templates/

# Expose the Flask port
EXPOSE 5001

# Run the extended container application
CMD ["python", "app_extended.py"]