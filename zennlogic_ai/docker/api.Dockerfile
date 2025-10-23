FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install .
EXPOSE 8000
CMD ["uvicorn", "src.zennlogic_ai_service.rest.app:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "1", "--loop", "uvloop", "--http", "httptools", "--timeout-keep-alive", "15"]
