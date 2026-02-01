#!/bin/bash

clear
echo "=========================================="
echo "   Mentra AI - One-Time Setup"
echo "=========================================="
echo ""

# Colors for output
GREEN='\033[0.32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check Python
echo -n "Checking Python... "
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install Python 3.8+ from https://www.python.org/"
    exit 1
fi
echo -e "${GREEN}✓ $(python3 --version)${NC}"

# Check Node.js
echo -n "Checking Node.js... "
if ! command -v node &> /dev/null; then
    echo -e "${RED}✗ Not found${NC}"
    echo "Please install Node.js 16+ from https://nodejs.org/"
    exit 1
fi
echo -e "${GREEN}✓ $(node --version)${NC}"

echo ""
echo "=========================================="
echo "   Installing Backend Dependencies"
echo "=========================================="
echo ""

cd backend

# Install Python packages
echo "Installing Flask, OpenAI, and other Python packages..."
pip3 install -r requirements.txt --quiet
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ Python packages installed${NC}"
else
    echo -e "${RED}✗ Failed to install Python packages${NC}"
    exit 1
fi

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo ""
    echo "Creating .env file..."
    cp .env.template .env
    echo -e "${YELLOW}⚠  IMPORTANT: Edit backend/.env and add your OpenAI API key!${NC}"
    echo "   Get your key from: https://platform.openai.com/api-keys"
    echo ""
fi

cd ..

echo ""
echo "=========================================="
echo "   Installing Frontend Dependencies"
echo "=========================================="
echo ""

cd frontend

# Install Node packages
echo "Installing React, Vite, and other npm packages..."
echo "(This may take a few minutes...)"
npm install --silent
if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ npm packages installed${NC}"
else
    echo -e "${RED}✗ Failed to install npm packages${NC}"
    exit 1
fi

cd ..

echo ""
echo "=========================================="
echo "   Setup Complete! ✓"
echo "=========================================="
echo ""
echo "Next steps:"
echo "  1. Edit backend/.env and add your OpenAI API key"
echo "     Get key from: https://platform.openai.com/api-keys"
echo ""
echo "  2. Run the application:"
echo "     ${GREEN}./start.sh${NC}"
echo ""
echo "=========================================="
echo ""
