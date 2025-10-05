# Echosphere Frontend - React

Modern React frontend for Urban Resilience Digital Twin - NASA Space Apps Challenge

## 🚀 Tech Stack

- **React 18** - Modern UI framework with hooks
- **Vite** - Lightning-fast build tool with HMR
- **Tailwind CSS** - Utility-first CSS framework
- **Leaflet.js** - Interactive maps
- **React-Leaflet** - React components for Leaflet
- **Zustand** - Lightweight state management
- **Axios** - HTTP client for API calls
- **Recharts** - Data visualization library (ready for integration)
- **Lucide React** - Beautiful icon library

## 📦 Installation

### Prerequisites

- Node.js 18+ and npm/yarn/pnpm
- Backend server running on `http://localhost:8000`

### Setup Steps

1. **Install dependencies:**
   ```bash
   npm install
   # or
   yarn install
   # or
   pnpm install
   ```

2. **Create environment file:**
   ```bash
   cp .env.example .env
   ```

3. **Configure backend URL in `.env`:**
   ```env
   VITE_BACKEND_URL=http://localhost:8000
   ```

4. **Start development server:**
   ```bash
   npm run dev
   # or
   yarn dev
   # or
   pnpm dev
   ```

5. **Open in browser:**
   - The app will automatically open at `http://localhost:5173`
   - Or manually navigate to the URL shown in terminal

## 🏗️ Project Structure

```
frontend-react/
├── public/              # Static assets
├── src/
│   ├── components/      # React components
│   │   ├── Header.jsx
│   │   ├── LoadingOverlay.jsx
│   │   ├── Sidebar/     # Sidebar components
│   │   │   ├── index.jsx
│   │   │   ├── DataLayers.jsx
│   │   │   ├── PlanningScenarios.jsx
│   │   │   ├── CitySelector.jsx
│   │   │   ├── SearchLocation.jsx
│   │   │   ├── MapLayers.jsx
│   │   │   ├── AreaSelection.jsx
│   │   │   └── ElevationPanel.jsx
│   │   ├── Map/         # Map components
│   │   │   ├── MapContainer.jsx
│   │   │   └── StatusPanel.jsx
│   │   └── DataPanel/   # Data & AI components
│   │       ├── index.jsx
│   │       ├── MetricsGrid.jsx
│   │       └── AIAssistant.jsx
│   ├── services/        # API services
│   │   └── api.js       # Axios API client
│   ├── store/           # State management
│   │   └── useStore.js  # Zustand store
│   ├── utils/           # Utility functions
│   │   ├── toast.js     # Toast notifications
│   │   └── cn.js        # Class name merger
│   ├── App.jsx          # Main App component
│   ├── main.jsx         # Entry point
│   └── index.css        # Global styles
├── index.html           # HTML template
├── package.json         # Dependencies
├── vite.config.js       # Vite configuration
├── tailwind.config.js   # Tailwind configuration
├── postcss.config.js    # PostCSS configuration
└── .eslintrc.cjs        # ESLint configuration
```

## 🎨 Features

### ✅ Implemented

- **Interactive Map**
  - Multiple base layers (Satellite, Topographic, Terrain, Streets)
  - Real-time status overlay
  - City selector with preset locations
  - Location search with geocoding

- **Data Visualization**
  - Environmental metrics cards
  - Heat, Air Quality, Water Stress, Green Coverage indicators
  - Real-time trend indicators

- **AI Assistant**
  - Chat interface with conversation history
  - Context-aware responses
  - Pre-built question suggestions
  - Area analysis integration

- **Planning Scenarios**
  - Green Corridor simulation
  - Cool Roofs simulation
  - Flood Mitigation simulation

- **Area Selection** (UI ready)
  - Interactive area selection tool
  - Area statistics display
  - Analysis integration

- **State Management**
  - Zustand for global state
  - Efficient re-rendering
  - Persistent chat history

- **Responsive Design**
  - Mobile-friendly layout
  - Adaptive sidebar
  - Touch-optimized controls

### 🔄 Backend Integration

The frontend connects to the FastAPI backend for:

- **AI Chat** - `POST /api/chat`
- **Area Analysis** - `POST /api/analyze-area`
- **NASA Imagery** - `GET /api/nasa/imagery`
- **EONET Events** - `GET /api/nasa/eonet/events`
- **Climate Data** - `GET /api/nasa/power/climate`
- **Health Check** - `GET /api/health`

All API calls are handled through the Axios client in `src/services/api.js` with:
- Request/response interceptors
- Error handling
- Automatic JSON parsing
- Logging

## 🛠️ Development

### Available Scripts

```bash
# Start development server with HMR
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

### Environment Variables

Create a `.env` file:

```env
# Backend API URL (required)
VITE_BACKEND_URL=http://localhost:8000
```

### Adding New Features

1. **Components**: Add to `src/components/`
2. **State**: Extend `src/store/useStore.js`
3. **API**: Add endpoints to `src/services/api.js`
4. **Styles**: Use Tailwind utility classes

### Code Style

- Use functional components with hooks
- Follow React best practices
- Use Tailwind CSS for styling
- Keep components small and focused
- Extract reusable logic to custom hooks

## 🎯 Key Technologies

### React & Vite

- Fast HMR for instant feedback
- Efficient production builds
- Modern ES modules

### Tailwind CSS

- Utility-first approach
- Custom design system
- Responsive breakpoints
- Dark mode ready

### Zustand

- Minimal boilerplate
- No Context providers needed
- DevTools integration
- TypeScript support ready

### Leaflet

- Interactive maps
- Multiple layer support
- Marker and popup management
- Area selection tools

## 🔗 Backend Connection

### Prerequisites

1. **Backend must be running:**
   ```bash
   cd ../backend
   python main.py
   ```

2. **Backend should be accessible at:**
   - Default: `http://localhost:8000`
   - API Docs: `http://localhost:8000/docs`

3. **CORS must be configured in backend:**
   - Frontend URL should be in allowed origins
   - Default includes `http://localhost:5173`

### Testing Connection

1. Open browser console
2. Check for API request logs
3. Navigate to `http://localhost:8000/api/health` to verify backend
4. Test AI chat in the application

## 📱 Responsive Breakpoints

- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px
- **Large Desktop**: > 1200px

## 🎨 Color Palette

- **Primary**: Blue shades (Ocean, Sky)
- **Success**: Green shades (Nature, Growth)
- **Danger**: Red shades (Heat, Alerts)
- **Info**: Cyan shades (Air, Water)

## 🐛 Troubleshooting

### Port already in use

```bash
# Change port in vite.config.js or use:
npm run dev -- --port 5174
```

### Backend connection errors

- Check backend is running: `http://localhost:8000/api/health`
- Verify VITE_BACKEND_URL in `.env`
- Check browser console for CORS errors

### Map not rendering

- Check Leaflet CSS is imported in `index.html`
- Verify map container has height
- Check browser console for errors

### Build errors

```bash
# Clear node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

## 🚢 Production Build

```bash
# Build optimized production bundle
npm run build

# Preview production build locally
npm run preview
```

Build output will be in `dist/` directory.

### Deployment

The built app is a static SPA that can be deployed to:
- Vercel
- Netlify
- GitHub Pages
- AWS S3 + CloudFront
- Any static hosting service

**Important:** Update `VITE_BACKEND_URL` to production backend URL before building.

## 📄 License

Built for NASA Space Apps Challenge 🚀

---

## 🎓 Learning Resources

- [React Docs](https://react.dev)
- [Vite Guide](https://vitejs.dev)
- [Tailwind CSS](https://tailwindcss.com)
- [Zustand Docs](https://github.com/pmndrs/zustand)
- [Leaflet Tutorial](https://leafletjs.com/examples.html)
- [React-Leaflet](https://react-leaflet.js.org)

## 🤝 Contributing

This is a hackathon project. Feel free to fork and extend!

---

**Built with ❤️ for NASA Space Apps Challenge**

