# ⚡ Quick Start - React Frontend

Get the React frontend running in 3 minutes!

## 🚀 3-Step Setup

### Step 1: Install Dependencies

```bash
cd frontend-react
npm install
```

Or use alternative package managers:
```bash
yarn install
# or
pnpm install
```

**Wait time:** 1-2 minutes

---

### Step 2: Configure Backend Connection

Create `.env` file:

```bash
cp .env.example .env
```

The file should contain:
```env
VITE_BACKEND_URL=http://localhost:8000
```

**⚠️ Important:** Make sure backend is running first!

---

### Step 3: Start Development Server

```bash
npm run dev
```

**That's it!** 🎉

Browser will open automatically at `http://localhost:5173`

---

## ✅ Verify It's Working

1. **Map loads** - You should see an interactive map
2. **City selector** - Try changing cities (Kuala Lumpur, Jakarta, etc.)
3. **Metrics update** - Environmental data cards should show values
4. **AI Chat works** - Send a message to the AI assistant
5. **Backend connected** - Check browser console for successful API calls

---

## 🐛 Quick Troubleshooting

### Backend Not Running?

Start it first:
```bash
cd ../backend
python main.py
```

### Port 5173 Already in Use?

```bash
npm run dev -- --port 5174
```

### Module Not Found?

```bash
rm -rf node_modules package-lock.json
npm install
```

### Map Not Showing?

- Refresh the page
- Check browser console for errors
- Verify Leaflet CSS loaded

---

## 🎯 Quick Test Checklist

- [ ] Backend running on port 8000
- [ ] Frontend running on port 5173
- [ ] Map displays correctly
- [ ] Can select different cities
- [ ] Metrics cards show data
- [ ] AI chat responds (if backend configured)
- [ ] No console errors

---

## 📚 Next Steps

1. **Explore the UI** - Try all features
2. **Check AI Chat** - Ask about urban planning
3. **Test Scenarios** - Run planning simulations
4. **Select Areas** - Use area selection tool (UI ready)
5. **Read README** - Full documentation in `README.md`

---

## 🔥 Pro Tips

- **Hot Reload**: Edit files and see instant changes
- **React DevTools**: Install browser extension for debugging
- **Console Logs**: Check browser console for API calls
- **Tailwind**: Use utility classes for quick styling

---

## 📞 Need Help?

- Check `README.md` for detailed docs
- Backend docs: `../backend/README.md`
- Backend API: `http://localhost:8000/docs`

---

**Time to Complete:** 3-5 minutes ⏱️

**You're ready to demo!** 🚀

