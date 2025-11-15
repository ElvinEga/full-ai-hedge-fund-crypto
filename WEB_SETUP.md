# Web Interface Setup Guide

This guide will help you set up and run the web interface for the AI Hedge Fund Crypto trading framework.

## Prerequisites

Before starting, ensure you have:

1. **Python 3.12+** with the project dependencies installed
2. **Bun** installed (for the frontend)
3. **Binance API keys** configured in `.env`
4. **LLM API keys** (OpenAI, Anthropic, etc.) configured in `.env`

## Quick Start (Recommended)

The easiest way to run the full stack:

```bash
./start.sh
```

This single command will:
- Activate your Python virtual environment
- Start the FastAPI backend on port 8000
- Start the Next.js frontend on port 3000

Access the application at:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Documentation**: http://localhost:8000/docs

Press `Ctrl+C` to stop both services.

## Manual Setup

If you prefer to run services separately:

### Step 1: Start the Python Backend

```bash
# From project root
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

The API will be available at http://localhost:8000

### Step 2: Start the Next.js Frontend

Open a new terminal:

```bash
# From project root
cd frontend
bun run dev
```

The frontend will be available at http://localhost:3000

## Using the Web Interface

### Backtest Page

1. Navigate to http://localhost:3000/backtest
2. Configure your backtest parameters:
   - **Start Date**: Beginning of backtest period
   - **End Date**: End of backtest period
   - **Initial Cash**: Starting capital in USD
   - **Tickers**: Comma-separated list (e.g., `BTCUSDT, ETHUSDT`)
   - **Intervals**: Comma-separated timeframes (e.g., `30m, 1h, 4h`)
   - **Strategies**: Comma-separated strategy names (e.g., `MacdStrategy`)
3. Click "Run Backtest"
4. View results including:
   - Performance metrics (Sharpe ratio, Sortino ratio, Max drawdown)
   - Portfolio value chart over time

### Live Signals Page

1. Navigate to http://localhost:3000/live
2. Click "Fetch Live Signals"
3. View current trading signals for each ticker:
   - Action (buy/sell/hold)
   - Quantity
   - Confidence level
   - AI reasoning

## Troubleshooting

### Backend Issues

**Problem**: `ModuleNotFoundError` when starting the API

**Solution**: Ensure your virtual environment is activated and dependencies are installed:
```bash
source .venv/bin/activate
uv pip sync
```

**Problem**: CORS errors in browser console

**Solution**: Check that the frontend URL is in the `origins` list in `api.py`

### Frontend Issues

**Problem**: `ECONNREFUSED` error when fetching data

**Solution**: Ensure the backend is running on port 8000

**Problem**: Environment variable not found

**Solution**: Create `.env.local` in the frontend directory:
```
NEXT_PUBLIC_API_URL=http://localhost:8000/api
```

## Architecture

```
┌─────────────────┐         HTTP/REST         ┌──────────────────┐
│                 │ ◄────────────────────────► │                  │
│  Next.js        │                            │  FastAPI         │
│  Frontend       │   POST /api/backtest       │  Backend         │
│  (Port 3000)    │   GET /api/live-signals    │  (Port 8000)     │
│                 │                            │                  │
└─────────────────┘                            └──────────────────┘
                                                        │
                                                        │
                                                        ▼
                                               ┌──────────────────┐
                                               │                  │
                                               │  Trading Engine  │
                                               │  - Backtester    │
                                               │  - Agent         │
                                               │  - Strategies    │
                                               │                  │
                                               └──────────────────┘
```

## Next Steps

- Customize the frontend styling in `frontend/app/globals.css`
- Add more API endpoints in `api.py`
- Create additional pages in `frontend/app/`
- Implement WebSocket support for real-time updates
- Add authentication for production deployment

## Production Deployment

For production deployment:

1. Build the frontend:
   ```bash
   cd frontend
   bun run build
   ```

2. Run the production server:
   ```bash
   bun run start
   ```

3. Use a process manager like PM2 or systemd for the backend
4. Set up a reverse proxy (nginx/Apache) for both services
5. Enable HTTPS with SSL certificates
6. Implement proper authentication and authorization

## Support

For issues or questions:
- Check the main [README.md](README.md)
- Review the [frontend README](frontend/README.md)
- Open an issue on GitHub
