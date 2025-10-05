# ✅ Echosphere - Running Status

## Current Status
- ✅ Backend: Running on port **8000**
- ✅ Frontend: Running on port **5173**
- ✅ API Keys: Configured
- ✅ Dependencies: Installed

---

## Access URLs

| Service | URL |
|---------|-----|
| **Frontend** | http://localhost:5173 |
| **Backend API** | http://localhost:8000 |
| **API Docs** | http://localhost:8000/docs |

---

## Quick Commands

### Check Status
```bash
# Check if servers are running
ss -tlnp | grep -E ":(8000|5173)"
```

### View Logs
```bash
# Backend
tail -f /tmp/echosphere-backend.log

# Frontend (terminal where npm run dev is running)
```

### Stop Servers
```bash
pkill -f "python3 main.py"
pkill -f "npm run dev"
```

### Restart Servers
```bash
# Backend
./start-backend.sh

# Frontend
cd frontend-react && npm run dev
```

---

## Troubleshooting

**Page is blank?**
- Press `Ctrl + Shift + R` (hard refresh)
- Check browser console (F12) for errors

**Backend not responding?**
```bash
curl http://localhost:8000/api/health
```

**Port conflicts?**
- Change ports in respective config files
- Backend: Edit uvicorn port in `backend/main.py`
- Frontend: `npm run dev -- --port 5174`

---

For full documentation, see [README.md](README.md)
