#!/bin/bash

clear
echo "=========================================="
echo "   Mentra AI - Starting Servers"
echo "=========================================="
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Function to cleanup on exit
cleanup() {
    echo ""
    echo "=========================================="
    echo "   Shutting down servers..."
    echo "=========================================="
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup INT TERM

# Check if .env exists
if [ ! -f "backend/.env" ]; then
    echo -e "${YELLOW}⚠  Warning: backend/.env not found${NC}"
    echo "   Creating from template..."
    cp backend/.env.template backend/.env
    echo ""
    echo -e "${YELLOW}   Please edit backend/.env and add your OpenAI API key!${NC}"
    echo "   Get key from: https://platform.openai.com/api-keys"
    echo ""
    read -p "Press Enter to continue (backend will run without AI features)..."
fi

echo "[1/2] Starting Backend Server..."
echo ""

# Start backend in background
cd backend
python3 backend_api.py > ../backend.log 2>&1 &
BACKEND_PID=$!
cd ..

# Wait for backend to start
sleep 3

# Check if backend is running
if ps -p $BACKEND_PID > /dev/null; then
    echo -e "${GREEN}✓ Backend running on http://localhost:5000${NC}"
else
    echo -e "${YELLOW}⚠  Backend may have failed to start. Check backend.log${NC}"
fi

echo ""
echo "[2/2] Starting Frontend Server..."
echo ""

# Start frontend
cd frontend

echo ""
echo "=========================================="
echo "   🚀 Mentra AI is Starting"
echo "=========================================="
echo ""
echo -e "${GREEN}Backend:${NC}  http://localhost:5000"
echo -e "${GREEN}Frontend:${NC} http://localhost:5173"
echo ""
echo "The browser will open automatically..."
echo ""
echo "Press ${YELLOW}Ctrl+C${NC} to stop both servers"
echo "=========================================="
echo ""

# Start frontend (this will block)
npm run dev

# Cleanup when frontend stops
cleanup
