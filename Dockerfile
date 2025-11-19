# Use slim base for smaller image
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Ensure models dir and copy model from repo root into it
RUN mkdir -p /app/models
# If rf_blade_model.pkl exists in repo root, copy it to the expected location
COPY rf_blade_model.pkl /app/models/rf_blade_model.pkl

# Environment variables
ENV FLASK_ENV=production
ENV MODEL_PATH=models/rf_blade_model.pkl

# Render provides $PORT at runtime (we expose a default for clarity)
ENV PORT=10000
EXPOSE 10000

# Start via shell so $PORT expands
CMD ["sh", "-c", "gunicorn 'src.windturbine.app:app' --bind 0.0.0.0:$PORT --workers 2"]
