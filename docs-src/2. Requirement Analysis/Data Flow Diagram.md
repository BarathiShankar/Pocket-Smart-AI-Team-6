# Data Flow Diagram

{{HEADER:2 Marks}}

## Level 0 - Context Diagram

```text
                 +----------------------+
                 |       User           |
                 | Browser / Mobile Web |
                 +----------+-----------+
                            |
                 budget + preferences
                            v
              +-----------------------------+
              |       PocketSmart AI        |
              | FastAPI planning service    |
              +---+------------+---------+--+
                  |            |         |
                  |            |         +------------------+
                  |            |                            |
                  v            v                            v
             [ SQLite ]   [ Gemini API ]             [ Store Search
             users +      recommendations              Links ]
             saved plans  text / image
```

## Level 1 - Main Data Flow

```text
(User)
   |
   +--> 1.0 Account / Session Validation ----> [D1 Users]
   |
   +--> 2.0 Validate Planner Input
   |          |
   |          +--> budget, quantities, event details, preferences
   |          |
   |          v
   |     3.0 Build AI Request ----------------> (Gemini API)
   |          ^                                      |
   |          | structured recommendation            |
   |          v                                      v
   |     4.0 Sanitize + Verify Budget --------> [D2 Recommendations]
   |          |
   |          +--> build shopping search links
   |          |
   v          v
(Result shown to user) <-------------------------+
   |
   +--> 5.0 Retrieve History -------------------> [D2 Recommendations]
```

| Symbol | Meaning |
|---|---|
| `(User)` | Person interacting with the application |
| `1.0–5.0` | Major application processes |
| `[D1]`, `[D2]` | SQLite data stores |
| `Gemini API` | External generative AI service |
| `Store Search Links` | External shopping/service destinations |

## Important Control Point

Gemini is not treated as the final calculator. Its response passes through the backend, where item prices and quantities are converted into totals and checked against the user's budget before the result is saved or displayed.
