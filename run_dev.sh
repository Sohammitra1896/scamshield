#!/bin/bash
# ==============================================================================
# ScamShield Development Launcher
# Team: OBSIDIAN | INNOV12 Competition
# ==============================================================================

set -e

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

echo "=========================================================="
echo " Starting ScamShield Development Environment"
echo " Team: OBSIDIAN | INNOV12"
echo " Tracks: Cyber & Digital Trust (Primary) | AI & GenAI"
echo "=========================================================="

# Check Python environment
if [ ! -d "backend/venv" ]; then
    echo "[!] backend/venv not found. Creating..."
    python3 -m venv backend/venv
    backend/venv/bin/pip install -r backend/requirements.txt
fi

# Check frontend modules
if [ ! -d "frontend/node_modules" ]; then
    echo "[!] frontend/node_modules not found. Running npm install..."
    (cd frontend && npm install)
fi

# Cleanup on exit
cleanup() {
    echo ""
    echo "[*] Shutting down ScamShield services..."
    kill $BACKEND_PID 2>/dev/null || true
    kill $FRONTEND_PID 2>/dev/null || true
    exit 0
}
trap cleanup SIGINT SIGTERM EXIT

# Start Backend
echo "[*] Launching FastAPI backend on http://127.0.0.1:8000..."
"$PROJECT_ROOT/backend/venv/bin/uvicorn" app.main:app \
    --app-dir "$PROJECT_ROOT/backend" \
    --host 127.0.0.1 \
    --port 8000 \
    --reload &
BACKEND_PID=$!

# Wait for backend health
echo "[*] Waiting for backend to initialize..."
for i in {1..15}; do
    if curl -s http://127.0.0.1:8000/api/v1/health | grep -q "healthy"; then
        echo "[+] Backend is healthy and ready!"
        break
    fi
    sleep 1
done

# Start Frontend
echo "[*] Launching React Vite frontend on http://localhost:5173..."
(cd frontend && npm run dev) &
FRONTEND_PID=$!

echo ""
echo "=========================================================="
echo " ScamShield is running!"
echo " - Frontend: http://localhost:5173"
echo " - API Docs: http://127.0.0.1:8000/api/v1/docs"
echo " - Health:   http://127.0.0.1:8000/api/v1/health"
echo " Press Ctrl+C to terminate both servers."
echo "=========================================================="

wait
