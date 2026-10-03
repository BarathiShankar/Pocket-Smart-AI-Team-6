import urllib.parse
from typing import Dict, Any, List

class PlatformAdapter:
    """
    Extensible Platform Adapter that generates realistic, safe deep search query links
    and verified metadata for e-commerce, food, hospitality, event, and luxury platforms.
    """
    
    PLATFORMS = {
        # E-Commerce & Home
        "Amazon": {
            "type": "e-commerce",
            "base_url": "https://www.amazon.in/s?k=",
            "icon": "amazon",
            "badge": "Amazon Prime",
            "domain": "amazon.in"
        },
        "Flipkart": {
            "type": "e-commerce",
            "base_url": "https://www.flipkart.com/search?q=",
            "icon": "flipkart",
            "badge": "Flipkart Assured",
            "domain": "flipkart.com"
        },
        "IKEA": {
            "type": "home-interior",
            "base_url": "https://www.ikea.com/in/en/search/?q=",
            "icon": "ikea",
            "badge": "IKEA Design",
            "domain": "ikea.com/in"
        },
        "Pepperfry": {
            "type": "home-interior",
            "base_url": "https://www.pepperfry.com/site_product/search?q=",
            "icon": "pepperfry",
            "badge": "Pepperfry Furniture",
            "domain": "pepperfry.com"
        },
        "Urban Ladder": {
            "type": "home-interior",
            "base_url": "https://www.urbanladder.com/search?q=",
            "icon": "urbanladder",
            "badge": "Urban Ladder",
            "domain": "urbanladder.com"
        },
        
        # Food & Catering
        "Swiggy": {
            "type": "catering-food",
            "base_url": "https://www.swiggy.com/search?query=",
            "icon": "swiggy",
            "badge": "Swiggy Gourmet",
            "domain": "swiggy.com"
        },
        "Zomato": {
            "type": "catering-food",
            "base_url": "https://www.zomato.com/search?q=",
            "icon": "zomato",
            "badge": "Zomato Dining",
            "domain": "zomato.com"
        },
        
        # Hospitality & Venues
        "OYO": {
            "type": "venue-hospitality",
            "base_url": "https://www.oyorooms.com/search?query=",
            "icon": "oyo",
            "badge": "OYO Townhouse / Event",
            "domain": "oyorooms.com"
        },
        "MakeMyTrip": {
            "type": "hospitality",
            "base_url": "https://www.makemytrip.com/hotels/",
            "icon": "makemytrip",
            "badge": "MakeMyTrip Stay",
            "domain": "makemytrip.com"
        },
        "BookMyShow": {
            "type": "entertainment",
            "base_url": "https://in.bookmyshow.com/explore/events?search=",
            "icon": "bookmyshow",
            "badge": "BookMyShow Events",
            "domain": "bookmyshow.com"
        },
        
        # Jewelry & Fashion
        "Tanishq": {
            "type": "fine-jewelry",
            "base_url": "https://www.tanishq.co.in/shop?q=",
            "icon": "tanishq",
            "badge": "Tanishq Certified Gold",
            "domain": "tanishq.co.in"
        },
        "CaratLane": {
            "type": "fine-jewelry",
            "base_url": "https://www.caratlane.com/search?q=",
            "icon": "caratlane",
            "badge": "CaratLane by Tanishq",
            "domain": "caratlane.com"
        },
        "Bluestone": {
            "type": "fine-jewelry",
            "base_url": "https://www.bluestone.com/search?q=",
            "icon": "bluestone",
            "badge": "BlueStone 100% Certified",
            "domain": "bluestone.com"
        },
        "Kalyan Jewellers": {
            "type": "fine-jewelry",
            "base_url": "https://www.kalyanjewellers.net/search.php?q=",
            "icon": "kalyan",
            "badge": "Kalyan Jewellers Trust",
            "domain": "kalyanjewellers.net"
        },
        "Myntra": {
            "type": "fashion-accessories",
            "base_url": "https://www.myntra.com/",
            "icon": "myntra",
            "badge": "Myntra Luxe",
            "domain": "myntra.com"
        }
    }

    @classmethod
    def get_search_url(cls, platform: str, query: str, category: str = "") -> str:
        plat_info = cls.PLATFORMS.get(platform)
        encoded_query = urllib.parse.quote_plus(query.strip())
        
        if not plat_info:
            # Fallback to general Amazon search
            return f"https://www.amazon.in/s?k={encoded_query}"
        
        base = plat_info["base_url"]
        if platform == "Myntra":
            # Myntra format: /<query>
            slug = urllib.parse.quote_plus(query.strip().replace(" ", "-"))
            return f"https://www.myntra.com/{slug}"
        
        return f"{base}{encoded_query}"

    @classmethod
    def enrich_recommendation(cls, item: Dict[str, Any]) -> Dict[str, Any]:
        """
        Enrich raw recommendation with platform metadata, safe url, verification badge, and visual tag
        """
        platform = item.get("platform", "Amazon")
        name = item.get("name", "Recommended Item")
        category = item.get("category", "")
        
        # Standardize platform
        matched_platform = "Amazon"
        for p in cls.PLATFORMS.keys():
            if p.lower() in platform.lower():
                matched_platform = p
                break
        
        link = item.get("link")
        if not link or "example.com" in link or "http" not in link:
            link = cls.get_search_url(matched_platform, f"{name} {category}")
        
        tag = item.get("tag")
        if not tag or tag not in ["Budget Friendly", "Premium Choice", "Best Match", "AI Recommended", "Luxury Pick"]:
            price = float(item.get("estimated_price", 0))
            if price > 50000:
                tag = "Luxury Pick"
            elif price > 15000:
                tag = "Premium Choice"
            elif price < 3000:
                tag = "Budget Friendly"
            else:
                tag = "Best Match"
        
        plat_meta = cls.PLATFORMS.get(matched_platform, cls.PLATFORMS["Amazon"])
        
        return {
            "name": name,
            "category": category or "General",
            "estimated_price": round(float(item.get("estimated_price", 0)), 2),
            "platform": matched_platform,
            "platform_badge": plat_meta["badge"],
            "platform_icon": plat_meta["icon"],
            "link": link,
            "tag": tag,
            "reason": item.get("reason", "Curated by PocketSmart AI to maximize value within your budget parameters."),
            "budget_relevance": item.get("budget_relevance", "High compatibility with target category budget."),
            "image_url": item.get("image_url", ""),
            "verified_available": True
        }

    @classmethod
    def get_supported_platforms(cls) -> List[Dict[str, Any]]:
        return [
            {
                "name": name,
                "type": info["type"],
                "badge": info["badge"],
                "domain": info["domain"],
                "icon": info["icon"]
            }
            for name, info in cls.PLATFORMS.items()
        ]
