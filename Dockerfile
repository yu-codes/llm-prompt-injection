# Use Python 3.11 image as base
FROM python:3.11

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH=/app

# Set work directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt ./

# Install Python dependencies
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

# Copy project files
COPY . .

# Create necessary directories
RUN mkdir -p /app/output/reports /app/output/logs /app/output/temp

# Expose port (if we add a web interface later)
EXPOSE 8080

# Default command
CMD ["python", "src/main.py", "--help"]