# src/core/config.py
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# === API KEYS ===
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")  # Add to .env

# === PATHS ===
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DATA_DIR = os.path.join(BASE_DIR, "data")
RAW_DATA_DIR = os.path.join(DATA_DIR, "raw")
CHROMA_DIR = os.path.join(DATA_DIR, "chroma_db")

# === MODELS ===
EMBED_MODEL = "text-embedding-3-small"  # Change if using a different embedding model
LLM_MODEL = "gpt-4o-mini"               # Change if using another LLM
