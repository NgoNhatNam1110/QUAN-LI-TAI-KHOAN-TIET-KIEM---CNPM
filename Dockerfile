# Use an official Python runtime as a parent image
FROM python:3.12

# Set environment variables to prevent Python from writing .pyc files and buffering stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set the working directory in the container
WORKDIR /app

# Install system dependencies for Tkinter and other GUI libraries
RUN apt-get update && \
    apt-get install -y python3-tk tk curl && \
    curl https://sh.rustup.rs -sSf | sh -s -- -y && \
    rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Set the default command (update this if your main file is different)
CMD ["python", "GUI/runapp.py"]