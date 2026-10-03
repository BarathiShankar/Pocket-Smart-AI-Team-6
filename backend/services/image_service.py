import os
import uuid
import base64
import logging
from pathlib import Path
from PIL import Image
import io
from werkzeug.utils import secure_filename
from backend.config import Config

logger = logging.getLogger("pocketsmart.image")

class ImageService:
    @staticmethod
    def allowed_file(filename: str) -> bool:
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in Config.ALLOWED_EXTENSIONS

    @classmethod
    def save_upload(cls, file_storage) -> dict:
        """
        Validate and save an uploaded image file securely.
        Returns dict with status, file_path, public_url, and base64_data.
        """
        if not file_storage or file_storage.filename == '':
            return {"success": False, "error": "No file provided"}

        if not cls.allowed_file(file_storage.filename):
            return {
                "success": False, 
                "error": f"Invalid format. Allowed formats: {', '.join(Config.ALLOWED_EXTENSIONS)}"
            }

        try:
            filename = secure_filename(file_storage.filename)
            extension = filename.rsplit('.', 1)[1].lower() if '.' in filename else "jpg"
            unique_filename = f"{uuid.uuid4().hex}_{filename}"
            save_path = Config.UPLOAD_FOLDER / unique_filename

            # Read and validate image using Pillow
            image_bytes = file_storage.read()
            if len(image_bytes) > Config.MAX_CONTENT_LENGTH:
                return {"success": False, "error": "File size exceeds 10MB limit"}

            img = Image.open(io.BytesIO(image_bytes))
            # Convert RGBA or Palette to RGB if needed for JPEG
            if img.mode in ("RGBA", "P") and extension in ("jpg", "jpeg"):
                img = img.convert("RGB")
            
            # Save normalized image
            img.save(save_path)
            
            # Prepare base64 representation for Gemini Multimodal API
            base64_data = base64.b64encode(image_bytes).decode("utf-8")
            mime_type = f"image/{'jpeg' if extension == 'jpg' else extension}"

            return {
                "success": True,
                "filename": unique_filename,
                "file_path": str(save_path),
                "url": f"/uploads/{unique_filename}",
                "base64_data": base64_data,
                "mime_type": mime_type,
                "width": img.width,
                "height": img.height
            }
        except Exception as e:
            logger.error(f"Image upload failed: {e}", exc_info=True)
            return {"success": False, "error": f"Failed to process image: {str(e)}"}
