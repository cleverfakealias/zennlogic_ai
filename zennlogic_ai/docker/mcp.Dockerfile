FROM python:3.12-slim
WORKDIR /app
COPY . /app
# Install only MCP-related extras (FastAPI + AWS libs)
RUN pip install --upgrade pip && pip install .[mcp]
EXPOSE 8080
CMD ["uvicorn", "service.mcp_server.api:app", "--host", "0.0.0.0", "--port", "8080", "--loop", "uvloop", "--http", "httptools"]
