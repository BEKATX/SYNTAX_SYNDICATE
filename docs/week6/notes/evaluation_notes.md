# Evaluation Notes
**Lab 6: Function Calling - Team SYNTAX_SYNDICATE**

### Functions Tested
1. `generate_study_quiz(topic, difficulty, num_questions)`
2. `extract_key_concepts(text_content, max_concepts)`

### Test Summary
| Test | Input | Expected | Got | Time (s) | Pass |
|------|--------|-----------|-----|-----------|------|
| 1 | Quiz: "Python", 3 Qs | QuizResult object | Valid Object | 0.05 | ✅ |
| 2 | Concepts: "AI Text" | ConceptList object | Valid Object | 0.04 | ✅ |
| 3 | Quiz: 20 Qs (Invalid) | ValidationError | ValidationError | 0.01 | ✅ |

### Observations
- Response time is negligible as we are currently using mock data inside the function logic.
- Pydantic models successfully caught the invalid input for Test 3 (num_questions > 10).
- Structure matches the JSON schema required for the frontend.

### Next Step
Connect `extract_key_concepts` to the actual PDF text extraction library (PyPDF2) in Week 7.
