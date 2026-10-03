# Communication

{{HEADER:1 Mark}}

## Communication Plan

| S.No | Communication Type | Frequency | Channel | Participants | Purpose |
|---|---|---|---|---|---|
| 1 | Short progress update | Daily during active development | Team chat | All members | Share completed work and blockers |
| 2 | Development review | As features are completed | GitHub | Relevant developers | Review changes before merging |
| 3 | AI/backend discussion | As needed | Team chat / Meet | Gogul M, Sameer Ahamed T | Resolve prompt, API and backend issues |
| 4 | UI review | As needed | Meet / screen share | Sabarirajan R + team | Check usability and consistency |
| 5 | Testing review | Before each final merge | GitHub + team chat | Barathi Shankar R + contributors | Confirm regression status |
| 6 | Documentation review | Before submission | Shared repository | Kawin M + all members | Keep phase documents consistent |

## Communication Challenges and Responses

| Challenge | Response |
|---|---|
| Multiple members editing the same area | Assign an owner to each module and merge through GitHub |
| AI output changing between requests | Keep output structured and validate it in the backend |
| Different local environments | Use `requirements.txt`, `.env.example` and clear run instructions |
| Last-minute documentation mismatch | Keep editable Markdown sources in `docs-src/` and regenerate PDFs together |
