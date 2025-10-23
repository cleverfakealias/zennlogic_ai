"""Structured logging setup for zennlogic_ai_service."""

import logging

import structlog


logging.basicConfig(level=logging.INFO)
logger = structlog.get_logger()
