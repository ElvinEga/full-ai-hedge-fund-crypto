# Quick Reference Guide

## Starting the Application

### Option 1: Quick Start (Recommended)
```bash
./start.sh
```
- Starts both backend and frontend
- Press `Ctrl+C` to stop both services

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

**Terminal 2 - Frontend:**
```bash
cd frontend
bun run dev
```

## URLs

| Service | URL | Description |
|---------|-----|-------------|
| Frontend | http://localhost:3000 | Web interface |
| Backend API | http://localhost:8000 | REST API |
| API Docs | http://localhost:8000/docs | Interactive API documentation |
| Backtest Page | http://localhost:3000/backtest | Run backtests |
| Live Signals | http://localhost:3000/live | View trading signals |

## Common Commands

### Backend

```bash
# Start API server
uvicorn api:app --reload --port 8000

# Run backtest (CLI)
uv run backtest.py

# Run live mode (CLI)
uv run main.py

# Test API
python test_api.py

# Install new Python package
uv pip install <package-name>
```

### Frontend

```bash
# Start development server
bun run dev

# Build for production
bun run build

# Start production server
bun run start

# Install new package
bun add <package-name>

# Add Shadcn component
bunx shadcn@latest add <component-name>
```

## Configuration Files

| File | Purpose |
|------|---------|
| `config.yaml` | Trading strategy configuration |
| `.env` | Backend API keys (Binance, OpenAI, etc.) |
| `frontend/.env.local` | Frontend environment variables |

## API Endpoints

### GET /
Health check endpoint
```bash
curl http://localhost:8000/
```

### POST /api/backtest
Run a backtest
```bash
curl -X POST http://localhost:8000/api/backtest \
  -H "Content-Type: application/json" \
  -d '{
    "start_date": "2025-08-20T00:00:00",
    "end_date": "2025-09-04T00:00:00",
    "initial_cash": 10000,
    "tickers": ["BTCUSDT"],
    "intervals": ["1h"],
    "strategies": ["MacdStrategy"]
  }'
```

### GET /api/live-signals
Get current trading signals
```bash
curl http://localhost:8000/api/live-signals
```

## Troubleshooting

### Backend won't start
```bash
# Check if virtual environment is activated
which python  # Should show path in .venv

# Reinstall dependencies
source .venv/bin/activate
uv pip sync
```

### Frontend won't start
```bash
# Reinstall dependencies
cd frontend
bun install

# Clear Next.js cache
rm -rf .next
bun run dev
```

### CORS errors
Check that `frontend/.env.local` has:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

### API connection refused
Make sure backend is running on port 8000:
```bash
curl http://localhost:8000/
```

### Module not found errors
```bash
# Backend
source .venv/bin/activate
uv pip sync

# Frontend
cd frontend
bun install
```

## File Locations

### Backend Files
- `api.py` - FastAPI server
- `src/agent/agent.py` - Trading agent
- `src/backtest/backtester.py` - Backtesting engine
- `src/strategies/` - Trading strategies

### Frontend Files
- `frontend/app/page.tsx` - Home page
- `frontend/app/backtest/page.tsx` - Backtest page
- `frontend/app/live/page.tsx` - Live signals page
- `frontend/lib/axios.ts` - API client

### Configuration
- `config.yaml` - Main configuration
- `.env` - Backend secrets
- `frontend/.env.local` - Frontend config

## Development Workflow

1. **Make changes to backend:**
   - Edit Python files
   - Server auto-reloads (if using `--reload`)

2. **Make changes to frontend:**
   - Edit TypeScript/React files
   - Browser auto-refreshes

3. **Add new strategy:**
   - Create file in `src/strategies/`
   - Add to `config.yaml`
   - Restart backend

4. **Add new UI component:**
   - Use Shadcn: `bunx shadcn@latest add <component>`
   - Or create custom in `frontend/components/`

## Testing

### Test Backend
```bash
# Interactive test
python test_api.py

# Manual curl test
curl http://localhost:8000/
```

### Test Frontend
```bash
# Open in browser
open http://localhost:3000

# Check console for errors
# Open browser DevTools (F12)
```

## Production Deployment

### Backend
```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn api:app -w 4 -k uvicorn.workers.UvicornWorker
```

### Frontend
```bash
cd frontend
bun run build
bun run start
```

## Environment Variables

### Backend (.env)
```bash
BINANCE_API_KEY=your-key
BINANCE_API_SECRET=your-secret
OPENAI_API_KEY=your-key
ANTHROPIC_API_KEY=your-key
```

### Frontend (.env.local)
```bash
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Logs

### Backend Logs
- Printed to console where `uvicorn` is running
- Check for errors in red

### Frontend Logs
- Browser console (F12 → Console tab)
- Terminal where `bun run dev` is running

## Performance Tips

1. **Cache market data** - Reduces API calls to Binance
2. **Use production builds** - Much faster than dev mode
3. **Limit date ranges** - Shorter backtests run faster
4. **Reduce intervals** - Fewer timeframes = faster processing

## Getting Help

1. Check documentation:
   - `README.md` - Main documentation
   - `WEB_SETUP.md` - Setup guide
   - `ARCHITECTURE.md` - System architecture
   - `frontend/README.md` - Frontend docs

2. Check logs for errors

3. Test API with `test_api.py`

4. Open issue on GitHub

## Useful Links

- [FastAPI Docs](https://fastapi.tiangolo.com/)
- [Next.js Docs](https://nextjs.org/docs)
- [Shadcn UI](https://ui.shadcn.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Recharts](https://recharts.org/)
