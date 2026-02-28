FROM python:3.9-slim

RUN pip install --no-cache-dir flask

WORKDIR /app
COPY app.py /app/app.py

EXPOSE 80
CMD ["python", "app.py"]
