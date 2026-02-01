# Mentra AI - Group Therapy Matching & Coordination

**AI-Orchestrated Group Therapy System with ChatGPT Integration**

A complete hackathon-ready solution combining a beautiful Lovable-designed frontend with a powerful Python Flask backend, integrated with OpenAI's ChatGPT for intelligent conversation analysis and group formation.

---

## 🚀 Quick Start (Two Commands!)

###Step 1: One-Time Setup
```bash
./setup.sh
```

### Step 2: Run Locally
```bash
./start.sh
```


That's it! The application will open in your browser at http://localhost:5173

---

## 📋 What This Does

### Phase 1: AI-Powered Discovery
- **Conversational Chatbot**: Natural conversation interface with empathetic AI responses
- **Real-time Analysis**: OpenAI ChatGPT analyzes user messages for:
  - Mental health concerns (anxiety, depression, stress, grief, etc.)
  - Sentiment detection (8 emotional states)
  - Urgency level assessment (normal, elevated, high, crisis)
  - Recommended therapy group type

### Phase 2: Intelligent Group Formation
- **AI-Optimized Matching**: Automatically categorizes users into compatible groups
- **Cohesion Scoring**: Measures group compatibility (0-100%)
- **Smart Algorithms**: Balance severity levels, concerns, and therapeutic needs

### Phase 3: Therapist Handoff
- **Comprehensive Briefings**: Auto-generated therapist briefing materials
- **Group Profiles**: Detailed member summaries and common themes
- **Clinical Insights**: AI-powered therapeutic recommendations

---

## 🛠️ Tech Stack

**Frontend:**
- React 18 + TypeScript
- Vite (fast build tool)
- Tailwind CSS + shadcn/ui components
- Lovable-designed UI (preserved exactly)

**Backend:**
- Python 3.8+ / Flask
- OpenAI ChatGPT API (gpt-4o-mini)
- CORS-enabled REST API

**AI Models:**
- Conversation Analyzer: gpt-4o-mini
- Group Matcher: gpt-4o-mini  
- Briefing Generator: gpt-4o

---

## 📦 Project Structure

```
mentra-hackathon/
├── frontend/                 # React + TypeScript frontend
│   ├── src/
│   │   ├── components/      # UI components (Lovable design)
│   │   │   ├── chat/       # Chat intake with AI
│   │   │   ├── groups/     # Group formation
│   │   │   ├── dashboard/  # System dashboard
│   │   │   ├── schedule/   # Scheduling (UI ready)
│   │   │   └── payment/    # Payment flow (UI ready)
│   │   ├── services/
│   │   │   └── api.ts      # Backend API client
│   │   └── contexts/       # React contexts
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                  # Flask backend with ChatGPT
│   ├── backend_api.py       # Main API server
│   ├── prompt_templates.py  # AI prompt library
│   ├── requirements.txt     # Python dependencies
│   └── .env                 # Environment variables
│
├── setup.sh                  # One-time setup script
├── start.sh                  # Start both servers
└── README.md                 # This file
```

---

## ⚙️ Setup Instructions

### Prerequisites
- **Python 3.8+** ([Download](https://www.python.org/))
- **Node.js 16+** ([Download](https://nodejs.org/))
- **OpenAI API Key** ([Get Here](https://platform.openai.com/api-keys))

### One-Time Setup

#### Option 1: Automated (Recommended)
```bash
# Make script executable
chmod +x setup.sh

# Run setup
./setup.sh
```

This script will:
1. Install Python dependencies
2. Install Node.js dependencies  
3. Create .env file
4. Verify installations

#### Option 2: Manual Setup

**Backend Setup:**
```bash
cd backend
pip install -r requirements.txt

# Create .env file
cp .env.template .env

# Edit .env and add your OpenAI API key
echo "OPENAI_API_KEY=sk-your-key-here" > .env
```

**Frontend Setup:**
```bash
cd frontend
npm install
```

### Get Your OpenAI API Key
1. Go to https://platform.openai.com/api-keys
2. Click "+ Create new secret key"
3. Copy the key (starts with `sk-`)
4. Add to `backend/.env` file

---

## 🎯 Running Locally

### Option 1: One-Click Start (Recommended)
```bash
./start.sh
```

This opens:
- Backend API: http://localhost:5000
- Frontend UI: http://localhost:5173 (opens automatically in browser)

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd backend
python backend_api.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend  
npm run dev
```

---

## 🧪 Testing the System

### 1. Test Chat Interface
1. Navigate to the Chat tab
2. Type: *"I've been feeling really anxious about work and can't sleep"*
3. Watch AI analyze the message
4. See detected concerns, sentiment, urgency level

### 2. Test Group Formation
1. Have multiple conversations in Chat
2. Go to Groups tab
3. Click "Form New Groups"
4. See AI-created therapy groups with reasoning

### 3. Test Dashboard
1. Go to Dashboard tab
2. View system statistics
3. See backend health status
4. Check AI model configuration

---

## 🔌 API Endpoints

All endpoints are available at `http://localhost:5000/api`

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check backend & OpenAI status |
| `/analyze-message` | POST | Analyze user message with AI |
| `/analyze-conversation` | POST | Analyze conversation thread |
| `/users` | POST | Create/update user profile |
| `/groups/form` | POST | Form therapy groups (AI/traditional) |
| `/groups` | GET | Get all groups |
| `/therapist/briefing/:id` | GET | Generate therapist briefing |
| `/stats` | GET | System statistics |
| `/config/model` | POST | Change AI model |
| `/config/prompt` | GET/POST | View/update system prompts |

### Example API Call
```bash
curl -X POST http://localhost:5000/api/analyze-message \
  -H "Content-Type: application/json" \
  -d '{
    "message": "I feel anxious",
    "user_id": "test_user",
    "use_ai": true
  }'
```

---

## 🎨 Features

### ✅ Implemented

**Chat Intake:**
- ✅ Natural conversation interface
- ✅ Real-time ChatGPT analysis
- ✅ Sentiment detection (8 states)
- ✅ Concern identification
- ✅ Urgency assessment
- ✅ Emoji emotional mirror
- ✅ Backend connection status

**Group Formation:**
- ✅ AI-optimized matching
- ✅ Cohesion scoring
- ✅ Member compatibility
- ✅ Group reasoning display
- ✅ Traditional fallback algorithm

**Dashboard:**
- ✅ System statistics
- ✅ Backend health monitoring
- ✅ AI model configuration
- ✅ Performance metrics

**Backend:**
- ✅ Flask REST API
- ✅ OpenAI ChatGPT integration
- ✅ Customizable prompts
- ✅ Multiple AI models
- ✅ CORS enabled
- ✅ Error handling

### 🚧 UI Ready (Can be activated)
- Scheduling system
- Payment flow
- Therapist briefing display

---

## 💰 Cost Estimates

### Using gpt-4o-mini (Default)
- Message analysis: ~$0.00014 each
- Group formation: ~$0.00025 each
- **Monthly (100 messages/day): ~$4-5**

### Using gpt-4o
- Message analysis: ~$0.002 each
- Briefing generation: ~$0.017 each
- **Monthly (100 messages/day): ~$60**

---

## 🐛 Troubleshooting

### Backend Not Connected
**Problem:** Yellow banner saying "Backend Disconnected"

**Solution:**
```bash
# Make sure backend is running
cd backend
python backend_api.py

# Should see: "Running on http://0.0.0.0:5000"
```

### OpenAI API Key Not Working
**Problem:** `openai_api: not_configured`

**Solution:**
```bash
# Check .env file exists
cat backend/.env

# Should contain:
OPENAI_API_KEY=sk-...

# Restart backend after adding key
```

### Port Already in Use
**Backend (5000):**
```bash
# Kill process on port 5000
lsof -ti:5000 | xargs kill -9
```

**Frontend (5173):**
```bash
# Kill process on port 5173
lsof -ti:5173 | xargs kill -9
```

### npm install fails
```bash
cd frontend
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

## 🏆 For Judges

### Demo Flow (5 minutes)
1. **Show Chat** (2 min)
   - Type anxiety message
   - Show AI analysis
   - Show sentiment detection

2. **Show Groups** (2 min)
   - Click "Form New Groups"
   - Show AI-optimized matches
   - Explain cohesion scores

3. **Show Dashboard** (1 min)
   - Backend health
   - System stats
   - AI configuration

### Key Features to Highlight
- ✅ Real OpenAI ChatGPT integration
- ✅ Beautiful, professional UI (Lovable design)
- ✅ Complete end-to-end workflow
- ✅ Production-ready architecture
- ✅ Easy to run locally
- ✅ Fully functional in 2 commands

---

## 🔐 Security & Privacy

- API keys stored in `.env` (never committed)
- CORS properly configured
- User data kept in-memory (demo mode)
- HTTPS recommended for production
- Input validation on all endpoints

---

## 📝 Environment Variables

Create `backend/.env`:
```bash
# OpenAI Configuration
OPENAI_API_KEY=sk-your-key-here

# Optional: Change default model
# OPENAI_MODEL=gpt-4o-mini
```

Create `frontend/.env.local` (optional):
```bash
# Backend API URL (default: http://localhost:5000/api)
VITE_API_URL=http://localhost:5000/api
```

---

## 🚀 Deployment

### Frontend (Vercel - Recommended)
```bash
cd frontend
npm run build
# Upload dist/ folder to Vercel
```

Or use Vercel CLI:
```bash
npm i -g vercel
vercel
```

### Backend (Railway - Recommended)
1. Push to GitHub
2. Connect Railway to repo
3. Add `OPENAI_API_KEY` environment variable
4. Deploy!

### Production Environment Variables
```bash
# Frontend
VITE_API_URL=https://your-backend.railway.app/api

# Backend
OPENAI_API_KEY=sk-...
FLASK_ENV=production
```

---

## 📚 Documentation

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)
- [Vite Documentation](https://vitejs.dev/)

---

## 🤝 Team

Built for the BIR Hackathon 2026 - Mentra Bounty Challenge

---

## 📄 License

MIT License - Open Source

---

## ✅ Pre-Demo Checklist

- [ ] Backend running on port 5000
- [ ] Frontend running on port 5173
- [ ] OpenAI API key configured
- [ ] Green "AI-Powered Analysis Active" banner visible
- [ ] Test message sent successfully
- [ ] Groups can be formed
- [ ] Dashboard shows statistics

---

**Ready to demo! Good luck! 🚀**
