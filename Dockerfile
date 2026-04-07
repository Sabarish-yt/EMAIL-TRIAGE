FROM python:3.10-slim

WORKDIR /app

# Copy files
COPY . .

# Install dependencies (stable)
RUN pip install --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 7860

# Run using main() (IMPORTANT for Scaler)
CMD ["python", "-m", "server.app"]
