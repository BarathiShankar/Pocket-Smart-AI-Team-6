import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Ensure project root is in sys.path
BASE_DIR = Path(__file__).resolve().parent.parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

# Load .env file if available
load_dotenv(BASE_DIR / ".env")

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "pocketsmart-super-secret-jwt-key-2026-luxury-gold")
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
    # Default to supported fast Gemini model
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    
    # Storage settings
    DATA_DIR = BASE_DIR / "data"
    DATA_DIR.mkdir(exist_ok=True)
    DATABASE_PATH = os.getenv("DATABASE_PATH", str(DATA_DIR / "pocketsmart.db"))
    
    UPLOAD_FOLDER = BASE_DIR / "uploads"
    UPLOAD_FOLDER.mkdir(exist_ok=True)
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp", "gif"}
    
    # AWS Deployment / Cloud Configuration Placeholders
    AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
    AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET", "")
    AWS_DYNAMODB_TABLE = os.getenv("AWS_DYNAMODB_TABLE", "")
    USE_AWS = os.getenv("USE_AWS", "false").lower() in ("true", "1", "yes")
