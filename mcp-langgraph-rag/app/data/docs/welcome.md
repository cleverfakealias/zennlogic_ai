# Welcome to the LangGraph MCP RAG Project

This repository demonstrates how to combine a local retrieval-augmented generation (RAG) pipeline with a LangGraph-powered agent that is surfaced through the Model Context Protocol (MCP).

- **MCP Server:** Provides structured tools that clients can call.
- **LangGraph Agent:** Wraps the LLM with tool-calling support.
- **RAG Stack:** Uses FAISS for fast vector similarity search on local documentation.
