import json
import logging
from flask import Blueprint, request, jsonify, session
from backend.services.ai_service import AIService
from backend.services.image_service import ImageService
from backend.models import save_plan_history

logger = logging.getLogger("pocketsmart.planner_routes")
planner_bp = Blueprint("planner", __name__, url_prefix="/api/planner")

@planner_bp.route("/home", methods=["POST"])
def plan_home():
    try:
        data = request.get_json() or {}
        budget = float(data.get("budget", 0))
        if budget <= 0:
            return jsonify({"success": False, "error": "Please provide a valid budget greater than 0"}), 400

        custom_key = request.headers.get("X-Gemini-Key") or data.get("custom_api_key")
        result = AIService.generate_home_plan(data, custom_api_key=custom_key)

        # Save to history if user logged in or guest session
        user_id = session.get("user_id")
        title = f"{data.get('room_type', 'Home')} Interior Plan - ₹{budget:,.0f}"
        
        summary = result.get("budget_summary", {})
        plan_id = save_plan_history(
            user_id=user_id,
            planner_type="home",
            title=title,
            budget=budget,
            allocated_total=summary.get("allocated_total", budget),
            estimated_spend=summary.get("estimated_spend", budget),
            contingency=summary.get("contingency_reserve", 0),
            inputs_dict=data,
            result_dict=result
        )
        result["plan_id"] = plan_id

        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"Error in home planner: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to generate interior plan: {str(e)}"}), 500

@planner_bp.route("/party", methods=["POST"])
def plan_party():
    try:
        data = request.get_json() or {}
        budget = float(data.get("budget", 0))
        guests = int(data.get("guests", 1))

        if budget <= 0:
            return jsonify({"success": False, "error": "Please provide a valid budget greater than 0"}), 400
        if guests <= 0:
            return jsonify({"success": False, "error": "Guest count must be at least 1"}), 400

        custom_key = request.headers.get("X-Gemini-Key") or data.get("custom_api_key")
        result = AIService.generate_party_plan(data, custom_api_key=custom_key)

        user_id = session.get("user_id")
        title = f"{data.get('event_type', 'Party')} ({guests} Guests) - ₹{budget:,.0f}"
        
        summary = result.get("budget_summary", {})
        plan_id = save_plan_history(
            user_id=user_id,
            planner_type="party",
            title=title,
            budget=budget,
            allocated_total=summary.get("allocated_total", budget),
            estimated_spend=summary.get("estimated_spend", budget),
            contingency=summary.get("contingency_reserve", 0),
            inputs_dict=data,
            result_dict=result
        )
        result["plan_id"] = plan_id

        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"Error in party planner: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to generate party plan: {str(e)}"}), 500

@planner_bp.route("/jewelry", methods=["POST"])
def plan_jewelry():
    try:
        # Handle both JSON and multipart/form-data
        image_data = None
        if request.content_type and "multipart/form-data" in request.content_type:
            data = request.form.to_dict()
            if "image" in request.files:
                file_storage = request.files["image"]
                if file_storage and file_storage.filename:
                    upload_res = ImageService.save_upload(file_storage)
                    if upload_res.get("success"):
                        image_data = upload_res
                    else:
                        return jsonify({"success": False, "error": upload_res.get("error")}), 400
        else:
            data = request.get_json() or {}

        budget = float(data.get("budget", 0))
        if budget <= 0:
            return jsonify({"success": False, "error": "Please provide a valid budget greater than 0"}), 400

        custom_key = request.headers.get("X-Gemini-Key") or data.get("custom_api_key")
        result = AIService.generate_jewelry_plan(data, image_data=image_data, custom_api_key=custom_key)

        if image_data:
            result["uploaded_image_url"] = image_data.get("url")

        user_id = session.get("user_id")
        title = f"{data.get('jewelry_category', 'Jewelry')} ({data.get('metal', 'Gold')}) - ₹{budget:,.0f}"
        
        summary = result.get("budget_summary", {})
        plan_id = save_plan_history(
            user_id=user_id,
            planner_type="jewelry",
            title=title,
            budget=budget,
            allocated_total=summary.get("allocated_total", budget),
            estimated_spend=summary.get("estimated_spend", budget),
            contingency=summary.get("contingency_reserve", 0),
            inputs_dict=data,
            result_dict=result
        )
        result["plan_id"] = plan_id

        return jsonify({
            "success": True,
            "data": result
        })
    except Exception as e:
        logger.error(f"Error in jewelry planner: {e}", exc_info=True)
        return jsonify({"success": False, "error": f"Failed to generate jewelry plan: {str(e)}"}), 500
