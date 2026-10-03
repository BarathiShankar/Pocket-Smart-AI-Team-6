import math
from typing import Dict, Any, List

class BudgetService:
    """
    Financial and budget allocation service.
    Computes contingency buffers, category percentages, and validates balance calculations.
    """

    HOME_DEFAULT_RATIOS = {
        "Living Room Furniture": 0.25,
        "Bedroom & Wardrobe": 0.22,
        "Modular Kitchen & Storage": 0.20,
        "Lighting & Electricals": 0.10,
        "Wall Decor & Paint/Wallpaper": 0.08,
        "Flooring & Carpets": 0.05,
        "Contingency Reserve": 0.10
    }

    PARTY_DEFAULT_RATIOS = {
        "Venue & Infrastructure": 0.30,
        "Food & Catering Services": 0.35,
        "Decoration & Theme Setup": 0.12,
        "Photography & Video Coverage": 0.08,
        "Music & Entertainment": 0.05,
        "Logistics & Contingency": 0.10
    }

    JEWELRY_DEFAULT_RATIOS = {
        "Primary Centerpiece (Necklace/Set/Ring)": 0.60,
        "Secondary Complement (Earrings/Bangles/Bracelet)": 0.25,
        "Making Charges & Hallmark Certification": 0.10,
        "Insurance & Maintenance Reserve": 0.05
    }

    @classmethod
    def calculate_contingency(cls, total_budget: float, percentage: float = 10.0) -> float:
        """Calculate safety contingency reserve"""
        return round(total_budget * (percentage / 100.0), 2)

    @classmethod
    def generate_home_allocation(cls, budget: float, room_type: str = "3 BHK", style: str = "Modern Contemporary") -> Dict[str, Any]:
        total = float(budget)
        contingency = cls.calculate_contingency(total, 10.0)
        allocable = total - contingency
        
        allocations = [
            {
                "category": "Core Furniture (Sofa, Dining, Bed)",
                "allocated_amount": round(allocable * 0.36, 2),
                "percentage": 36,
                "notes": "Essential focal pieces with high durability rating."
            },
            {
                "category": "Modular Storage & Wardrobes",
                "allocated_amount": round(allocable * 0.24, 2),
                "percentage": 24,
                "notes": "Custom built-ins and optimized closet systems."
            },
            {
                "category": "Architectural & Ambient Lighting",
                "allocated_amount": round(allocable * 0.14, 2),
                "percentage": 14,
                "notes": "Warm LED profiles, chandeliers, and task lights."
            },
            {
                "category": "Soft Furnishings & Drapes",
                "allocated_amount": round(allocable * 0.12, 2),
                "percentage": 12,
                "notes": "Curtains, custom cushions, rugs, and upholstery."
            },
            {
                "category": "Wall Treatments, Art & Decor",
                "allocated_amount": round(allocable * 0.14, 2),
                "percentage": 14,
                "notes": "Textured finishes, artwork, mirrors, and indoor plants."
            }
        ]
        
        allocated_sum = sum(a["allocated_amount"] for a in allocations)
        
        return {
            "total_budget": total,
            "allocated_total": round(allocated_sum, 2),
            "estimated_spend": round(allocated_sum, 2),
            "remaining_unallocated": max(0, round(total - allocated_sum - contingency, 2)),
            "contingency_reserve": contingency,
            "contingency_percentage": 10.0,
            "allocations": allocations
        }

    @classmethod
    def generate_party_allocation(cls, budget: float, guests: int = 50, event_type: str = "Birthday Party") -> Dict[str, Any]:
        total = float(budget)
        contingency = cls.calculate_contingency(total, 8.0)
        allocable = total - contingency
        per_guest = round(total / max(1, guests), 2)
        
        allocations = [
            {
                "category": "Catering & Gourmet Menu",
                "allocated_amount": round(allocable * 0.42, 2),
                "percentage": 42,
                "notes": f"Estimated ₹{round((allocable * 0.42)/max(1, guests), 2)} per guest for multi-course meal and refreshments."
            },
            {
                "category": "Venue Rental & Hospitality",
                "allocated_amount": round(allocable * 0.28, 2),
                "percentage": 28,
                "notes": "Includes seating, stage layout, and banquet amenities."
            },
            {
                "category": "Theme Styling & Floral Decor",
                "allocated_amount": round(allocable * 0.15, 2),
                "percentage": 15,
                "notes": "Welcome arch, backdrop, photo-booth, and table centerpieces."
            },
            {
                "category": "Photography & Live Entertainment",
                "allocated_amount": round(allocable * 0.10, 2),
                "percentage": 10,
                "notes": "Pro event photographer and DJ / acoustic sound setup."
            },
            {
                "category": "Invitations, Favors & Coordination",
                "allocated_amount": round(allocable * 0.05, 2),
                "percentage": 5,
                "notes": "Digital invites, guest giveaways, and logistics."
            }
        ]
        
        allocated_sum = sum(a["allocated_amount"] for a in allocations)
        
        return {
            "total_budget": total,
            "guests_count": guests,
            "per_guest_budget": per_guest,
            "allocated_total": round(allocated_sum, 2),
            "estimated_spend": round(allocated_sum, 2),
            "remaining_unallocated": max(0, round(total - allocated_sum - contingency, 2)),
            "contingency_reserve": contingency,
            "contingency_percentage": 8.0,
            "allocations": allocations
        }

    @classmethod
    def generate_jewelry_allocation(cls, budget: float, category: str = "Bridal Set", metal: str = "22K Yellow Gold") -> Dict[str, Any]:
        total = float(budget)
        contingency = cls.calculate_contingency(total, 5.0)
        allocable = total - contingency
        
        allocations = [
            {
                "category": f"Primary {category} (Base Precious Metal)",
                "allocated_amount": round(allocable * 0.65, 2),
                "percentage": 65,
                "notes": f"Net precious metal weight in {metal} with certified hallmark."
            },
            {
                "category": "Gemstone / Diamond Studding",
                "allocated_amount": round(allocable * 0.18, 2),
                "percentage": 18,
                "notes": "Natural or lab-grown certification (IGI / SGL / GIA)."
            },
            {
                "category": "Artisan Craftsmanship / Making Charges",
                "allocated_amount": round(allocable * 0.12, 2),
                "percentage": 12,
                "notes": "Intricate filigree, kundan setting, or laser precision carving."
            },
            {
                "category": "Certification, Care & Assurance",
                "allocated_amount": round(allocable * 0.05, 2),
                "percentage": 5,
                "notes": "Hallmark registration, lifetime maintenance, and transit insurance."
            }
        ]
        
        allocated_sum = sum(a["allocated_amount"] for a in allocations)
        
        return {
            "total_budget": total,
            "jewelry_category": category,
            "metal_type": metal,
            "allocated_total": round(allocated_sum, 2),
            "estimated_spend": round(allocated_sum, 2),
            "remaining_unallocated": max(0, round(total - allocated_sum - contingency, 2)),
            "contingency_reserve": contingency,
            "contingency_percentage": 5.0,
            "allocations": allocations
        }
