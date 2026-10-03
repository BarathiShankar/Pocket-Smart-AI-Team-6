# Technology Stack

{{HEADER:2 Marks}}

| S.No | Architecture Component | Technology | Why It Fits the Project |
|---|---|---|---|
| 1 | Frontend | HTML5, CSS3, JavaScript, Jinja2 | Lightweight interface without a separate frontend build system; suitable for a small academic web application |
| 2 | Backend | Python, FastAPI, Uvicorn | Fast API development, request validation and clear route structure |
| 3 | Data Validation | Pydantic | Keeps budgets, quantities, guest counts and text inputs within defined limits |
| 4 | AI Layer | Google Gemini through `google-genai` | Generates structured recommendations and can process the optional jewelry image |
| 5 | Database | SQLite | Simple relational storage for users and saved plans with no separate database server |
| 6 | Authentication | bcrypt and JWT | Secure password hashing and signed session tokens |
| 7 | Image Handling | Pillow | Validates and prepares uploaded images before multimodal processing |
| 8 | Testing | pytest, custom load-test script | Functional checks and basic concurrency/performance evidence |
| 9 | Version Control | Git and GitHub | Supports five-member collaboration, history and code review |
| 10 | Deployment Support | Docker | Provides a repeatable environment for later cloud deployment |

## Technology Selection Principle

The team deliberately uses a small, understandable stack. The project does not train its own machine-learning model; Gemini provides the generative component while the application's backend remains responsible for validation, calculations, storage and access control.
