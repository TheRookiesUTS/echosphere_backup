# Echosphere Backend

FastAPI backend for Urban Resilience Digital Twin - NASA Space Apps Challenge

## Features

- 🤖 **AI Chat Assistant** - DeepSeek V3.1 via OpenRouter for urban planning consultation
- 📊 **Area Analysis** - Comprehensive environmental and resilience analysis
- 🛰️ **NASA API Proxy** - Secure access to NASA Earth observation data
- 💾 **Smart Caching** - In-memory caching to optimize API usage
- 🔒 **Secure** - API keys hidden in backend, never exposed to frontend

## Tech Stack

- **FastAPI** - Modern async Python web framework
- **httpx** - Async HTTP client for external APIs
- **OpenAI SDK** - For OpenRouter/DeepSeek integration
- **Pydantic** - Data validation and settings management

## Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Copy `.env.example` to `.env` and fill in your API keys:

```bash
cp .env.example .env
```

Edit `.env`:
```env
OPENROUTER_API_KEY=your_openrouter_key_here
NASA_API_KEY=your_nasa_key_here
```

### 3. Run the Server

```bash
python main.py
```

Or with uvicorn directly:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## API Endpoints

### AI Services

#### POST `/api/chat`
AI-powered urban planning chatbot
- Context-aware responses
- Chat history support
- Area-specific analysis

#### POST `/api/analyze-area`
Comprehensive area analysis
- Environmental risk assessment
- Actionable recommendations
- Priority levels

### NASA Services

#### GET `/api/nasa/imagery`
Earth imagery from NASA satellites
- Parameters: `lat`, `lng`, `dim`

#### GET `/api/nasa/eonet/events`
Natural disaster events (fires, floods, storms, etc.)
- Parameters: `status`, `limit`

#### GET `/api/nasa/power/climate`
Climate and weather data
- Parameters: `lat`, `lng`

### Utility

#### GET `/api/health`
Health check endpoint

## Project Structure

```
backend/
├── main.py                      # FastAPI app entry point
├── requirements.txt             # Python dependencies
├── .env                         # Environment variables (not in git)
├── .env.example                 # Template for environment variables
└── app/
    ├── config.py               # Configuration management
    ├── routers/
    │   ├── chat.py            # AI chat endpoints
    │   ├── nasa.py            # NASA proxy endpoints
    │   └── health.py          # Health check
    ├── services/
    │   ├── ai_service.py      # DeepSeek integration
    │   ├── nasa_service.py    # NASA API calls
    │   └── cache_service.py   # In-memory caching
    └── models/
        └── schemas.py          # Pydantic models
```

## Development

### Testing the API

Visit http://localhost:8000/docs for interactive API documentation (Swagger UI).

### Logs

The application logs all requests and responses. Check console output for:
- API calls
- Cache hits/misses
- Errors and warnings

## Integration with Frontend

Your frontend should call these endpoints instead of directly calling NASA or OpenRouter APIs.

Update `frontend/script.js`:
```javascript
const BACKEND_URL = 'http://localhost:8000';

// Example: Fetch NASA imagery
async function fetchNASAEarthImagery(lat, lng) {
    const response = await fetch(
        `${BACKEND_URL}/api/nasa/imagery?lat=${lat}&lng=${lng}&dim=0.1`
    );
    return response.json();
}

// Example: Chat with AI
async function sendAIMessage(message, areaData) {
    const response = await fetch(`${BACKEND_URL}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
            message: message,
            selectedAreaData: areaData,
            sessionId: 'default'
        })
    });
    return response.json();
}
```

## Notes

- Cache TTL is 1 hour by default (configurable in `config.py`)
- Chat history stores last 20 messages per session
- In-memory cache will reset on server restart
- Database integration coming from teammate (PostgreSQL + PostGIS)

## Troubleshooting

**Import errors**: Make sure you're in the `backend/` directory when running the server

**CORS errors**: Check that your frontend URL is in the CORS allowed origins in `main.py`

**API key errors**: Verify your `.env` file has correct API keys

**Rate limits**: NASA DEMO_KEY has limits (30/hour, 50/day). Get a personal key at https://api.nasa.gov

---

Built for NASA Space Apps Challenge 🚀

