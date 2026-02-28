FROM python:3.11-slim
WORKDIR /app
RUN pip install --no-cache-dir flask requests
COPY . .
EXPOSE 5001
ENV DIFFICULTY=easy
CMD ["python", "app.py"]
