# FastAPI Integration Guide - Week 10/11

## Overview

This guide explains how the `ProductionFunctionCaller` class from `docs/week-9/src/ai/production_caller.py` has been integrated into the FastAPI main routes.

## Integration Details

### File Structure

```
SYNTAX_SYNDICATE/
├── src/
│   └── main.py                    # FastAPI application with integrated ProductionFunctionCaller
├── docs/
│   └── week-9/
│       └── src/
│           ├── ai/
│           │   └── production_caller.py  # AI Engine (Google Gemini Flash)
│           └── utils/
│               └── cost_tracking.py       # Cost tracking utilities
├── requirements.txt               # Python dependencies
└── .env                           # Environment variables (create from .env.example)
```

### Key Integration Points

1. **Import Path Handling**
   - The FastAPI app adds both `docs/week-9/src` and `docs/week-9` to `sys.path`
   - This ensures `ProductionFunctionCaller` can import `src.utils.cost_tracking` correctly
   - Path: `src/main.py` lines 15-20

2. **Environment Variable Configuration**
   - The app requires `GOOGLE_API_KEY` to be set in the environment
   - Loaded via `python-dotenv` from `.env` file
   - Production environments should set this as an environment variable
   - Path: `src/main.py` lines 22-24

3. **Singleton Pattern**
   - `ProductionFunctionCaller` is initialized once and reused across requests
   - Initialization happens lazily on first request
   - Path: `src/main.py` lines 40-52

## API Endpoints

### Health Check
```
GET /health
```
Returns the health status of the API and AI engine.

### Generate Quiz
```
POST /api/generate-quiz
```

**Request Body:**
```json
{
  "context_text": "The French Revolution began in 1789...",
  "topic": "History",
  "difficulty": "medium",
  "num_questions": 5
}
```

**Response:**
```json
{
  "success": true,
  "topic": "History",
  "questions": [
    {
      "id": 1,
      "question": "When did the French Revolution begin?",
      "options": ["1776", "1789", "1792", "1804"],
      "answer": "1789",
      "explanation": "The French Revolution began in 1789..."
    }
  ],
  "total": 5,
  "message": "Quiz generated successfully"
}
```

## Environment Setup

### Local Development

1. **Create `.env` file:**
   ```bash
   cp .env.example .env
   ```

2. **Add your Google API Key:**
   ```env
   GOOGLE_API_KEY=your_actual_api_key_here
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the server:**
   ```bash
   cd src
   python main.py
   # Or with uvicorn directly:
   uvicorn main:app --reload
   ```

### Production Environment

Ensure `GOOGLE_API_KEY` is set as an environment variable in your production environment:

**Render.com:**
- Go to your service settings
- Add environment variable: `GOOGLE_API_KEY` = `your_key`

**Docker:**
```dockerfile
ENV GOOGLE_API_KEY=your_key
```

**Kubernetes:**
```yaml
env:
  - name: GOOGLE_API_KEY
    valueFrom:
      secretKeyRef:
        name: cognify-secrets
        key: google-api-key
```

## Pathing Notes

As mentioned in the task, the imports use `docs/week-9` as the root path. When you move files to the final `src` folder structure, you may need to adjust:

1. **Current structure:** `docs/week-9/src/ai/production_caller.py`
2. **Future structure:** `src/ai/production_caller.py`

**Migration steps:**
- Update `sys.path.insert()` calls in `src/main.py`
- Change import from `from ai.production_caller import ProductionFunctionCaller`
- Update any relative imports in `production_caller.py` if needed

## Testing

### Test the Integration

```bash
# Start the server
cd src
python main.py

# In another terminal, test the endpoint
curl -X POST "http://localhost:8000/api/generate-quiz" \
  -H "Content-Type: application/json" \
  -d '{
    "context_text": "Python is a high-level programming language.",
    "topic": "Programming",
    "difficulty": "easy",
    "num_questions": 3
  }'
```

### Verify Environment Variable

```bash
# Check if GOOGLE_API_KEY is set
python -c "import os; from dotenv import load_dotenv; load_dotenv(); print('GOOGLE_API_KEY:', 'SET' if os.getenv('GOOGLE_API_KEY') else 'NOT SET')"
```

## Troubleshooting

### Import Errors
- **Error:** `Failed to import ProductionFunctionCaller`
- **Solution:** Verify `docs/week-9/src/ai/production_caller.py` exists and check the path in `src/main.py`

### Missing API Key
- **Error:** `GOOGLE_API_KEY not found in environment variables`
- **Solution:** Create `.env` file with `GOOGLE_API_KEY=your_key` or set it in production environment

### Cost Tracking Not Working
- The `cost_tracking` import may fail silently and use a dummy decorator
- This is expected if the path structure doesn't match exactly
- Quiz generation will still work, but cost tracking won't log

## Next Steps

1. ✅ ProductionFunctionCaller integrated into FastAPI routes
2. ✅ Environment variable handling configured
3. ✅ Pathing configured for `docs/week-9` structure
4. 🔄 Move files to final `src` folder structure (when ready)
5. 🔄 Update frontend to call `/api/generate-quiz` endpoint
6. 🔄 Add authentication/authorization if needed
7. 🔄 Configure CORS origins for production

