FROM python:3.12-slim
WORKDIR /app
COPY . /app
RUN pip install --upgrade pip && pip install .
EXPOSE 9000
CMD ["mcp-server"]
