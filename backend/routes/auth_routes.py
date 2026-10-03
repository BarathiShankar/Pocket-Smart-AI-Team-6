from flask import Blueprint, request, jsonify, session
from backend.models import create_user, authenticate_user, get_user_by_id, update_user_profile

auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")

@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")
    name = data.get("name", "").strip()
    location = data.get("location", "Mumbai, India").strip()
    currency = data.get("currency", "INR").strip()

    if not email or not password or not name:
        return jsonify({"success": False, "error": "Name, email, and password are required"}), 400

    if len(password) < 6:
        return jsonify({"success": False, "error": "Password must be at least 6 characters"}), 400

    user = create_user(email, password, name, location, currency)
    if not user:
        return jsonify({"success": False, "error": "An account with this email already exists"}), 409

    session["user_id"] = user["id"]
    return jsonify({
        "success": True,
        "message": "Account created successfully",
        "user": user
    }), 201

@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")

    if not email or not password:
        return jsonify({"success": False, "error": "Email and password are required"}), 400

    user = authenticate_user(email, password)
    if not user:
        return jsonify({"success": False, "error": "Invalid email or password"}), 401

    session["user_id"] = user["id"]
    return jsonify({
        "success": True,
        "message": "Logged in successfully",
        "user": {
            "id": user["id"],
            "email": user["email"],
            "name": user["name"],
            "location": user.get("location", "Mumbai, India"),
            "currency": user.get("currency", "INR")
        }
    })

@auth_bp.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"success": True, "message": "Logged out successfully"})

@auth_bp.route("/me", methods=["GET"])
def get_current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"authenticated": False, "user": None})

    user = get_user_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"authenticated": False, "user": None})

    return jsonify({"authenticated": True, "user": user})

@auth_bp.route("/profile", methods=["PUT"])
def update_profile():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"success": False, "error": "Authentication required"}), 401

    data = request.get_json() or {}
    name = data.get("name", "").strip()
    location = data.get("location", "Mumbai, India").strip()
    currency = data.get("currency", "INR").strip()

    if not name:
        return jsonify({"success": False, "error": "Name is required"}), 400

    updated = update_user_profile(user_id, name, location, currency)
    return jsonify({
        "success": True,
        "message": "Profile updated successfully",
        "user": updated
    })
