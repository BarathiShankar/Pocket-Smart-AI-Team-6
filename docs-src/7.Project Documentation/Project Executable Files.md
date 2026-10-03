# Project Executable Files

{{HEADER:3 Marks}}

## Submission Checklist

| S.No | Item | Status |
|---|---|---|
| 1 | Source code | Included |
| 2 | README and setup guide | Included |
| 3 | Python dependency files | Included |
| 4 | Database implementation | Included |
| 5 | `.env.example` configuration template | Included |
| 6 | Test cases and evidence | Included |
| 7 | Docker configuration | Included |
| 8 | Phase-wise documentation | Included |
| 9 | Hosted URL | Not currently hosted |
| 10 | Demo video | To be added after recording |

## Project Structure

```text
PocketSmart-AI/
|-- main.py
|-- gemini_utils.py
|-- auth.py
|-- models.py
|-- database.py
|-- config.py
|-- check_gemini.py
|-- requirements.txt
|-- requirements-dev.txt
|-- .env.example
|-- Dockerfile
|-- templates/
|-- static/
|-- tests/
|-- tools/
|-- docs-src/
|-- 1. Brainstorming & Ideation/
|-- 2. Requirement Analysis/
|-- 3. Project Design Phase/
|-- 4. Project Planning Phase/
|-- 5. Project Development Phase/
|-- 6.Project Testing/
|-- 7.Project Documentation/
|-- 8.Project Demonstration/
`-- README.md
```

## Run Instructions

1. Install Python 3.10 or newer.
2. Create a virtual environment.
3. Install dependencies with `pip install -r requirements.txt`.
4. Copy `.env.example` to `.env`.
5. Add the Gemini API key to the environment if live AI generation is required.
6. Start the server using `uvicorn main:app --reload`.
7. Open `http://localhost:8000`.
8. Run the test suite with the development requirements installed.

## Known Limitations

| Limitation | Current Handling |
|---|---|
| External prices are not guaranteed to be live | The UI clearly treats amounts as estimates |
| Shopping links open search pages | User confirms the actual product/service and price |
| SQLite is intended for a small deployment | PostgreSQL is a future production upgrade |
| Live Gemini latency varies | Offline fallback keeps the application usable when the API is unavailable |
