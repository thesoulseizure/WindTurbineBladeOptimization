FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# copy only needed files
COPY . .

ENV FLASK_APP=app.py
ENV PORT=5002
EXPOSE 5002

CMD ["gunicorn", "--bind", "0.0.0.0:5002", "app:app", "--workers", "2", "--timeout", "60"]
