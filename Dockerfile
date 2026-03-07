# Dockerfile for Hugging Face Spaces deployment
FROM python:3.12-slim

WORKDIR /app

# Copy and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . .

# Create a folder for the SQLite database (required for HF Space persistent storage or local file writing)
RUN mkdir -p /app/data && chmod 777 /app/data

# Expose port (Hugging Face Spaces uses port 7860 by default)
EXPOSE 7860

# Startup command
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "7860"]
