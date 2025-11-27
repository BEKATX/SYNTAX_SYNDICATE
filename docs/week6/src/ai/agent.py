import os
import json
from openai import OpenAI
from dotenv import load_dotenv
from ..models.function_models import QuizRequest, ConceptRequest
from ..functions.tools import generate_study_quiz, extract_key_concepts

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Define Tools Schema for OpenAI
TOOLS_SCHEMA = [
    {
        "type": "function",
        "function": {
            "name": "generate_study_quiz",
            "description": "Generate a quiz from a topic to help the student study.",
            "parameters": QuizRequest.model_json_schema()
        }
    },
    {
        "type": "function",
        "function": {
            "name": "extract_key_concepts",
            "description": "Extract key terms and definitions from text to create flashcards.",
            "parameters": ConceptRequest.model_json_schema()
        }
    }
]

def run_cognify_agent(user_query: str):
    """
    Simulates a turn of the COGNIFY agent.
    """
    print(f"🤖 User: {user_query}")
    
    # 1. Call LLM to see if it wants to use a tool
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": user_query}],
        tools=TOOLS_SCHEMA,
        tool_choice="auto" 
    )
    
    message = response.choices[0].message

    # 2. Check if tool call is required
    if message.tool_calls:
        tool_call = message.tool_calls[0]
        fn_name = tool_call.function.name
        args = json.loads(tool_call.function.arguments)
        
        print(f"⚙️  AI Decided to call: {fn_name}")
        print(f"📋 Arguments: {args}")

        result = None
        
        # 3. Execute the appropriate function
        if fn_name == "generate_study_quiz":
            # Validate with Pydantic
            request_model = QuizRequest(**args)
            result = generate_study_quiz(request_model)
            
        elif fn_name == "extract_key_concepts":
            request_model = ConceptRequest(**args)
            result = extract_key_concepts(request_model)

        print(f"✅ Function Result: {result}")
        return result
    else:
        print("ℹ️  No function called. Regular response.")
        return message.content
