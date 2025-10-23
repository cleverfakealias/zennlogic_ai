# zennlogic_ai_service

Applied AI RAG/chat service with REST API and MCP server support.

## Overview

zennlogic_ai_service is a comprehensive AI service that provides retrieval-augmented generation (RAG) capabilities through both REST API and Model Context Protocol (MCP) interfaces. The service supports multiple vector backends, LLM providers, and cloud integrations.

## Features

- **REST API**: FastAPI-based HTTP endpoints for chat and RAG operations
- **MCP Server**: Model Context Protocol server for tool-based AI interactions
- **Vector Backends**: Support for FAISS and Annoy vector databases
- **LLM Providers**: OpenAI and AWS Bedrock integration
- **Authentication**: API key-based authentication for secure access
- **AWS Integration**: S3 for data storage, SSM for configuration management
- **Embeddings**: Sentence-transformers for text vectorization
- **Observability**: Structured logging and optional LangSmith tracing

## Installation

### Prerequisites

- Python 3.12+
- uv package manager (recommended)

### Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd zennlogic_ai_service
```

2. Install dependencies:
```bash
uv sync
```

3. Install pre-commit hooks:
```bash
uv run pre-commit install
```

## Configuration

Create a `.env` file based on `.env.example`:

```bash
cp .env.example .env
```

### Required Environment Variables

- `OPENAI_API_KEY`: OpenAI API key (if using OpenAI provider)
- `AWS_REGION`: AWS region for Bedrock/S3/SSM services
- `SSM_API_KEY_PARAM`: SSM parameter name for API key storage

### Optional Environment Variables

- `ENV`: Environment name (default: local)
- `VECTOR_BACKEND`: Vector backend to use - faiss, annoy, or auto (default: auto)
- `LLM_PROVIDER`: LLM provider - openai or bedrock (default: openai)
- `EMBED_PROVIDER`: Embedding provider - openai or bedrock (default: openai)
- `EMBED_MODEL`: Sentence-transformers model name (default: sentence-transformers/all-MiniLM-L6-v2)
- `MAX_TOKENS`: Maximum tokens for LLM responses (default: 256)
- `TOP_K`: Number of similar documents to retrieve (default: 5)
- `LANGSMITH_TRACING`: Enable LangSmith tracing (default: false)

## Usage

### REST API

Start the REST API server:

```bash
uv run uvicorn zennlogic_ai_service.rest.app:app --reload
```

The API will be available at `http://localhost:8000`

#### Endpoints

- `GET /health`: Health check endpoint
- `POST /chat`: Chat with LLM
- `POST /rag/search`: Search documents using RAG

All endpoints except `/health` require API key authentication.

### MCP Server

Run the MCP server:

```bash
uv run mcp-server
```

The MCP server provides tools for health checks, RAG operations, and S3 interactions.

## Development

### Code Quality

The project uses several tools for code quality:

- **ruff**: Linting and formatting
- **mypy**: Type checking
- **pytest**: Testing

### Development Commands

```bash
# Run tests
uv run pytest

# Run linting
uv run ruff check src tests

# Format code
uv run ruff format src tests

# Type checking
uv run mypy src

# Run all checks
just test && just lint && just typecheck
```

### Project Structure

```
src/zennlogic_ai_service/
├── auth/                 # Authentication modules
├── aws/                  # AWS service integrations
├── config.py            # Application configuration
├── llm/                 # LLM provider abstractions
├── mcp_server/         # MCP server implementation
├── rag/                 # RAG pipeline components
├── rest/                # REST API implementation
└── logging.py           # Logging configuration
```

## Testing

Run the test suite:

```bash
uv run pytest
```

Run with coverage:

```bash
uv run pytest --cov=src/zennlogic_ai_service
```

## Deployment

### Local Development

Use the provided scripts or run directly with uvicorn:

```bash
uv run uvicorn zennlogic_ai_service.rest.app:app --host 0.0.0.0 --port 8000
```

### AWS Deployment

The project includes CloudFormation templates for AWS deployment:

```bash
# Validate templates
make validate

# Deploy infrastructure
make deploy-all

# Deploy application
make deploy-application
```

See the `Makefile` for available deployment commands.

## Docker

Build and run with Docker:

```bash
# Build image
docker build -f docker/mcp.Dockerfile -t zennlogic-ai .

# Run container
docker run -p 8000:8000 zennlogic-ai
```

## License

MIT License - see LICENSE file for details.
