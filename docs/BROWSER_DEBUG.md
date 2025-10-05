# 🔍 Browser Debugging Guide

## The Issue

You're seeing an empty page at http://localhost:5173 even though the servers are running correctly.

## ✅ What We Confirmed

1. ✅ Frontend Vite server is running on port 5173
2. ✅ Backend API server is running on port 8000
3. ✅ HTML is being served correctly
4. ✅ React and all components are being compiled
5. ✅ .env file is configured with backend URL

## 🔍 How to Debug in Browser

### Step 1: Open Browser DevTools

1. Open http://localhost:5173 in your browser
2. Press **F12** or **Ctrl+Shift+I** (Linux) to open DevTools
3. Go to the **Console** tab

### Step 2: Check for JavaScript Errors

Look for any RED error messages in the console. Common issues:

**If you see CORS errors:**
- This means frontend can't connect to backend
- Backend is configured to allow localhost:5173
- Should not be an issue

**If you see "Module not found" or import errors:**
- Try: Clear browser cache (Ctrl+Shift+Delete)
- Or: Hard refresh (Ctrl+Shift+R)

**If you see "Failed to fetch" errors:**
- Backend might not be responding
- Check: `curl http://localhost:8000/api/health`

### Step 3: Check Network Tab

1. Go to **Network** tab in DevTools
2. Refresh the page (Ctrl+R)
3. Look for any failed requests (shown in RED)
4. Check if `/src/main.jsx` loads successfully

### Step 4: Try Different Browser

- Try opening in a different browser (Chrome, Firefox, Brave)
- Sometimes browser extensions can interfere

## 🛠️ Quick Fixes

### Fix 1: Hard Refresh
```
Press: Ctrl + Shift + R
```

### Fix 2: Clear Browser Cache
```
1. Press Ctrl + Shift + Delete
2. Select "Cached images and files"
3. Click "Clear data"
4. Reload page
```

### Fix 3: Disable Browser Extensions
```
1. Try in Incognito/Private mode
2. Or disable all extensions temporarily
```

### Fix 4: Restart Servers

Stop both servers:
```bash
pkill -f "python3 main.py"
pkill -f "npm run dev"
```

Start backend:
```bash
cd /home/zakyasshii/Documents/echosphere-main
./start-backend.sh > /tmp/echosphere-backend.log 2>&1 &
```

Start frontend:
```bash
cd /home/zakyasshii/Documents/echosphere-main/frontend-react
npm run dev
```

## 🔍 Common Error Messages

### "Uncaught SyntaxError"
- Clear cache and hard refresh

### "Cannot read property of undefined"
- Check console for which component is failing
- Might be a missing environment variable

### "Network Error" or "Failed to fetch"
- Backend not running or blocked
- Check: `curl http://localhost:8000`

### White/Blank screen with no errors
- React might be rendering but CSS not loading
- Check Network tab for CSS files
- Try disabling dark mode/browser theme

## 🎯 What to Look For

When you open DevTools Console, you should see:
- No RED error messages
- Possibly some info messages (blue/gray)
- Network requests to `/src/main.jsx`, `/src/App.jsx`, etc.

## 📸 What It Should Look Like

When working correctly, you should see:
1. **Header** - "Urban Resilience Digital Twin" at the top
2. **Sidebar** - Left panel with data layers and controls
3. **Map** - Center panel with interactive Leaflet map
4. **Data Panel** - Right panel with metrics and AI chat

## 🚨 If Still Not Working

### Check Logs

Backend log:
```bash
tail -f /tmp/echosphere-backend.log
```

Frontend log (in terminal):
```bash
cd /home/zakyasshii/Documents/echosphere-main/frontend-react
npm run dev
# Watch for any error messages
```

### Test API Directly

```bash
# Test backend
curl http://localhost:8000
curl http://localhost:8000/api/health

# Test frontend
curl http://localhost:5173
```

### Verify Servers Running

```bash
ss -tlnp | grep -E ":(8000|5173)"
```

Should show:
- Port 8000: python3 (backend)
- Port 5173: node/vite (frontend)

## 💡 Most Likely Issues

1. **Browser Cache** - Try Ctrl+Shift+R
2. **JavaScript Disabled** - Check browser settings
3. **Ad Blocker** - Try disabling temporarily
4. **Browser Extension** - Try incognito mode
5. **CORS Issue** - Check DevTools console

## 📞 Report Back

After checking DevTools console, report:
1. What error messages you see (if any)
2. What's in the Network tab
3. Which browser you're using
4. Screenshot of the console would help

---

**The servers are running correctly! The issue is in the browser rendering.**

