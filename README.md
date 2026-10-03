# 💰 PocketSmart AI

## AI-Powered Personal Budget Planning Assistant

PocketSmart AI is an **AI-powered personal budgeting assistant** that helps users plan their spending based on their **available budget, expenses, requirements, priorities, and savings goals**.

Instead of performing only basic calculations, PocketSmart AI uses **Google Gemini AI** to understand financial requirements written in natural language and generate personalized budget recommendations.

---

## 🎯 Problem

Managing personal finances can be difficult because users have:

* Multiple expenses
* Different priorities
* Savings goals
* Unexpected requirements
* Limited monthly budgets

Traditional budgeting applications mainly calculate expenses, while users still need to decide how their money should be distributed.

---

## 💡 Solution

PocketSmart AI combines:

```text
User Input
    ↓
Budget Calculation
    ↓
Expense & Priority Analysis
    ↓
Google Gemini AI
    ↓
Personalized Recommendations
    ↓
Budget Dashboard
```

Users can simply describe their financial situation and receive an understandable spending plan.

---

## ⭐ Features

### 💰 Budget Planning

Calculate:

* Total budget
* Total expenses
* Savings
* Remaining balance
* Budget deficit

### 🤖 AI Recommendations

Uses Gemini AI to understand user requirements and generate personalized suggestions.

### 💬 Natural Language Input

Example:

```text
I have ₹40,000 this month.
Rent is ₹10,000.
Food is ₹6,000.
Travel is ₹3,000.
I want to save ₹8,000.
Can I spend ₹4,000 on entertainment?
```

### ⭐ Priority-Based Expenses

Expenses can be classified as:

```text
Essential
Important
Optional
```

### 🎯 Savings Goals

Users can specify a target such as:

```text
Monthly Savings = ₹10,000
```

### ⚠️ Overspending Detection

```text
Budget = ₹30,000
Expenses = ₹35,000

Deficit = ₹5,000
```

The system identifies the budget problem and generates recommendations.

---

# 🧠 AI Workflow

```text
Natural Language Input
        ↓
Requirement Extraction
        ↓
Expense Identification
        ↓
Priority Analysis
        ↓
Budget Calculation
        ↓
Gemini AI
        ↓
Recommendation Generation
        ↓
Dashboard
```

---

# 🏗️ Architecture

```text
              USER
                │
                ▼
        ┌───────────────┐
        │   FRONTEND    │
        │ React + JS    │
        └───────┬───────┘
                │
             JSON/API
                │
                ▼
        ┌───────────────┐
        │    BACKEND    │
        │ Python/FastAPI│
        └───────┬───────┘
                │
       ┌────────┴─────────┐
       │                  │
       ▼                  ▼
┌──────────────┐   ┌──────────────┐
│    Budget    │   │ Gemini AI    │
│   Calculator │   │   Service    │
└──────┬───────┘   └──────┬───────┘
       │                  │
       └────────┬─────────┘
                ▼
       ┌─────────────────┐
       │ Recommendation  │
       │     Engine      │
       └────────┬────────┘
                ▼
          Dashboard
```

---

# 🛠️ Technology Stack

## Frontend

```text
React.js
JavaScript
HTML5
CSS3
Vite
```

## Backend

```text
Python
FastAPI
Pydantic
Uvicorn
```

## AI

```text
Google Gemini API
```

## Development

```text
Git
GitHub
VS Code
npm
Python
```

---

# 📂 Project Structure

```text
PocketSmart-AI/
│
├── backend/
│   ├── main.py
│   ├── requirements.txt
│   ├── .env
│   ├── routes/
│   ├── services/
│   ├── models/
│   └── utils/
│
├── frontend/
│   ├── package.json
│   ├── public/
│   └── src/
│       ├── components/
│       ├── services/
│       ├── styles/
│       ├── App.jsx
│       └── main.jsx
│
├── README.md
└── .gitignore
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/BarathiShankar/Pocket_Smart_AI
cd PocketSmart-AI
```

---

## 2. Backend Setup

```bash
cd backend
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Linux/macOS

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

# 🔐 Environment Variables

Create:

```text
backend/.env
```

Add:

```env
GEMINI_API_KEY=your_gemini_api_key
```

Never upload `.env` to GitHub.

Add:

```gitignore
.env
venv/
__pycache__/
node_modules/
dist/
```

---

# ▶️ Run Backend

```bash
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

API documentation:

```text
http://127.0.0.1:8000/docs
```

---

# ⚛️ Run Frontend

Open another terminal:

```bash
cd frontend
npm install
npm run dev
```

Open the local URL provided by Vite.

---

# 🔌 API

## Health Check

```http
GET /api/health
```

## Budget Analysis

```http
POST /api/budget/analyze
```

Example request:

```json
{
  "budget": 50000,
  "savings_goal": 10000,
  "expenses": [
    {
      "category": "Rent",
      "amount": 12000
    },
    {
      "category": "Food",
      "amount": 6000
    },
    {
      "category": "Transport",
      "amount": 3000
    }
  ],
  "requirements": "I want to spend some money on entertainment."
}
```

Example response:

```json
{
  "budget": 50000,
  "total_expenses": 21000,
  "savings_goal": 10000,
  "remaining_budget": 19000,
  "status": "within_budget",
  "recommendations": [
    "Maintain your savings target.",
    "Reserve part of the remaining budget for emergencies."
  ]
}
```

---

# 🧮 Budget Logic

```text
Total Expenses =
Expense 1 + Expense 2 + Expense 3 + ...

Total Allocation =
Total Expenses + Savings

Remaining Budget =
Available Budget - Total Allocation
```

Example:

```text
Budget        = ₹50,000
Expenses      = ₹21,000
Savings       = ₹10,000

Remaining     = ₹19,000
```

---

# 📊 Dashboard

The dashboard can display:

```text
┌─────────────────────────────────┐
│       POCKETSMART AI            │
├─────────────────────────────────┤
│ Budget       ₹50,000            │
│ Expenses     ₹21,000            │
│ Savings      ₹10,000            │
│ Remaining    ₹19,000            │
├─────────────────────────────────┤
│ Expense Categories              │
│                                 │
│ Rent             ₹12,000        │
│ Food              ₹6,000        │
│ Transport         ₹3,000        │
│                                 │
├─────────────────────────────────┤
│ 🤖 AI Recommendation             │
│ Your current budget is within   │
│ the planned allocation.         │
└─────────────────────────────────┘
```

---

# 🔐 Security

PocketSmart AI follows basic security practices:

* Gemini API key stored in environment variables
* API key never exposed to frontend
* Input validation
* Backend-based AI communication
* `.env` excluded from Git
* Sensitive configuration kept outside source code

Architecture:

```text
Frontend
   ↓
Backend
   ↓
Gemini API
```

---

# 🧪 Example Test Cases

### Normal Budget

```text
Budget = ₹50,000
Expenses = ₹30,000
Savings = ₹10,000

Result = ₹10,000 remaining
```

### Overspending

```text
Budget = ₹30,000
Expenses = ₹35,000

Result = ₹5,000 deficit
```

### Zero Budget

```text
Budget = ₹0

Result = Invalid / No available budget
```

---

# 🚀 Future Enhancements

Planned improvements can include:

* 📊 Expense tracking
* 📅 Monthly budget history
* 📈 Spending analytics
* 🔔 Budget alerts
* 🎯 Goal-based savings
* 🧾 Receipt scanning
* 📱 Mobile application
* 🔗 Financial data integrations
* 📉 Spending trend analysis
* 🌐 Multi-currency support

---

# ⚠️ Disclaimer

PocketSmart AI is an **AI-assisted budgeting application** intended for general budgeting and educational purposes.

AI-generated recommendations should not be treated as guaranteed financial, investment, tax, or professional advice.

Users should verify important financial decisions independently and consult a qualified professional when appropriate.

---

# 👨‍💻 Project

## PocketSmart AI

**AI-Powered Personal Budget Planning Assistant**

```text
React
+
Python
+
FastAPI
+
Google Gemini AI
=
PocketSmart AI
```

### Plan Smarter. Spend Better. Save with Confidence. 💰