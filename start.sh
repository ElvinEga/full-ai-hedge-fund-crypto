#!/bin/bash

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${GREEN}Starting AI Hedge Fund Crypto Full Stack Application${NC}"
echo ""

# Function to cleanup background processes on exit
cleanup() {
    echo -e "\n${BLUE}Shutting down services...${NC}"
    kill $BACKEND_PID $FRONTEND_PID 2>/dev/null
    exit
}

trap cleanup SIGINT SIGTERM

# Start Python Backend
echo -e "${BLUE}Starting Python FastAPI Backend on port 8000...${NC}"
source .venv/bin/activate
uvicorn api:app --reload --port 8000 &
BACKEND_PID=$!

# Wait a moment for backend to start
sleep 2

# Start Next.js Frontend
echo -e "${BLUE}Starting Next.js Frontend on port 3000...${NC}"
cd frontend
bun run dev &
FRONTEND_PID=$!

echo ""
echo -e "${GREEN}Services started successfully!${NC}"
echo -e "Backend API: ${BLUE}http://localhost:8000${NC}"
echo -e "Frontend UI: ${BLUE}http://localhost:3000${NC}"
echo -e "API Docs: ${BLUE}http://localhost:8000/docs${NC}"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for both processes
wait
