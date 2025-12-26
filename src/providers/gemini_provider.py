from google import genai
try:
    from .base_provider import LLMProvider, ProviderResponse
except ImportError:
    from base_provider import LLMProvider, ProviderResponse

class GeminiProvider(LLMProvider):
    def __init__(self, api_key: str):
        self.client = genai.Client(api_key=api_key)
        self.model_id = 'gemini-2.0-flash-exp'  # Updated to newer model

    def generate(self, prompt: str) -> ProviderResponse:
        try:
            response = self.client.models.generate_content(model=self.model_id, contents=prompt)
            print(f"[OK] Gemini response received (length: {len(response.text)})")
            return ProviderResponse(content=response.text, status="success")
        except Exception as e:
            print(f"[ERROR] Gemini error: {e}")
            return ProviderResponse(content=str(e), status="error")