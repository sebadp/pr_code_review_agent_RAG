import logging

import os

# Config
VECTOR_STORE_DIR = os.getenv("VECTOR_STORE_DIR", "data/vectorstore")
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "mistral")
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
