# No. of Functional Features Included in the Solution

{{HEADER:5 Marks}}

## Functional Features

| S.No | Feature | Description | Component | Status |
|---|---|---|---|---|
| 1 | User registration | Validated account creation with hashed passwords | `auth.py`, `main.py` | Done |
| 2 | Login and logout | Signed session token, protected routes and logout handling | `auth.py` | Done |
| 3 | Home budget planner | Plans lights, fans, furniture, dining tables and selected rooms | `main.py`, `gemini_utils.py` | Done |
| 4 | Event budget planner | Allocates event spending among venue, food, decoration and entertainment | `main.py`, `gemini_utils.py` | Done |
| 5 | Jewelry planner | Uses occasion/preferences and optional outfit image for recommendations | `main.py`, `gemini_utils.py` | Done |
| 6 | Budget verification | Recomputes totals and removes items when the plan exceeds the limit | `gemini_utils.py` | Done |
| 7 | Shopping search links | Creates category-specific external search links | `gemini_utils.py` | Done |
| 8 | Saved history | Stores and retrieves a user's completed plans | `database.py` | Done |
| 9 | Dashboard | Shows planner entry points and recent activity | `dashboard.html` | Done |
| 10 | AI fallback | Provides a standard plan when Gemini is unavailable or unusable | `gemini_utils.py` | Done |
| 11 | Input and upload validation | Checks ranges, required fields, image types and image size | `models.py`, `main.py` | Done |
| 12 | Print-friendly result | Allows the generated plan to be saved through the browser's print function | `styles.css` | Done |

## Feature Summary

| Metric | Value |
|---|---:|
| Features documented | 12 |
| Core planning features | 5 |
| Supporting features | 7 |
| Automated test suite included | Yes |
| Direct payment integration | Not included |

## Feature Philosophy

The project focuses on the complete planning loop: **collect → generate → verify → save → continue shopping**. Features that would require retailer contracts, payment processing or live inventory are deliberately kept outside the current scope.
