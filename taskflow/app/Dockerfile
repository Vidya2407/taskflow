# Base image — Python 3.12
FROM python:3.12-slim

# Set working directory inside container
WORKDIR /app

# Copy requirements first (for faster builds)
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy rest of the app
COPY . .

# Expose port 5000
EXPOSE 5000

# Run the app
CMD ["python", "app.py"]