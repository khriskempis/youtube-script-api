import os
from dotenv import load_dotenv
import logging

load_dotenv()

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Config:
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY")
    PROXY = os.environ.get("PROXY")
    PORT = int(os.environ.get("PORT", 8080))