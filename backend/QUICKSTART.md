# 🚀 Echosphere Backend - Quick Start Guide

## ⚡ 3-Step Setup (5 minutes)

### Step 1: Install Dependencies

**One-line command:**
```bash
pip install fastapi==0.109.0 uvicorn[standard]==0.27.0 pydantic==2.5.0 pydantic-settings==2.1.0 httpx==0.26.0 openai==1.12.0 python-dotenv==1.0.0
```

Or use requirements.txt:
```bash
pip install -r requirements.txt
```

---

### Step 2: Create `.env` File

Create a file named `.env` in the `backend/` folder:

```env
# OpenRouter API Key (for DeepSeek AI)
OPENROUTER_API_KEY=your_openrouter_key_here

# NASA API Key
NASA_API_KEY=your_nasa_key_here

# Optional
SITE_URL=http://localhost:5173
SITE_NAME=Echosphere Urban Resilience
```

**Replace with your actual API keys!**

---

### Step 3: Run the Server

**From the `backend/` directory:**
```bash
python main.py
```

Or with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

---

## ✅ Verify It's Working

1. **Open browser:** http://localhost:8000
   - Should see: `{"message": "Echosphere API - Urban Resilience Digital Twin"}`

2. **Check API docs:** http://localhost:8000/docs
   - Interactive Swagger UI with all endpoints

3. **Test health check:** http://localhost:8000/api/health
   - Should return status "ok"

---

## 🌐 Connect Frontend

Your frontend is already updated! Just:

1. **Open `frontend/index.html`** in your browser (use Live Server)
2. **Make sure backend is running** on port 8000
3. **Test the AI chat** - Ask it something!
4. **Select an area** on the map and click "Analyze Selected Area"

---

## 🐛 Troubleshooting

**Import errors?**
- Make sure you're in `backend/` directory when running
- Check: `python --version` (should be 3.8+)

**CORS errors in browser?**
- Backend should auto-allow localhost origins
- Check browser console for errors

**API key errors?**
- Verify `.env` file exists in `backend/` folder
- Check keys are correct (no quotes needed)

**Port already in use?**
- Change port: `uvicorn main:app --port 8001`
- Update frontend: `const BACKEND_URL = 'http://localhost:8001'`

---

## 📊 Available Endpoints

- **POST** `/api/chat` - AI chatbot
- **POST** `/api/analyze-area` - Comprehensive area analysis
- **GET** `/api/nasa/imagery` - NASA Earth imagery
- **GET** `/api/nasa/eonet/events` - Natural disasters
- **GET** `/api/nasa/power/climate` - Climate data
- **GET** `/api/health` - Health check

---

## 🎯 Demo Tips

1. **Select a city** (Kuala Lumpur, Jakarta, etc.)
2. **Use area selection tool** to draw a region
3. **Click "Analyze Selected Area"** - AI will analyze it!
4. **Chat with AI** about urban planning strategies
5. **Show disaster tracking** - EONET events are real!

---

## ⏰ You're Ready!

Backend setup should take **5-10 minutes max**.

Remaining 34 hours for:
- Testing & debugging
- Polish & features
- Demo preparation
- Presentation practice

Good luck with the hackathon! 🚀

