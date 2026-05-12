# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set environment variables
WORKDIR /backend

# Install system dependencies
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade -r requirements.txt

# Make port 8001 available external to this container
EXPOSE 8001

# Copy the current directory contents into the container at /backend
COPY ./ .

# Run the application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]

# CMD ["fastapi", "run", "app/main.py", "--port", "8000"]