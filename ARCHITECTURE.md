# System Architecture

## Full Stack Architecture

```
┌─────────────────────────────────────────────────────────────────────┐
│                           USER BROWSER                              │
│                        http://localhost:3000                        │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ HTTP/REST
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                      NEXT.JS FRONTEND                               │
│                                                                     │
│  ┌─────────────┐  ┌──────────────┐  ┌────────────────┐           │
│  │   Home      │  │  Backtest    │  │  Live Signals  │           │
│  │   Page      │  │    Page      │  │     Page       │           │
│  │     /       │  │  /backtest   │  │    /live       │           │
│  └─────────────┘  └──────────────┘  └────────────────┘           │
│                                                                     │
│  ┌──────────────────────────────────────────────────────┐         │
│  │              Axios API Client                        │         │
│  │         (lib/axios.ts)                               │         │
│  └──────────────────────────────────────────────────────┘         │
│                                                                     │
│  Components: Shadcn UI (Card, Form, Table, Button, etc.)          │
│  Styling: Tailwind CSS                                             │
│  Charts: Recharts                                                  │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │ POST /api/backtest
                             │ GET /api/live-signals
                             │
┌────────────────────────────▼────────────────────────────────────────┐
│                      FASTAPI BACKEND                                │
│                    http://localhost:8000                            │
│                                                                     │
│  ┌─────────────────────────────────────────────────────────────┐  │
│  │                    API Endpoints                            │  │
│  │                                                             │  │
│  │  GET  /              → Health check                        │  │
│  │  POST /api/backtest  → Run backtest                        │  │
│  │  GET  /api/live-signals → Get trading signals              │  │
│  │  GET  /docs          → API documentation                   │  │
│  └─────────────────────────────────────────────────────────────┘  │
│                                                                     │
│  CORS Middleware: Allows frontend access                           │
│  Pydantic Models: Request/response validation                      │
└────────────────────────────┬────────────────────────────────────────┘
                             │
                             │
        ┌────────────────────┴────────────────────┐
        │                                         │
        ▼                                         ▼
┌───────────────────┐                  ┌──────────────────┐
│   Backtester      │                  │      Agent       │
│                   │                  │                  │
│ - Run backtest    │                  │ - Fetch data     │
│ - Calculate       │                  │ - Run strategies │
│   metrics         │                  │ - Generate       │
│ - Generate        │                  │   signals        │
│   portfolio       │                  │ - LLM reasoning  │
│   history         │                  │                  │
└─────────┬─────────┘                  └────────┬─────────┘
          │                                     │
          │                                     │
          └──────────────┬──────────────────────┘
                         │
                         ▼
        ┌────────────────────────────────────┐
        │      Trading Engine Core           │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │   Data Provider              │ │
        │  │   (Binance API)              │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │   Strategy Nodes             │ │
        │  │   - MacdStrategy             │ │
        │  │   - RSIStrategy              │ │
        │  │   - BollingerStrategy        │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │   Risk Management            │ │
        │  └──────────────────────────────┘ │
        │                                    │
        │  ┌──────────────────────────────┐ │
        │  │   Portfolio Management       │ │
        │  │   (LLM-based decisions)      │ │
        │  └──────────────────────────────┘ │
        └────────────────────────────────────┘
```

## Data Flow

### Backtest Flow

```
1. User fills form on /backtest page
   ↓
2. Frontend validates input (Zod schema)
   ↓
3. POST request to /api/backtest
   ↓
4. Backend creates Backtester instance
   ↓
5. Backtester fetches historical data
   ↓
6. Runs strategies across timeframes
   ↓
7. Generates signals and executes trades
   ↓
8. Calculates performance metrics
   ↓
9. Returns results to frontend
   ↓
10. Frontend displays:
    - Performance metrics table
    - Portfolio value chart
```

### Live Signals Flow

```
1. User clicks "Fetch Live Signals"
   ↓
2. GET request to /api/live-signals
   ↓
3. Backend creates Agent instance
   ↓
4. Agent fetches current market data
   ↓
5. Runs strategies on live data
   ↓
6. LLM analyzes signals and generates decisions
   ↓
7. Returns decisions to frontend
   ↓
8. Frontend displays for each ticker:
    - Action (buy/sell/hold)
    - Quantity
    - Confidence
    - Reasoning
```

## Technology Stack

### Frontend
```
┌─────────────────────────────────────┐
│         Next.js 16                  │
│         (React 19)                  │
├─────────────────────────────────────┤
│  UI Framework: Shadcn UI            │
│  Styling: Tailwind CSS              │
│  Forms: React Hook Form + Zod       │
│  HTTP: Axios                        │
│  Charts: Recharts                   │
│  Notifications: Sonner              │
│  Runtime: Bun                       │
└─────────────────────────────────────┘
```

### Backend
```
┌─────────────────────────────────────┐
│         FastAPI                     │
│         (Python 3.12)               │
├─────────────────────────────────────┤
│  Server: Uvicorn                    │
│  Validation: Pydantic               │
│  Trading: Custom Framework          │
│  Data: Binance API                  │
│  AI: OpenAI/Anthropic/etc.          │
│  Package Manager: uv                │
└─────────────────────────────────────┘
```

## File Structure

```
ai-hedge-fund-crypto/
│
├── Backend (Python)
│   ├── api.py                    # FastAPI server
│   ├── main.py                   # CLI entry point
│   ├── backtest.py               # Backtest CLI
│   ├── src/
│   │   ├── agent/                # Agent system
│   │   ├── backtest/             # Backtesting engine
│   │   ├── graph/                # Workflow nodes
│   │   ├── strategies/           # Trading strategies
│   │   ├── indicators/           # Technical indicators
│   │   └── utils/                # Utilities
│   └── .venv/                    # Python virtual env
│
├── Frontend (Next.js)
│   ├── app/
│   │   ├── page.tsx              # Home
│   │   ├── layout.tsx            # Root layout
│   │   ├── backtest/page.tsx     # Backtest UI
│   │   └── live/page.tsx         # Live signals UI
│   ├── components/ui/            # Shadcn components
│   ├── lib/axios.ts              # API client
│   └── node_modules/             # Dependencies
│
├── Configuration
│   ├── config.yaml               # Trading config
│   ├── .env                      # API keys (backend)
│   └── frontend/.env.local       # API URL (frontend)
│
├── Scripts
│   ├── start.sh                  # Start both services
│   └── test_api.py               # API testing
│
└── Documentation
    ├── README.md                 # Main docs
    ├── frontend/README.md        # Frontend docs
    ├── WEB_SETUP.md              # Setup guide
    ├── ARCHITECTURE.md           # This file
    └── IMPLEMENTATION_SUMMARY.md # Implementation details
```

## Communication Protocol

### Request/Response Format

**Backtest Request:**
```json
{
  "start_date": "2025-08-20T00:00:00",
  "end_date": "2025-09-04T00:00:00",
  "initial_cash": 10000,
  "tickers": ["BTCUSDT", "ETHUSDT"],
  "intervals": ["30m", "1h", "4h"],
  "strategies": ["MacdStrategy"]
}
```

**Backtest Response:**
```json
{
  "performance_metrics": {
    "sharpe_ratio": 1.23,
    "sortino_ratio": 1.45,
    "max_drawdown": -5.67
  },
  "portfolio_history": [
    {
      "Date": "2025-08-20T00:00:00",
      "Portfolio Value": 10000.00
    },
    ...
  ]
}
```

**Live Signals Response:**
```json
{
  "BTCUSDT": {
    "action": "buy",
    "quantity": 0.5,
    "confidence": 75,
    "reasoning": "Strong bullish signals across multiple timeframes..."
  },
  "ETHUSDT": {
    "action": "hold",
    "quantity": 0,
    "confidence": 50,
    "reasoning": "Mixed signals, waiting for clearer trend..."
  }
}
```

## Security Considerations

1. **CORS**: Configured to only allow localhost:3000
2. **API Keys**: Stored in .env files (not committed to git)
3. **Input Validation**: Pydantic models validate all inputs
4. **Error Handling**: Sensitive errors not exposed to frontend
5. **Rate Limiting**: Should be added for production
6. **Authentication**: Should be added for production

## Deployment Architecture (Future)

```
┌─────────────────────────────────────────────────────────────┐
│                      Load Balancer                          │
│                      (nginx/Cloudflare)                     │
└────────────┬────────────────────────────┬───────────────────┘
             │                            │
             │                            │
    ┌────────▼────────┐          ┌───────▼────────┐
    │   Frontend      │          │    Backend     │
    │   (Vercel/      │          │    (AWS/       │
    │    Netlify)     │          │     Railway)   │
    └─────────────────┘          └────────────────┘
                                          │
                                          │
                                 ┌────────▼────────┐
                                 │   Database      │
                                 │   (PostgreSQL)  │
                                 └─────────────────┘
```

## Performance Considerations

1. **Caching**: Market data cached to reduce API calls
2. **Async Operations**: FastAPI handles requests asynchronously
3. **Lazy Loading**: Frontend components load on demand
4. **Optimized Builds**: Production builds are minified
5. **CDN**: Static assets served from CDN in production

## Monitoring & Logging

For production deployment, consider:

1. **Backend Logging**: Python logging module
2. **Frontend Analytics**: Vercel Analytics or Google Analytics
3. **Error Tracking**: Sentry for both frontend and backend
4. **Performance Monitoring**: New Relic or DataDog
5. **Uptime Monitoring**: UptimeRobot or Pingdom
