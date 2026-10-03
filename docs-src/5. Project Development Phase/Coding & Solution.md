# Coding & Solution

{{HEADER:5 Marks}}

## Solution Summary

| Field | Details |
|---|---|
| Repository | {{repo_url}} |
| Languages | Python, JavaScript, HTML, CSS |
| Frameworks | FastAPI, Uvicorn, Jinja2, Pydantic |
| AI Integration | Google Gemini through `google-genai` |
| Core Implementation | Budget-first planners, server-side calculation, shopping search links, accounts, history and fallback handling |
| Current Limitations | External links are search links; prices are estimates; no direct checkout or live retailer inventory |
| Run Method | Install dependencies, configure environment variables and start the FastAPI application with Uvicorn |

## Implementation Approach

1. **Validate the request** using Pydantic models before the AI call.
2. **Build a planner-specific prompt** from the validated budget and requirements.
3. **Request structured output** from Gemini.
4. **Sanitize the response** and convert prices/quantities into safe numeric values.
5. **Recalculate totals on the server** rather than trusting the model's arithmetic.
6. **Trim items when required** to keep the plan within the submitted limit.
7. **Attach search links** according to the recommendation category.
8. **Save the completed plan** to the user's history.

## Code Quality Checklist

| S.No | Criteria | Status |
|---|---|---|
| 1 | Clear module separation | Yes |
| 2 | Meaningful names and validation rules | Yes |
| 3 | Error handling around authentication, uploads and AI calls | Yes |
| 4 | Reusable budget and shopping-link helpers | Yes |
| 5 | Environment-based configuration for secrets | Yes |
| 6 | Automated tests included | Yes |

## Important Engineering Decision

The project does not allow an AI response to directly decide the final amount. The backend owns the calculation and budget constraint, which makes the application behaviour more predictable.
