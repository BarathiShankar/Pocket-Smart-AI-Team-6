from flask import Blueprint, request, jsonify, session
from backend.models import (
    get_user_plan_history,
    get_plan_by_id,
    delete_plan,
    save_item_to_favorites,
    get_user_saved_items,
    delete_saved_item
)

history_bp = Blueprint("history", __name__, url_prefix="/api/history")

@history_bp.route("", methods=["GET"])
def list_history():
    user_id = session.get("user_id")
    limit = request.args.get("limit", 50, type=int)
    history = get_user_plan_history(user_id=user_id, limit=limit)
    return jsonify({
        "success": True,
        "count": len(history),
        "history": history
    })

@history_bp.route("/<int:plan_id>", methods=["GET"])
def get_plan(plan_id):
    user_id = session.get("user_id")
    plan = get_plan_by_id(plan_id, user_id=user_id)
    if not plan:
        # Fallback to general lookup if user not strictly filtered
        plan = get_plan_by_id(plan_id)
    if not plan:
        return jsonify({"success": False, "error": "Plan not found"}), 404
    return jsonify({"success": True, "plan": plan})

@history_bp.route("/<int:plan_id>", methods=["DELETE"])
def remove_plan(plan_id):
    user_id = session.get("user_id")
    deleted = delete_plan(plan_id, user_id=user_id)
    if not deleted:
        return jsonify({"success": False, "error": "Plan not found or could not be deleted"}), 404
    return jsonify({"success": True, "message": "Plan deleted successfully"})

@history_bp.route("/saved-items", methods=["GET"])
def list_saved_items():
    user_id = session.get("user_id")
    items = get_user_saved_items(user_id=user_id)
    return jsonify({
        "success": True,
        "count": len(items),
        "saved_items": items
    })

@history_bp.route("/saved-items", methods=["POST"])
def add_saved_item():
    user_id = session.get("user_id")
    data = request.get_json() or {}
    if not data.get("name"):
        return jsonify({"success": False, "error": "Item name is required"}), 400

    item_id = save_item_to_favorites(user_id=user_id, item_data=data)
    return jsonify({
        "success": True,
        "message": "Item saved to your favorites",
        "item_id": item_id
    }), 201

@history_bp.route("/saved-items/<int:item_id>", methods=["DELETE"])
def remove_saved_item(item_id):
    user_id = session.get("user_id")
    deleted = delete_saved_item(item_id, user_id=user_id)
    if not deleted:
        return jsonify({"success": False, "error": "Item not found"}), 404
    return jsonify({"success": True, "message": "Item removed from favorites"})
