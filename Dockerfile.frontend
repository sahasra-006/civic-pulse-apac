FROM python:3.11-slim
WORKDIR /app
COPY frontend/ ./frontend/
COPY serve.py .
EXPOSE 8080
CMD ["python", "serve.py"] 
