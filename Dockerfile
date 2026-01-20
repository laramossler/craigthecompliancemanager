# Craig - The AI Compliance Manager
# Docker container for production deployment

FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    cron \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Make craig.py executable
RUN chmod +x craig.py

# Create cron job file
RUN echo "0 9 * * 1-5 cd /app && /usr/local/bin/python craig.py daily-check >> /var/log/craig-daily.log 2>&1" > /etc/cron.d/craig-daily && \
    echo "0 16 * * 5 cd /app && /usr/local/bin/python craig.py weekly-summary >> /var/log/craig-weekly.log 2>&1" > /etc/cron.d/craig-weekly && \
    chmod 0644 /etc/cron.d/craig-daily && \
    chmod 0644 /etc/cron.d/craig-weekly && \
    crontab /etc/cron.d/craig-daily && \
    crontab /etc/cron.d/craig-weekly

# Create log directory
RUN mkdir -p /var/log && touch /var/log/craig-daily.log /var/log/craig-weekly.log

# Health check
HEALTHCHECK --interval=1h --timeout=10s --start-period=5s --retries=3 \
  CMD python craig.py test || exit 1

# Start cron in foreground
CMD ["cron", "-f"]

# Alternative: Run once and exit (for serverless functions)
# CMD ["python", "craig.py", "daily-check"]
