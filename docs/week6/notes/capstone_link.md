# Capstone Link
**Team:** SYNTAX_SYNDICATE
**Project:** COGNIFY (Study Helper)

### Function Reused from Lab 6
`generate_study_quiz(params: QuizRequest)`

### Integration Plan
- This function is core to our "Active Recall" feature.
- Currently, it resides in `src/functions/tools.py`.
- In Week 7, we will replace the mock data with a real call to OpenAI that feeds in the text from the uploaded PDF.
- **Next Step:** Implement the PDF-to-Text parser so we can feed real content into the `topic` field.
