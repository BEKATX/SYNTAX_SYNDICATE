import os
import re
import json
from dotenv import load_dotenv

# Import the providers
from src.providers.gemini_provider import GeminiProvider
from src.providers.mock_provider import MockProvider

# Load the .env file from the project root
load_dotenv()

class ProductionFunctionCaller:
    """
    COGNIFY AI ENGINE (Week 13 - Multi-Vendor Fallback)
    Handles the chain of LLM providers to ensure 99.9% uptime.
    """
    def __init__(self):
        self.providers = []
        
        # 1. Attempt to add Gemini (Primary)
        api_key = os.getenv("GOOGLE_API_KEY")
        if api_key and not api_key.startswith("your_actual"):
            try:
                self.providers.append(GeminiProvider(api_key))
                print("✅ Gemini Provider initialized.")
            except Exception as e:
                print(f"⚠️ Failed to init Gemini: {e}")
        else:
            print("⚠️ Skipping Gemini: No API Key found in .env")

        # 2. Always add MockProvider (Safety Fallback)
        # This ensures the app NEVER crashes even if all API keys fail.
        self.providers.append(MockProvider())
        print("✅ Mock Provider initialized (Emergency Fallback).")

    def generate_quiz(self, context_text: str, topic: str, difficulty: str, num_questions: int = 5):
        """
        Loops through providers until one succeeds.
        """
        prompt = f"""
        Generate a {num_questions}-question MCQ quiz about {topic} based on: {context_text}.
        Difficulty: {difficulty}.
        Return ONLY valid JSON.
        """
        
        for provider in self.providers:
            provider_name = type(provider).__name__
            print(f"🤖 Routing request to {provider_name}...")
            
            response = provider.generate(prompt)
            
            if response.status == "success":
                print(f"✨ {provider_name} succeeded!")
                return self._process_and_wrap(response.content)
            else:
                print(f"❌ {provider_name} failed: {response.content[:50]}...")
                continue # Try the next provider in the list
        
        return None

    def _process_and_wrap(self, raw_content):
        """
        Cleans JSON and ensures consistent keys for the UI.
        """
        try:
            clean_text = re.sub(r'```json|```', '', raw_content).strip()
            data = json.loads(clean_text)
            
            # NORMALIZATION: Ensure we have a standard 'topic' key
            # Check for common variations: quizTitle, quiz_title, title
            if 'topic' not in data:
                for alt in ['quizTitle', 'quiz_title', 'title']:
                    if alt in data:
                        data['topic'] = data[alt]
                        break
                if 'topic' not in data: data['topic'] = "Study Quiz"

            # Ensure we have a 'questions' key
            if 'questions' not in data:
                for alt in ['quiz', 'quiz_questions']:
                    if alt in data:
                        data['questions'] = data[alt]
                        break

            class ResponseWrapper:
                def __init__(self, d):
                    self.data = d
                    self.choices = [type('Choice', (), {
                        'message': type('Msg', (), {'content': json.dumps(d)})()
                    })()]
            
            return ResponseWrapper(data)
        except Exception as e:
            print(f"Parsing error: {e}")
            return None

if __name__ == "__main__":
    # Internal test loop
    engine = ProductionFunctionCaller()
    res = engine.generate_quiz("Cognify demo text.", "Demo", "easy")
    if res:
        print("\nFinal Output Check:")
        print(json.dumps(res.data, indent=2))