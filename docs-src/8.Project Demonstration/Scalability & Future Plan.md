# Scalability & Future Plan

{{HEADER:1 Mark}}

## Current Limitations

| S.No | Limitation | Effect |
|---|---|---|
| 1 | SQLite is used for the current deployment | Suitable for a small demo but not ideal for many simultaneous writes |
| 2 | Shopping destinations are search links | The application does not know live stock or final checkout price |
| 3 | Sessions are held in application memory | A multi-instance deployment would require shared session storage |
| 4 | Gemini response time depends on the external service | User-facing latency can vary with network and model availability |

## Scalability Plan

| Area | Current Approach | Future Upgrade |
|---|---|---|
| Users | Single application instance | Multiple workers behind a reverse proxy |
| Database | SQLite | PostgreSQL with connection pooling |
| Sessions | In-memory | Redis or another shared session store |
| AI requests | Synchronous work handled by the application | Async client, queueing and caching |
| Files | Local upload directory | Object storage with controlled access |
| Monitoring | Local test output | Central logging, metrics and error tracking |

## Future Roadmap

| Phase | Enhancement | Expected Benefit |
|---|---|---|
| Phase 2 | Live retailer/product data | More accurate price comparisons |
| Phase 3 | Cloud deployment and CI/CD | Easier public access and repeatable releases |
| Phase 4 | Editable plans and alternative scenarios | Users can compare different spending strategies |
| Phase 5 | More planning domains such as travel and education | Broader usefulness of the budget-first approach |

The roadmap keeps the original idea intact: expand the information available to the planner without removing the backend budget verification step.
