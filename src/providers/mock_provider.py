import json
from .base_provider import LLMProvider, ProviderResponse

class MockProvider(LLMProvider):
    def generate(self, prompt: str) -> ProviderResponse:
        # Returns a hardcoded JSON so the UI doesn't break
        mock_data = {
            "quizTitle": "Fallback Quiz",
            "questions": [{"id": 1, "question": "Provider is at capacity. This is a sample.", "options": ["A", "B", "C", "D"], "answer": "A"}]
        }
        return ProviderResponse(content=json.dumps(mock_data), status="success")