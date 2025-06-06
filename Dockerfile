FROM python:3.11-slim

# Install system dependencies for Playwright
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libsoup-3.0-0 \
    libenchant-2-2 \
    libsecret-1-0 \
    libmanette-0.2-0 \
    libgles2 \
    gstreamer1.0-plugins-base gstreamer1.0-plugins-good gstreamer1.0-plugins-bad \
    && rm -rf /var/lib/apt/lists/*

# Set workdir
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt

# Install Playwright browsers
RUN playwright install

# Copy the rest of the code
COPY . .

# Expose port
EXPOSE 8000

# Start the app
CMD ["uvicorn", "scraper.api:app", "--host", "0.0.0.0", "--port", "8000"] 