# Use slim base for smaller image
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Environment variables
ENV FLASK_ENV=production
ENV MODEL_PATH=models/rf_blade_model.pkl

# Render provides $PORT at runtime
ENV PORT=10000
EXPOSE 10000

# Start gunicorn using Render's assigned port
CMD ["gunicorn", "src.windturbine.app:app", "--bind", "0.0.0.0:$PORT", "--workers", "2"]
