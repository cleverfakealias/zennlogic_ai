FROM python:3.13-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install .[api]
EXPOSE 8000
CMD ["uvicorn", "src.service.rest.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "uvloop", "--http", "httptools", "--timeout-keep-alive", "15"]
