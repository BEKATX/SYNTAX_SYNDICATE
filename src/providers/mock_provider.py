import json
try:
    from .base_provider import LLMProvider, ProviderResponse
except ImportError:
    from base_provider import LLMProvider, ProviderResponse

class MockProvider(LLMProvider):
    def generate(self, prompt: str) -> ProviderResponse:
        print(f"[MOCK] MockProvider activated (prompt length: {len(prompt)})")

        # Determine the type of request based on the prompt
        if "summary" in prompt.lower() or "summarize" in prompt.lower():
            mock_data = {
                "topic": "Study Material",
                "summary": "This is a mock summary. The AI service is currently unavailable or at capacity. This is sample content to demonstrate the summary feature."
            }
            print(f"[MOCK] Returning mock SUMMARY")
        elif "glossary" in prompt.lower() or "terms" in prompt.lower() or "extract" in prompt.lower():
            mock_data = {
                "topic": "Study Material",
                "terms": [
                    {"term": "Mock Term 1", "definition": "This is a sample definition for the first term."},
                    {"term": "Mock Term 2", "definition": "Another sample definition for the second term."},
                    {"term": "Mock Term 3", "definition": "A third sample term with its definition."}
                ]
            }
            print(f"[MOCK] Returning mock GLOSSARY with {len(mock_data['terms'])} terms")
        else:
            # Quiz generation (default)
            mock_data = {
                "topic": "Study Material",
                "questions": [
                    {
                        "id": 1,
                        "question": "This is a sample question (AI service at capacity)",
                        "options": ["Option A", "Option B", "Option C", "Option D"],
                        "answer": "A. Option A",
                        "explanation": "This is a mock quiz. The AI service is currently unavailable or at capacity."
                    },
                    {
                        "id": 2,
                        "question": "What is this mock provider demonstrating?",
                        "options": ["Fallback functionality", "Error handling", "Service resilience", "All of the above"],
                        "answer": "D. All of the above",
                        "explanation": "The mock provider ensures the application continues to work even when the AI service is unavailable."
                    }
                ]
            }
            print(f"[MOCK] Returning mock QUIZ with {len(mock_data['questions'])} questions")

        json_string = json.dumps(mock_data, indent=2)
        print(f"[MOCK] Returning {len(json_string)} chars of JSON")
        return ProviderResponse(content=json_string, status="success")