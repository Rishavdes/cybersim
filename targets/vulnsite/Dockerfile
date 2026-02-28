FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Create data directory
RUN mkdir -p /app/uploads

EXPOSE 5000

ENV FLASK_APP=app.py
ENV DIFFICULTY=easy

CMD ["python", "app.py"]
