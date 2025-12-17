# Function Safety Documentation
**Project:** COGNIFY

## 1. Safety Mechanisms
We use a **Direct Function Calling** architecture with the following safeguards:

### Authorization
| Function | Permission | Description |
|----------|------------|-------------|
| `generate_study_quiz` | **read** | Users can generate quizzes from their own uploads. |
| `save_quiz_result` | **write** | Saves results to user profile. |
| `admin_purge_data` | **admin** | Only available to system admins. |

*Implementation:* The `ProductionFunctionCaller` accepts a `user_id`. In a real deployment, we check `user_role` against a permissions table before execution.

### Cost Controls
- **Limit:** $0.50 per session.
- **Model:** Default to `gpt-4o-mini` (cheaper) instead of `gpt-4o`.
- **Handling:** If limit is reached, the system raises a `CostLimitException` and returns a partial result or friendly error to the student.

### Failure Scenarios
1.  **PDF too large (Token Limit):**
    *   *Detection:* OpenAI API returns 400 error.
    *   *Handling:* We truncate context to 15,000 characters in `execute_quiz_generation`.
2.  **API Timeout:**
    *   *Detection:* Request takes > 15 seconds.
    *   *Handling:* `tenacity` library retries 3 times with exponential backoff.
3.  **Circuit Breaker:**
    *   If `generate_study_quiz` fails 5 times consecutively, the breaker opens for 60 seconds to prevent wasting tokens on a broken backend.

## 2. Audit Logging
Logs are stored in `logs/function_audit.log` in JSON format:
```json
{"timestamp": 17028392, "user_id": "u_123", "tool": "quiz_gen", "status": "success", "cost": 0.001}
