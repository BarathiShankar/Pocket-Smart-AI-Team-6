from flask import Blueprint, jsonify, request
from backend.services.platform_service import PlatformAdapter

platform_bp = Blueprint("platform", __name__, url_prefix="/api/platforms")

@platform_bp.route("", methods=["GET"])
def get_platforms():
    platforms = PlatformAdapter.get_supported_platforms()
    return jsonify({
        "success": True,
        "count": len(platforms),
        "platforms": platforms
    })

@platform_bp.route("/search-url", methods=["GET"])
def get_search_url():
    platform = request.args.get("platform", "Amazon")
    query = request.args.get("query", "")
    category = request.args.get("category", "")
    
    url = PlatformAdapter.get_search_url(platform, query, category)
    return jsonify({
        "success": True,
        "platform": platform,
        "url": url
    })
