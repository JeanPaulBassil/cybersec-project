FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY app.py .

# Environment variables
ENV DB_HOST=mysql
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=security_demo

# Expose the Flask port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"] 