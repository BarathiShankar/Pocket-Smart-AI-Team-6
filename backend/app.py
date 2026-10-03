import os
import sys
import logging
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from flask import Flask, send_from_directory, jsonify, send_file
from flask_cors import CORS
from backend.config import Config
from backend.models import init_db

# Configure Structured Logging (CloudWatch Ready)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] [%(name)s]: %(message)s",
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger("pocketsmart.app")

def create_app():
    app = Flask(
        __name__,
        static_folder=str(Path(__file__).resolve().parent.parent / "frontend"),
        static_url_path=""
    )
    
    app.config["SECRET_KEY"] = Config.SECRET_KEY
    app.config["MAX_CONTENT_LENGTH"] = Config.MAX_CONTENT_LENGTH

    # CORS configuration
    CORS(app, supports_credentials=True, origins=["*"])

    # Initialize Database Schema
    init_db()

    # Register Blueprints
    from backend.routes.auth_routes import auth_bp
    from backend.routes.planner_routes import planner_bp
    from backend.routes.history_routes import history_bp
    from backend.routes.platform_routes import platform_bp
    from backend.routes.health_routes import health_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(planner_bp)
    app.register_blueprint(history_bp)
    app.register_blueprint(platform_bp)
    app.register_blueprint(health_bp)

    # Serve uploaded images securely
    @app.route("/uploads/<path:filename>")
    def serve_upload(filename):
        return send_from_directory(Config.UPLOAD_FOLDER, filename)

    # Serve Frontend UI
    @app.route("/")
    def index():
        frontend_index = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        if frontend_index.exists():
            return send_file(frontend_index)
        return jsonify({
            "message": "PocketSmart AI Backend 2.0 is running successfully!",
            "status": "online"
        })

    # Backward compatibility endpoint for legacy tests
    @app.route("/generate-home", methods=["GET"])
    def legacy_home():
        from flask import request
        from backend.services.ai_service import AIService
        budget = float(request.args.get("budget", 200000))
        res = AIService.generate_home_plan({"budget": budget})
        return jsonify({
            "planner": "home",
            "budget": budget,
            "recommendations": [r["name"] for r in res.get("recommendations", [])],
            "full_plan": res
        })

    @app.route("/generate-party", methods=["GET"])
    def legacy_party():
        from flask import request
        from backend.services.ai_service import AIService
        budget = float(request.args.get("budget", 50000))
        guests = int(request.args.get("guests", 30))
        res = AIService.generate_party_plan({"budget": budget, "guests": guests})
        return jsonify({
            "planner": "party",
            "budget": budget,
            "guests": guests,
            "recommendations": [r["name"] for r in res.get("recommendations", [])],
            "full_plan": res
        })

    @app.route("/generate-jewelry", methods=["GET"])
    def legacy_jewelry():
        from flask import request
        from backend.services.ai_service import AIService
        budget = float(request.args.get("budget", 100000))
        res = AIService.generate_jewelry_plan({"budget": budget})
        return jsonify({
            "planner": "jewelry",
            "budget": budget,
            "recommendations": [r["name"] for r in res.get("recommendations", [])],
            "full_plan": res
        })

    # Global Error Handlers (Never expose internal stack traces to users)
    @app.errorhandler(404)
    def not_found_handler(e):
        # If it's an API request, return JSON; otherwise serve index.html for SPA routing
        from flask import request
        if request.path.startswith("/api/"):
            return jsonify({"success": False, "error": "Endpoint not found"}), 404
        frontend_index = Path(__file__).resolve().parent.parent / "frontend" / "index.html"
        if frontend_index.exists():
            return send_file(frontend_index)
        return jsonify({"success": False, "error": "Resource not found"}), 404

    @app.errorhandler(413)
    def file_too_large(e):
        return jsonify({"success": False, "error": "Uploaded file is too large (maximum 10MB)"}), 413

    @app.errorhandler(500)
    def internal_error(e):
        logger.error(f"Internal server error: {e}", exc_info=True)
        return jsonify({"success": False, "error": "An internal server error occurred. Please try again later."}), 500

    return app

app = create_app()

if __name__ == "__main__":
    port = int(os.getenv("PORT", 5000))
    logger.info(f"Starting PocketSmart AI server on port {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)
