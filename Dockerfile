# Use an official lightweight Python image
FROM python:3.10-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1

# Set the working directory
WORKDIR /app

# Copy the application files
COPY . /app/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 for the API
EXPOSE 5000

# Command to start the API
CMD ["python", "api.py"]
