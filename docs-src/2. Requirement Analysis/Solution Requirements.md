# Solution Requirements

{{HEADER:4 Marks}}

## Step 1: Functional Requirements

| S.No | Requirement Category | Requirement Description | Priority |
|---|---|---|---|
| 1 | Account Management | Register and sign in with validated credentials; passwords are stored as secure hashes | High |
| 2 | Access Control | Protected planners and history are available only to authenticated users, and a user can access only their own saved plans | High |
| 3 | Budget Input | Accept a total INR budget together with planner-specific quantities, guest count, occasion or preferences | High |
| 4 | AI Recommendation | Send validated planning information to Gemini and receive a structured recommendation rather than unrestricted text | High |
| 5 | Budget Verification | Recalculate item totals on the server and remove items if necessary so the displayed plan remains within the submitted budget | High |
| 6 | Shopping Support | Generate category-appropriate search links so the user can continue the purchase research on external platforms | Medium |
| 7 | History | Save completed plans and allow the owner to open the detailed breakdown later | Medium |
| 8 | Reliability | Provide a deterministic fallback plan when the AI service is unavailable or returns unusable data | High |
| 9 | Image Support | Accept an optional JPG, PNG or WEBP outfit image for the jewelry planner, with size and type validation | Medium |
| 10 | Reporting | Show planned spend, remaining amount, category allocation and recommendations in a readable result view | Medium |

## Step 2: Non-Functional Requirements

| S.No | NFR Category | Requirement | Acceptance Criteria |
|---|---|---|---|
| 1 | Performance | Application-side processing should remain lightweight before external AI latency | Repository load evidence shows sub-second average application overhead in offline mode |
| 2 | Security | Secrets must remain outside source code and protected routes must reject unauthenticated access | API key is read from environment; protected routes require a valid session |
| 3 | Reliability | AI failure must not leave a valid request without a usable response | Fallback plan is returned when Gemini is unavailable |
| 4 | Usability | A first-time user should understand the budget, inputs and result without technical knowledge | Responsive forms, clear labels, validation messages and visible totals |
| 5 | Maintainability | Planner-specific logic should be separated from authentication, storage and presentation | Dedicated modules for routes, models, AI service, authentication and database |
| 6 | Portability | The project should run on a normal development laptop | Python environment plus `requirements.txt`; optional Docker support |
