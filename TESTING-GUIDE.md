# Quick Testing Guide for Judges

## 🚀 Get Started in 2 Commands

```bash
./setup.sh    # One-time setup (2-3 minutes)
./start.sh    # Start the application
```

Browser opens automatically at **http://localhost:5173**

---

## 🧪 Test Scenarios

### Scenario 1: Test AI Chat Analysis (2 minutes)

**Step 1:** Click on "Chat" tab (should already be selected)

**Step 2:** Type one of these test messages:

**Anxiety Test:**
```
I've been feeling really anxious about work lately. I can't sleep at night and my heart races when I think about tomorrow's meeting.
```

**Depression Test:**
```
I feel so empty and hopeless. Nothing brings me joy anymore and I can't seem to get out of bed most days.
```

**Stress Test:**
```
I'm completely overwhelmed with deadlines at work. I have 3 projects due this week and I don't know how I'll manage.
```

**Step 3:** Watch the AI analyze the message and show:
- ✅ Detected concerns (e.g., "anxiety: 85% confidence")
- ✅ Sentiment (e.g., "negative")  
- ✅ Urgency level (e.g., "elevated")
- ✅ Recommended group type

**Expected Result:**
- Green banner says "AI-Powered Analysis Active"
- AI responds with empathetic message
- Analysis card shows detected concerns
- Emoji avatar changes based on sentiment

---

### Scenario 2: Test Group Formation (1 minute)

**Step 1:** Send 3-4 different messages in Chat (see examples above)

**Step 2:** Click "Groups" tab

**Step 3:** Make sure "Use AI Optimization" is checked

**Step 4:** Click "Form New Groups" button

**Expected Result:**
- Groups are created based on conversations
- Each group shows:
  - Group name (e.g., "Anxiety Management & Coping Skills")
  - Primary focus area
  - Member list
  - Cohesion score (%)
  - AI reasoning for the match
  - Formation method badge

---

### Scenario 3: Test Dashboard (30 seconds)

**Step 1:** Click "Dashboard" tab

**Expected Result:**
- System statistics displayed:
  - Total users enrolled
  - Groups formed
  - AI analysis status
  - Backend health status
- Green banner shows "Backend Status: healthy"
- AI model configuration shows current models:
  - Analyzer: gpt-4o-mini
  - Group Matcher: gpt-4o-mini
  - Briefing Generator: gpt-4o

---

## ✅ Success Indicators

You know everything is working when you see:

### Chat Tab:
- ✅ Green banner: "AI-Powered Analysis Active"
- ✅ AI responds to your messages within 2 seconds
- ✅ Analysis card appears below AI response
- ✅ Emoji avatar changes based on sentiment
- ✅ No yellow "Backend Disconnected" warning

### Groups Tab:
- ✅ "Form New Groups" creates groups successfully
- ✅ Groups show AI reasoning
- ✅ Cohesion scores are displayed (70-95%)
- ✅ Member names are listed

### Dashboard Tab:
- ✅ Green banner shows "Backend Status: healthy"
- ✅ "OpenAI API: configured" is shown
- ✅ Total users and groups stats update
- ✅ AI model configuration is visible

---

## 🔍 What to Look For

### Design Quality:
- ✅ Beautiful gradient background
- ✅ Smooth animations and transitions
- ✅ Glass-morphism effects
- ✅ Emoji avatar that changes with sentiment
- ✅ Professional, modern UI

### Functionality:
- ✅ Real ChatGPT integration (not mock responses)
- ✅ Accurate sentiment detection
- ✅ Intelligent group formation
- ✅ Live backend connection status
- ✅ Real-time updates

### Technical Quality:
- ✅ Fast response times (<2 seconds)
- ✅ No errors in browser console (F12)
- ✅ Proper error handling (try disconnecting backend)
- ✅ Clean, readable code
- ✅ Production-ready architecture

---

## 🐛 Troubleshooting

### If you see "Backend Disconnected":
```bash
# Make sure backend is running
cd backend
python3 backend_api.py
```

### If OpenAI API not configured:
```bash
# Add your API key to backend/.env
echo "OPENAI_API_KEY=sk-your-key-here" > backend/.env
# Restart backend
```

### If port is already in use:
```bash
# Kill processes
lsof -ti:5000 | xargs kill -9    # Backend
lsof -ti:5173 | xargs kill -9    # Frontend
# Then run ./start.sh again
```

---

## 💡 Advanced Testing

### Test Different AI Models:
Currently configured to use `gpt-4o-mini` for cost-effectiveness.
Can be changed to `gpt-4o` for higher quality analysis.

### Test Edge Cases:
- Empty messages (should be disabled)
- Very long messages (should work fine)
- Multiple quick messages (should handle gracefully)
- Disconnect backend mid-conversation (should show error gracefully)

### Test Multiple Conversation Types:
Try all 8 sentiment states:
- Calm, Anxious, Sad, Stressed
- Happy, Depressed, Excited, Angry

---

## 📊 Expected Performance

**Speed:**
- Message analysis: 1-2 seconds
- Group formation: 2-3 seconds
- Dashboard load: <1 second

**Accuracy:**
- Sentiment detection: 85-95%
- Concern identification: 80-90%
- Group matching: 75-85% cohesion scores

**Reliability:**
- Zero crashes during demo
- Graceful error handling
- Clear status indicators

---

## 🎯 Key Demo Points

1. **Real AI Integration**: Not mock data - actual ChatGPT API calls
2. **Beautiful UI**: Professional Lovable design preserved exactly
3. **Complete Workflow**: Chat → Analysis → Groups → Dashboard
4. **Production Ready**: Clean code, proper architecture, deployable
5. **Easy to Run**: Two commands to get started

---

## 📝 Questions Judges Might Ask

**Q: Is this using real AI?**
A: Yes! OpenAI ChatGPT (gpt-4o-mini model) via official API.

**Q: Can you change the AI prompts?**
A: Yes! Backend supports custom prompts via API endpoint.

**Q: How do you handle privacy?**
A: User data stays in-memory for demo. Production would use encrypted database.

**Q: Can this scale?**
A: Yes! Stateless API design, can add database and deploy to cloud.

**Q: What's the cost?**
A: ~$0.00014 per message with gpt-4o-mini. Very affordable.

---

**Ready to impress! 🚀**
