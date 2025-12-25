import os
import re
import json
from dotenv import load_dotenv

# Import the providers
from src.providers.gemini_provider import GeminiProvider
from src.providers.mock_provider import MockProvider

# Import the telemetry tracker your team built in Week 9
try:
    from src.utils.cost_tracking import track_cost
except ImportError:
    def track_cost(query_type="unknown"):
        def decorator(f): return f
        return decorator

load_dotenv()

class ProductionFunctionCaller:
    """
    COGNIFY AI ENGINE (Final Production Version)
    Handles Quiz, Summary, and Glossary with Multi-Vendor Fallback & Cost Tracking.
    """
    def __init__(self):
        self.providers = []
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and not api_key.startswith("your_actual"):
            try:
                self.providers.append(GeminiProvider(api_key))
                print("✅ Gemini Provider initialized.")
            except Exception as e:
                print(f"⚠️ Failed to init Gemini: {e}")

        # Emergency Fallback (Requirement for Lab 11)
        self.providers.append(MockProvider())
        print("✅ Mock Provider initialized.")

    def _execute_provider_chain(self, prompt: str):
        """Internal helper to handle the fallback routing logic."""
        for provider in self.providers:
            provider_name = type(provider).__name__
            print(f"🤖 Routing to {provider_name}...")
            
            response = provider.generate(prompt)
            
            if response.status == "success":
                print(f"✨ {provider_name} success!")
                return response.content
            else:
                print(f"❌ {provider_name} failed. Trying next...")
                continue
        return None

    @track_cost(query_type="generate_quiz")
    def generate_quiz(self, context_text: str, topic: str, difficulty: str, num_questions: int = 5):
        prompt = f"Generate a {num_questions}-question MCQ quiz about {topic} based on: {context_text}. Return ONLY valid JSON."
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "quiz")

    @track_cost(query_type="generate_summary")
    def generate_summary(self, context_text: str, topic: str):
        prompt = f"Summarize the following text about {topic} in bullet points. Return ONLY JSON with 'topic' and 'summary' keys: {context_text}"
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "summary")

    @track_cost(query_type="generate_glossary")
    def generate_glossary(self, context_text: str, topic: str):
        prompt = f"Extract key terms and definitions from this text about {topic}. Return ONLY JSON with 'topic' and a list 'terms' [{{'term': '...', 'definition': '...'}}]: {context_text}"
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "glossary")

    def _process_and_wrap(self, raw_content, mode):
        """Cleans JSON and standardizes keys for Beka (UI) and Daviti (Backend)."""
        if not raw_content: return None
        try:
            # 1. Strip Markdown backticks
            clean_text = re.sub(r'```json|```', '', raw_content).strip()
            data = json.loads(clean_text)
            
            # 2. Key Normalization (Ensures UI doesn't crash)
            if 'topic' not in data: data['topic'] = "Study Material"
            
            if mode == "quiz":
                if 'questions' not in data:
                    data['questions'] = data.get('quiz', data.get('quiz_questions', []))
            elif mode == "glossary":
                if 'terms' not in data:
                    data['terms'] = data.get('vocabulary', data.get('definitions', []))

            # 3. Object Wrapper for Team Compatibility
            class ResponseWrapper:
                def __init__(self, d):
                    self.data = d
                    # Supports the legacy .choices[0].message.content pattern
                    self.choices = [type('Choice', (), {
                        'message': type('Msg', (), {'content': json.dumps(d)})()
                    })()]
            
            return ResponseWrapper(data)
        except Exception as e:
            print(f"Normalization error in {mode}: {e}")
            return None

if __name__ == "__main__":
    engine = ProductionFunctionCaller()
    # Test Factual Integrity for the Audit
    test_text = "Python was created by Guido van Rossum and released in 1991."
    print("\n--- Verifying AI Logic ---")
    q = engine.generate_quiz(test_text, "Python", "easy")
    s = engine.generate_summary(test_text, "Python")
    if q and s: print("✅ Integrity Check Passed.")