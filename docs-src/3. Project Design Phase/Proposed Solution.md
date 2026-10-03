# Project Initialization and Planning Phase

{{HEADER:5 Marks}}

## Project Proposal

**PocketSmart AI — AI-Assisted Goal-Based Budget Planner** is a web application that converts a user's spending limit and practical requirements into a structured plan for home setup, event preparation or occasion-based jewelry selection.

### Project Overview

| Field | Details |
|---|---|
| Objective | Help a user decide how to distribute a fixed budget before beginning detailed shopping |
| Scope | Home, Party and Jewelry planners; AI recommendations; server-side budget checking; accounts; history; optional outfit image; external search links |
| Out of Scope | Payments, direct retailer checkout, guaranteed live prices and training a custom AI model |

### Problem Statement

| Field | Details |
|---|---|
| Problem | Planning is often done item-by-item, so users discover that the total is too high only after spending time comparing products |
| Impact | This causes repeated searching, difficult trade-offs and uncertainty about which categories deserve more of the available budget |

### Proposed Solution

| Field | Details |
|---|---|
| Approach | Collect a total budget and planner-specific inputs, create a structured Gemini request, parse the response, recompute totals in the backend, trim over-budget items when necessary and present the verified plan |
| Key Features | Budget-first planning; three use cases; optional outfit-image analysis; category allocation; remaining-budget display; shopping search links; account/history; AI fallback; input validation |

### Resource Requirements

| Resource | Requirement |
|---|---|
| Hardware | Ordinary laptop/desktop with internet access; no local GPU required |
| Memory | 4 GB RAM or more recommended for development |
| Storage | About 1 GB free for source, dependencies, database and uploads |
| Software | Python 3.10+, Git, VS Code or another editor, browser |
| Main Libraries | FastAPI, Uvicorn, Pydantic, google-genai, Pillow, bcrypt, python-jose, python-dotenv, pytest |
| Data | Runtime user inputs, generated plans and uploaded images; no project-specific model training dataset |

## Design Principle

**AI proposes; application rules decide.** This keeps the generative component useful without allowing an AI-generated total to bypass the application's budget constraint.
