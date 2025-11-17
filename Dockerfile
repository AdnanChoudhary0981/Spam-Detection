
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY . /app
EXPOSE 8080
ENV FLASK_APP=app.py
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:8080", "--workers=4"]
