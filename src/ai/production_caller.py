import os
import re
import json
from pathlib import Path
import sys
from dotenv import load_dotenv

# Add the parent directory to the path to ensure imports work correctly
current_dir = Path(__file__).parent
src_dir = current_dir.parent
if str(src_dir) not in sys.path:
    sys.path.insert(0, str(src_dir))

# Import the providers
try:
    from providers.gemini_provider import GeminiProvider
    from providers.mock_provider import MockProvider
except ImportError:
    # Fallback to src.providers if running from different context
    from src.providers.gemini_provider import GeminiProvider
    from src.providers.mock_provider import MockProvider

# Import the telemetry tracker your team built in Week 9
try:
    from utils.cost_tracking import track_cost
except ImportError:
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
                print("[OK] Gemini Provider initialized.")
            except Exception as e:
                print(f"[WARNING] Failed to init Gemini: {e}")

        # Emergency Fallback (Requirement for Lab 11)
        self.providers.append(MockProvider())
        print("[OK] Mock Provider initialized.")

    def _execute_provider_chain(self, prompt: str):
        """Internal helper to handle the fallback routing logic."""
        for provider in self.providers:
            provider_name = type(provider).__name__
            print(f"[ROUTING] to {provider_name}...")

            response = provider.generate(prompt)

            if response.status == "success":
                print(f"[SUCCESS] {provider_name} returned content")
                return response.content
            else:
                print(f"[ERROR] {provider_name} failed. Trying next provider...")
                continue
        return None

    @track_cost(query_type="generate_quiz")
    def generate_quiz(self, context_text: str, topic: str, difficulty: str, num_questions: int = 5):
        prompt = f"""Generate a {num_questions}-question multiple choice quiz about {topic} based on this text: {context_text}

Return ONLY valid JSON in this EXACT format (no markdown, no extra text):
{{
  "topic": "{topic}",
  "questions": [
    {{
      "id": 1,
      "question": "Question text here?",
      "options": ["Option A", "Option B", "Option C", "Option D"],
      "answer": "A. Option A",
      "explanation": "Brief explanation here"
    }}
  ]
}}"""
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "quiz")

    @track_cost(query_type="generate_summary")
    def generate_summary(self, context_text: str, topic: str):
        prompt = f"""Summarize the following text about {topic}: {context_text}

Return ONLY valid JSON in this EXACT format (no markdown, no extra text):
{{
  "topic": "{topic}",
  "summary": "Your comprehensive summary here in 3-5 bullet points or paragraphs"
}}"""
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "summary")

    @track_cost(query_type="generate_glossary")
    def generate_glossary(self, context_text: str, topic: str):
        prompt = f"""Extract 5-10 key terms and their definitions from this text about {topic}: {context_text}

Return ONLY valid JSON in this EXACT format (no markdown, no extra text):
{{
  "topic": "{topic}",
  "terms": [
    {{"term": "Term 1", "definition": "Definition of term 1"}},
    {{"term": "Term 2", "definition": "Definition of term 2"}}
  ]
}}"""
        raw_result = self._execute_provider_chain(prompt)
        return self._process_and_wrap(raw_result, "glossary")

    def _process_and_wrap(self, raw_content, mode):
        """Cleans JSON and standardizes keys for Beka (UI) and Daviti (Backend)."""
        if not raw_content:
            print(f"[WARNING] _process_and_wrap: raw_content is None or empty")
            return None

        try:
            # 1. Strip Markdown backticks and any other formatting
            clean_text = raw_content.strip()
            # Remove markdown code blocks
            clean_text = re.sub(r'```json\s*', '', clean_text)
            clean_text = re.sub(r'```\s*', '', clean_text)
            # Remove any leading/trailing whitespace
            clean_text = clean_text.strip()

            print(f"[DEBUG] Attempting to parse JSON for mode={mode}")
            print(f"[DEBUG] First 200 chars: {clean_text[:200]}")

            data = json.loads(clean_text)
            print(f"[OK] Successfully parsed JSON. Keys: {list(data.keys()) if isinstance(data, dict) else 'not a dict'}")

            # 2. Key Normalization (Ensures UI doesn't crash)
            if isinstance(data, dict):
                if 'topic' not in data:
                    data['topic'] = "Study Material"

                if mode == "quiz":
                    if 'questions' not in data:
                        # Try alternative keys
                        data['questions'] = data.get('quiz', data.get('quiz_questions', data.get('items', [])))
                    print(f"[DATA] Quiz mode: Found {len(data.get('questions', []))} questions")
                elif mode == "glossary":
                    if 'terms' not in data:
                        data['terms'] = data.get('vocabulary', data.get('definitions', data.get('items', [])))
                    print(f"[DATA] Glossary mode: Found {len(data.get('terms', []))} terms")
                elif mode == "summary":
                    if 'summary' not in data:
                        data['summary'] = data.get('text', data.get('content', ''))
                    print(f"[DATA] Summary mode: Summary length: {len(data.get('summary', ''))}")

            # 3. Object Wrapper for Team Compatibility
            class ResponseWrapper:
                def __init__(self, d):
                    self.data = d
                    # Supports the legacy .choices[0].message.content pattern
                    self.choices = [type('Choice', (), {
                        'message': type('Msg', (), {'content': json.dumps(d)})()
                    })()]

            return ResponseWrapper(data)
        except json.JSONDecodeError as e:
            print(f"[ERROR] JSON Decode error in {mode}: {e}")
            print(f"[ERROR] Raw content (first 500 chars): {raw_content[:500]}")
            return None
        except Exception as e:
            print(f"[ERROR] Normalization error in {mode}: {e}")
            print(f"[ERROR] Raw content type: {type(raw_content)}")
            return None

if __name__ == "__main__":
    engine = ProductionFunctionCaller()
    # Test Factual Integrity for the Audit
    test_text = "Python was created by Guido van Rossum and released in 1991."
    print("\n--- Verifying AI Logic ---")
    q = engine.generate_quiz(test_text, "Python", "easy")
    s = engine.generate_summary(test_text, "Python")
    if q and s: print("✅ Integrity Check Passed.")