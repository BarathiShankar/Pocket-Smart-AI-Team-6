import sys
from pathlib import Path

# Ensure project root is in sys.path
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

import unittest
import json
import io
from PIL import Image
from backend.app import create_app
from backend.config import Config

class PocketSmartTestSuite(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.app.config["TESTING"] = True
        self.client = self.app.test_client()

    def test_01_health_check(self):
        res = self.client.get("/api/health")
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertEqual(data["status"], "healthy")
        self.assertIn("architecture_mapping", data)
        print("[PASS] Health Check Passed")

    def test_02_auth_workflow(self):
        # 1. Register new user
        unique_email = f"test_user_{id(self)}@pocketsmart.ai"
        reg_res = self.client.post("/api/auth/register", json={
            "name": "Jane Doe",
            "email": unique_email,
            "password": "securepassword123",
            "location": "Mumbai, India",
            "currency": "INR"
        })
        self.assertEqual(reg_res.status_code, 201)
        
        # 2. Check /api/auth/me
        me_res = self.client.get("/api/auth/me")
        self.assertEqual(me_res.status_code, 200)
        self.assertTrue(me_res.get_json()["authenticated"])
        
        # 3. Logout
        logout_res = self.client.post("/api/auth/logout")
        self.assertEqual(logout_res.status_code, 200)
        
        # 4. Login
        login_res = self.client.post("/api/auth/login", json={
            "email": unique_email,
            "password": "securepassword123"
        })
        self.assertEqual(login_res.status_code, 200)
        print("[PASS] Auth Workflow (Register/Login/Logout/Me) Passed")

    def test_03_home_planner(self):
        payload = {
            "budget": 300000,
            "location": "Bangalore",
            "room_type": "2 BHK Apartment",
            "style": "Modern Minimalist",
            "colors": "Warm Beige & Gold",
            "furniture": "Sofa, Bed, Dining Table"
        }
        res = self.client.post("/api/planner/home", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        plan = data["data"]
        self.assertIn("budget_summary", plan)
        self.assertIn("allocation", plan)
        self.assertIn("recommendations", plan)
        self.assertGreater(len(plan["recommendations"]), 0)
        self.assertGreater(plan["budget_summary"]["contingency_reserve"], 0)
        print("[PASS] Home Planner Generation Passed")

    def test_04_party_planner(self):
        payload = {
            "budget": 75000,
            "guests": 50,
            "event_type": "Birthday Celebration",
            "location": "Mumbai",
            "venue": "Boutique Banquet Hall",
            "food": "Multi-cuisine Buffet"
        }
        res = self.client.post("/api/planner/party", json=payload)
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        self.assertTrue(data["success"])
        plan = data["data"]
        self.assertEqual(plan["budget_summary"]["guests_count"], 50)
        self.assertIn("recommendations", plan)
        print("[PASS] Party Planner Generation Passed")

    def test_05_jewelry_planner_with_image(self):
        # Create a tiny dummy image in memory
        img_byte_arr = io.BytesIO()
        test_image = Image.new('RGB', (100, 100), color='maroon')
        test_image.save(img_byte_arr, format='JPEG')
        img_byte_arr.seek(0)

        data = {
            "budget": "150000",
            "jewelry_category": "Bridal Set",
            "occasion": "Wedding Reception",
            "metal": "22K Yellow Gold",
            "gemstone": "Emeralds & Diamonds",
            "style": "Traditional Kundan",
            "image": (img_byte_arr, "test_outfit.jpg")
        }
        res = self.client.post(
            "/api/planner/jewelry",
            data=data,
            content_type="multipart/form-data"
        )
        self.assertEqual(res.status_code, 200)
        res_data = res.get_json()
        self.assertTrue(res_data["success"])
        plan = res_data["data"]
        self.assertIn("image_analysis", plan)
        self.assertIn("uploaded_image_url", plan)
        print("[PASS] Jewelry Multimodal Planner with Image Upload Passed")

    def test_06_history_and_favorites(self):
        # Fetch history
        hist_res = self.client.get("/api/history")
        self.assertEqual(hist_res.status_code, 200)
        hist_data = hist_res.get_json()
        self.assertTrue(hist_data["success"])
        self.assertGreater(hist_data["count"], 0)

        # Save favorite item
        fav_res = self.client.post("/api/history/saved-items", json={
            "name": "22K Royal Emerald Choker",
            "category": "Necklace",
            "estimated_price": 85000,
            "platform": "Tanishq",
            "link": "https://www.tanishq.co.in/shop?q=choker",
            "tag": "Best Match"
        })
        self.assertEqual(fav_res.status_code, 201)
        item_id = fav_res.get_json()["item_id"]

        # List saved favorites
        favs_res = self.client.get("/api/history/saved-items")
        self.assertEqual(favs_res.status_code, 200)
        self.assertGreater(favs_res.get_json()["count"], 0)

        # Remove saved favorite
        del_res = self.client.delete(f"/api/history/saved-items/{item_id}")
        self.assertEqual(del_res.status_code, 200)
        print("[PASS] History & Saved Favorites Passed")

    def test_07_legacy_endpoints(self):
        res1 = self.client.get("/generate-home?budget=200000")
        self.assertEqual(res1.status_code, 200)
        self.assertEqual(res1.get_json()["planner"], "home")

        res2 = self.client.get("/generate-party?budget=50000&guests=30")
        self.assertEqual(res2.status_code, 200)
        self.assertEqual(res2.get_json()["planner"], "party")

        res3 = self.client.get("/generate-jewelry?budget=100000")
        self.assertEqual(res3.status_code, 200)
        self.assertEqual(res3.get_json()["planner"], "jewelry")
        print("[PASS] Backward Compatibility Legacy Endpoints Passed")

if __name__ == "__main__":
    unittest.main()
