# Brainstorming & Idea Prioritization

{{HEADER:3 Marks}}

## Step 1: Idea Listing

| S.No | Team Member | Idea / Suggestion | Category | Group |
|---|---|---|---|---|
| 1 | Gogul M | Start with a fixed budget and automatically divide it into useful spending categories | Budget planning | A |
| 2 | Sameer Ahamed T | Use Gemini to convert user preferences into practical item recommendations | Generative AI | B |
| 3 | Sabarirajan R | Provide a simple planner interface with clear totals and remaining budget | User experience | C |
| 4 | Barathi Shankar R | Add validation, fallback handling and automated testing so incorrect AI output is not shown directly | Reliability | D |
| 5 | Kawin M | Save completed plans so users can revisit previous decisions and compare them later | Storage & documentation | E |
| 6 | Team | Connect directly to retailer payment systems | Payments | F |

## Step 2: Idea Prioritization

| Group | Final Idea | Feasibility | User Value | Priority | Selected |
|---|---|---|---|---|---|
| A | Budget-first allocation for home, event and jewelry planning | High | High | Core | Yes |
| B | Gemini-generated recommendations from structured preferences | High | High | Core | Yes |
| C | Simple responsive planner and result views | High | High | Core | Yes |
| D | Server-side budget verification, fallback plans and automated tests | High | High | Core | Yes |
| E | User accounts and saved planning history | High | Medium | Supporting | Yes |
| F | Direct checkout/payment integration | Low for the current scope | Medium | Future | No |

## Selected Concept

The team selected a **budget-first planning assistant** rather than a general shopping search engine. The important design decision is that the budget is treated as a hard constraint and the AI is used to propose options, not to perform the final financial calculation.
