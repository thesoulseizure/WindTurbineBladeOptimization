# Use slim base for smaller image
FROM python:3.10-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_ENV=production
ENV MODEL_PATH=models/rf_blade_model.pkl

CMD ["gunicorn", "src.windturbine.app:app", "--bind", "0.0.0.0:5000", "--workers", "2"]
