# Solution Architecture

{{HEADER:5 Marks}}

## Architecture Diagram

```text
+--------------------------------------------------------------+
|                    PRESENTATION LAYER                        |
| HTML + CSS + JavaScript + Jinja2                             |
| Landing | Login | Register | Dashboard | 3 Planners | History|
+-----------------------------+--------------------------------+
                              |
                         HTTP / JSON
                              v
+--------------------------------------------------------------+
|                      APPLICATION LAYER                       |
| FastAPI + Uvicorn                                            |
| Authentication | Validation | Planner Routes | History       |
+-----------+----------------+------------------+---------------+
            |                |                  |
            v                v                  v
     +------------+   +---------------+   +------------------+
     | Auth       |   | AI Service    |   | Database Service |
     | bcrypt/JWT |   | Gemini +      |   | SQLite           |
     | sessions   |   | budget check  |   | users + plans    |
     +------------+   +-------+-------+   +------------------+
                              |
                              v
                    +-------------------+
                    | Google Gemini API |
                    | text / image      |
                    +-------------------+

External continuation:
Verified recommendations -> search links -> retailer/service websites
```

## Component Description

| Component | Responsibility | Technology |
|---|---|---|
| Presentation | Collects inputs and displays plans, totals and history | HTML/CSS/JS/Jinja2 |
| API Layer | Routes requests, handles sessions, validation and responses | FastAPI/Uvicorn |
| AI Service | Builds prompts, calls Gemini, parses structured output and supplies fallback data | Python + google-genai |
| Budget Engine | Recomputes category totals and keeps the result within the submitted budget | Python |
| Authentication | Password hashing, signed tokens and protected routes | bcrypt + JWT |
| Database | Stores users and generated recommendations | SQLite |
| Image Handling | Validates optional outfit uploads | Pillow |
| External Shopping | Creates search URLs rather than claiming live product availability | URL templates |

## Data Responsibility

The AI is responsible for **recommendation generation**. The application is responsible for **validation, calculation, access control and persistence**.
