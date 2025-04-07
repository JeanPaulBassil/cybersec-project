FROM python:3.9-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Dynamically copy based on SECURE_VERSION
ARG SECURE_VERSION=false

# Set default to vulnerable unless SECURE_VERSION is true
COPY app_vulnerable.py app.py
RUN if [ "$SECURE_VERSION" = "true" ]; then cp app.py app.secure.py && cp app.secure.py app.py; fi


# Environment variables
ENV DB_HOST=mysql
ENV DB_USER=root
ENV DB_PASSWORD=password
ENV DB_NAME=security_demo

# Expose the Flask port
EXPOSE 8080

# Run the application
CMD ["python", "app.py"] 