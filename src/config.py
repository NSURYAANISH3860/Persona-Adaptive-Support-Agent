import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
MODEL_NAME = 'gemini-2.5-flash'
# Using the updated embedding model
EMBEDDING_MODEL = 'gemini-embedding-001' 
CHROMA_DB_DIR = "./chroma_db"
# Lowered threshold to prevent false-escalations on technical questions
CONFIDENCE_THRESHOLD = 0.15