from google import genai
from .base_provider import LLMProvider, ProviderResponse

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-flash-latest'

    def generate(self, prompt: str) -> ProviderResponse:
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=prompt)
            return ProviderResponse(content=response.text, status="success")
        except Exception as e:
            return ProviderResponse(content=str(e), status="error")