# 🚀 EchoSphere Development Commands

## **Complete Setup & Development Commands for Cursor IDE**

### **📋 Prerequisites Check**
```bash
# Check if you're in the correct directory
pwd
# Should show: /home/zakyasshii/Documents/echosphere

# Check if backend and frontend-react directories exist
ls -la
```

---

## **🔧 Backend Setup Commands**

### **1. Install Dependencies**
```bash
cd backend
pip install fastapi==0.118.0 uvicorn[standard]==0.27.0 pydantic==2.5.0 pydantic-settings==2.1.0 httpx==0.26.0 openai==1.12.0 python-dotenv==1.0.0
```

### **2. Create Environment File**
```bash
# Create .env file in backend directory
cat > .env << EOF
# OpenRouter API Key (for DeepSeek AI)
OPENROUTER_API_KEY=your_openrouter_key_here

# NASA API Key
NASA_API_KEY=your_nasa_key_here

# Optional
SITE_URL=http://localhost:5173
SITE_NAME=Echosphere Urban Resilience
EOF
```

### **3. Start Backend Server**
```bash
cd backend
python main.py
```

**Expected Output:**
```
🚀 Echosphere Backend Starting...
📍 Backend URL: http://localhost:8000
🌐 Frontend URL: http://127.0.0.1:5500
🤖 AI Model: deepseek/deepseek-chat-v3.1:free
🛰️  NASA API: Configured
```

---

## **🎨 Frontend Setup Commands**

### **1. Install Dependencies**
```bash
cd frontend-react
npm install react-router-dom@6
```

### **2. Start Frontend Development Server**
```bash
cd frontend-react
npm run dev
```

**Expected Output:**
```
  VITE v5.1.0  ready in 1234 ms

  ➜  Local:   http://localhost:5173/
  ➜  Network: use --host to expose
```

---

## **🧪 Testing Commands**

### **1. Test Backend API**
```bash
# Test health endpoint
curl http://localhost:8000/api/health

# Test reports endpoint
curl -X POST http://localhost:8000/api/reports/submit \
  -H "Content-Type: application/json" \
  -d '{
    "reporter_name": "Test User",
    "reporter_email": "test@example.com",
    "report_type": "environmental_issue",
    "title": "Test Report",
    "description": "This is a test report",
    "severity": "medium",
    "category": "heat_island",
    "location": {
      "address": "Test Location"
    },
    "date_observed": "2024-01-01T00:00:00Z"
  }'
```

### **2. Test Frontend Navigation**
1. Open http://localhost:5173
2. Click "Urban Planner Dashboard" → Should navigate to dashboard
3. Click "Reporting Portal" → Should navigate to reporting form
4. Click "EchoSphere" logo → Should return to main menu

---

## **🔍 Development Workflow Commands**

### **1. Start Both Servers (Terminal 1)**
```bash
cd backend
python main.py
```

### **2. Start Frontend (Terminal 2)**
```bash
cd frontend-react
npm run dev
```

### **3. View API Documentation**
```bash
# Open in browser
open http://localhost:8000/docs
```

---

## **📁 File Structure Verification**
```bash
# Verify all new files were created
find . -name "*.jsx" -o -name "*.py" | grep -E "(MainMenu|ReportingPortal|Dashboard|reports)" | sort

# Expected output:
# ./frontend-react/src/components/Dashboard.jsx
# ./frontend-react/src/components/MainMenu.jsx
# ./frontend-react/src/components/ReportingPortal.jsx
# ./backend/app/routers/reports.py
# ./backend/app/services/report_service.py
```

---

## **🎯 Feature Testing Checklist**

### **Main Menu Features:**
- [ ] EchoSphere logo displays correctly
- [ ] "Urban Planner Dashboard" button works
- [ ] "Reporting Portal" button works
- [ ] Visual design is consistent
- [ ] Responsive on mobile

### **Reporting Portal Features:**
- [ ] Form validation works
- [ ] Image upload functionality
- [ ] API submission works
- [ ] Success page displays
- [ ] Back to main menu works

### **Dashboard Features:**
- [ ] Existing dashboard loads correctly
- [ ] Back button returns to main menu
- [ ] All existing features still work
- [ ] Header shows EchoSphere branding

---

## **🚀 Production Deployment Commands**

### **Build Frontend**
```bash
cd frontend-react
npm run build
```

### **Check Build Output**
```bash
ls -la dist/
```

---

## **🐛 Troubleshooting Commands**

### **Backend Issues:**
```bash
# Check if port 8000 is in use
lsof -i :8000

# Kill process on port 8000
kill -9 $(lsof -t -i:8000)

# Check Python dependencies
pip list | grep -E "(fastapi|uvicorn|pydantic)"
```

### **Frontend Issues:**
```bash
# Check if port 5173 is in use
lsof -i :5173

# Clear npm cache
npm cache clean --force

# Reinstall dependencies
rm -rf node_modules package-lock.json
npm install
```

### **API Connection Issues:**
```bash
# Test backend connectivity
curl -I http://localhost:8000

# Check CORS settings
curl -H "Origin: http://localhost:5173" http://localhost:8000/api/health
```

---

## **📊 Performance Monitoring**

### **Backend Performance:**
```bash
# Monitor API response times
curl -w "@curl-format.txt" -o /dev/null -s http://localhost:8000/api/health

# Create curl-format.txt
cat > curl-format.txt << EOF
     time_namelookup:  %{time_namelookup}\n
        time_connect:  %{time_connect}\n
     time_appconnect:  %{time_appconnect}\n
    time_pretransfer:  %{time_pretransfer}\n
       time_redirect:  %{time_redirect}\n
  time_starttransfer:  %{time_starttransfer}\n
                     ----------\n
          time_total:  %{time_total}\n
EOF
```

---

## **🎨 UI/UX Validation Commands**

### **Color Theme Consistency:**
```bash
# Search for color classes in components
grep -r "from-primary\|to-primary\|bg-primary\|text-primary" frontend-react/src/components/

# Check for consistent gradient usage
grep -r "bg-gradient-to" frontend-react/src/components/
```

### **Responsive Design Check:**
```bash
# Test in different viewport sizes
# Use browser dev tools to test:
# - Mobile (375px)
# - Tablet (768px)  
# - Desktop (1024px)
```

---

## **✅ Final Validation Commands**

### **1. Complete System Test**
```bash
# Test all endpoints
curl http://localhost:8000/api/health
curl http://localhost:8000/api/reports/statistics
curl http://localhost:8000/api/reports/recent
```

### **2. Frontend Navigation Test**
```bash
# Open browser and test:
# 1. Main menu loads
# 2. Dashboard navigation works
# 3. Reporting portal navigation works
# 4. Form submission works
# 5. Back navigation works
```

### **3. API Integration Test**
```bash
# Test report submission
curl -X POST http://localhost:8000/api/reports/submit \
  -H "Content-Type: application/json" \
  -d @test-report.json

# Create test-report.json
cat > test-report.json << EOF
{
  "reporter_name": "Test User",
  "reporter_email": "test@example.com",
  "report_type": "environmental_issue",
  "title": "Heat Island in Downtown",
  "description": "High temperatures observed in commercial district",
  "severity": "high",
  "category": "heat_island",
  "location": {
    "address": "Downtown Sibu, Sarawak",
    "latitude": 2.3,
    "longitude": 111.82
  },
  "date_observed": "2024-01-15T10:00:00Z",
  "contact_permission": true,
  "follow_up": true
}
EOF
```

---

## **🎉 Success Criteria**

✅ **Main Menu:**
- Professional design with EchoSphere branding
- Two functional buttons (Dashboard & Reporting)
- Consistent color theme
- Responsive design

✅ **Reporting Portal:**
- Complete form with validation
- Image upload functionality
- API integration working
- Success/error handling
- Back navigation

✅ **Dashboard Integration:**
- Existing dashboard preserved
- New header with back button
- EchoSphere branding consistent
- All features functional

✅ **Backend API:**
- Reports endpoint working
- Data validation working
- Error handling implemented
- Documentation available

✅ **Overall System:**
- Smooth navigation between pages
- Consistent UI/UX design
- Professional appearance
- Ready for demo/presentation

---

**🎯 Ready for NASA Space Apps Challenge 2025 Demo! 🚀**

