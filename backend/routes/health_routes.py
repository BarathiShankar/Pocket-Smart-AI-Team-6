import os
import sys
from flask import Blueprint, jsonify
from backend.config import Config

health_bp = Blueprint("health", __name__, url_prefix="/api/health")

@health_bp.route("", methods=["GET"])
def health_check():
    gemini_configured = bool(Config.GEMINI_API_KEY)
    
    return jsonify({
        "status": "healthy",
        "service": "PocketSmart AI",
        "version": "2.0.0",
        "python_version": sys.version,
        "ai_engine": {
            "model": Config.GEMINI_MODEL,
            "api_key_configured": gemini_configured,
            "multimodal_supported": True,
            "mode": "Active Gemini Generation" if gemini_configured else "Intelligent Heuristic Fallback (Zero Downtime)"
        },
        "storage": {
            "type": "SQLite (DynamoDB ready)",
            "database": os.path.basename(Config.DATABASE_PATH)
        },
        "architecture_mapping": {
            "cdn": "Amazon CloudFront (Target)",
            "dns": "Amazon Route 53 (Target)",
            "api_gateway": "Amazon API Gateway (Target)",
            "compute": "AWS Lambda / Flask WSGI Backend (Implemented)",
            "ai": "Google Gemini 2.5 Flash Multimodal (Implemented)",
            "database": "SQLite Local / AWS DynamoDB Adapter (Implemented & Ready)",
            "storage": "Local File / AWS S3 Uploads (Implemented & Ready)",
            "monitoring": "CloudWatch Ready Logging (Implemented)"
        }
    })
