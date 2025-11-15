# AI Hedge Fund Crypto - Complete Edition

A production-ready, full-stack algorithmic trading framework with AI-enhanced decision making, featuring a modern web interface for backtesting, live signal analysis, and multi-strategy comparison.

## 🌟 Key Features

### Trading & Analysis
- ✅ **Multi-Strategy Backtesting** - Test multiple strategies simultaneously
- ✅ **Real-Time Signal Generation** - Live trading signals with AI reasoning
- ✅ **Multi-Timeframe Analysis** - Analyze across 5m, 15m, 30m, 1h, 4h, 1d
- ✅ **Ensemble Strategy Support** - Combine multiple strategies for better performance
- ✅ **AI-Powered Decisions** - LLM integration for intelligent portfolio management

### Visualization & UI
- ✅ **Alpha Arena-Style Charts** - Professional multi-strategy comparison
- ✅ **Interactive Data Tables** - Sortable, paginated trade logs
- ✅ **Advanced Performance Charts** - Portfolio value, drawdown, daily PnL
- ✅ **Real-Time Progress** - WebSocket streaming during backtests
- ✅ **Dark Mode** - Beautiful dark theme support
- ✅ **Responsive Design** - Works on desktop and mobile

### Data & Persistence
- ✅ **Database Storage** - All backtests saved automatically
- ✅ **Historical Tracking** - Review and compare past results
- ✅ **Configuration Management** - Edit settings via UI
- ✅ **Signal Breakdown** - Detailed analysis by ticker and interval

### Developer Experience
- ✅ **Modern Tech Stack** - Next.js 16, FastAPI, TypeScript
- ✅ **WebSocket Support** - Real-time updates
- ✅ **Health Monitoring** - Production-ready endpoints
- ✅ **Comprehensive Docs** - 15+ documentation files
- ✅ **Easy Deployment** - Docker & cloud-ready

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/51bitquant/ai-hedge-fund-crypto.git
cd ai-hedge-fund-crypto

# Backend setup
uv venv --python 3.12
source .venv/bin/activate
uv pip install -e .

# Configure environment
cp .env.example .env
# Edit .env with your API keys
```

### Running

```bash
# Start both services
./start.sh

# Or manually:
# Terminal 1 - Backend
uvicorn api:app --reload --port 8000

# Terminal 2 - Frontend
cd frontend && bun run dev
```

### Access

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

## 📊 Screenshots

### Multi-Strategy Comparison
Compare ensemble vs individual strategies with professional charts:
- Toggle between $ and % views
- Color-coded strategy lines
- Final values displayed
- Interactive tooltips

### Interactive Trade Log
- Sortable columns
- Pagination (20 rows/page)
- Color-coded actions
- Real-time updates

### Advanced Charts
- Portfolio value over time
- Drawdown visualization
- Daily PnL bars
- Responsive design

### Dark Mode
- Beautiful dark theme
- One-click toggle
- System theme detection
- Smooth transitions

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Web Browser                          │
│              http://localhost:3000                      │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ HTTP/REST + WebSocket
                     │
┌────────────────────▼────────────────────────────────────┐
│                 Next.js Frontend                        │
│  - 6 Pages (Home, Dashboard, Backtest, History, etc.)  │
│  - 20+ React Components                                │
│  - Real-time WebSocket Updates                         │
│  - Dark Mode Support                                   │
└────────────────────┬────────────────────────────────────┘
                     │
                     │ REST API + WebSocket
                     │
┌────────────────────▼────────────────────────────────────┐
│                 FastAPI Backend                         │
│  - 10 API Endpoints                                    │
│  - WebSocket Streaming                                 │
│  - Multi-Strategy Execution                            │
│  - Database Persistence                                │
└────────────────────┬────────────────────────────────────┘
                     │
        ┌────────────┴────────────┐
        │                         │
        ▼                         ▼
┌───────────────┐         ┌──────────────┐
│   SQLite DB   │         │  Binance API │
│  (Backtests)  │         │ (Market Data)│
└───────────────┘         └──────────────┘
```

## 📦 Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database
- **LangGraph** - Workflow orchestration
- **Pandas/NumPy** - Data analysis
- **WebSockets** - Real-time communication

### Frontend
- **Next.js 16** - React framework
- **TypeScript** - Type safety
- **Tailwind CSS** - Styling
- **Shadcn UI** - Component library
- **TanStack Table** - Data tables
- **Recharts** - Charts
- **next-themes** - Dark mode

## 🎯 Use Cases

### For Traders
- Test multiple strategies before live trading
- Compare strategy performance objectively
- Analyze historical performance
- Generate live trading signals
- Review detailed trade logs

### For Researchers
- Experiment with different parameters
- Analyze multi-timeframe signals
- Study strategy correlations
- Evaluate risk metrics
- Build ensemble strategies

### For Developers
- Learn full-stack development
- Study WebSocket implementation
- Understand trading algorithms
- Practice with modern frameworks
- Deploy production applications

## 📈 Performance

- **Backtest Speed**: Depends on data size and strategies
- **Real-time Updates**: < 100ms latency
- **Database Queries**: < 100ms
- **Chart Rendering**: < 500ms
- **Page Load**: < 2s

## 🔒 Security

- API keys in environment variables
- CORS configured
- Input validation (Pydantic + Zod)
- Error message sanitization
- Health check endpoint
- Production-ready

## 📚 Documentation

- **README.md** - Main documentation
- **DEPLOYMENT_GUIDE.md** - Production deployment
- **WEB_SETUP.md** - Setup instructions
- **ARCHITECTURE.md** - System architecture
- **QUICK_REFERENCE.md** - Command reference
- **PHASE_*.md** - Implementation details
- **FINAL_SUMMARY.md** - Complete overview

## 🚢 Deployment

### Recommended Platforms

**Frontend**: Vercel (automatic deployment)
**Backend**: Railway or Fly.io (Docker-based)
**Database**: PostgreSQL (production)

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for detailed instructions.

## 🛠️ Development

### Project Structure

```
ai-hedge-fund-crypto/
├── api.py                  # FastAPI server
├── src/                    # Backend source
│   ├── agent/              # Trading agent
│   ├── backtest/           # Backtesting engine
│   ├── strategies/         # Trading strategies
│   └── database.py         # Database models
├── frontend/               # Next.js frontend
│   ├── app/                # Pages
│   ├── components/         # React components
│   └── hooks/              # Custom hooks
└── docs/                   # Documentation
```

### Adding New Strategies

1. Create strategy file in `src/strategies/`
2. Implement `BaseNode` interface
3. Add to `config.yaml`
4. Run backtest

See [Creating Custom Strategies](README.md#creating-custom-strategies) for details.

## 🤝 Contributing

Contributions are welcome! Please:

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📊 Metrics

- **Total Code**: ~5500+ lines
- **Backend**: ~3000+ lines Python
- **Frontend**: ~2500+ lines TypeScript/React
- **Components**: 20+ React components
- **API Endpoints**: 10 endpoints
- **Pages**: 6 complete pages
- **Documentation**: 15+ markdown files

## 🎓 Learning Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)
- [LangGraph Documentation](https://langchain-ai.github.io/langgraph/)
- [Binance API Documentation](https://binance-docs.github.io/apidocs/)

## ⚠️ Disclaimer

This project is for educational and research purposes only. Trading cryptocurrencies involves substantial risk of loss. Past performance does not guarantee future results. Always do your own research and never invest more than you can afford to lose.

## 📝 License

MIT License - See [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built with inspiration from Alpha Arena
- Uses LangGraph for workflow orchestration
- Powered by Binance market data
- Enhanced by AI language models

## 📞 Support

- **Issues**: Open a GitHub issue
- **Discussions**: GitHub Discussions
- **Documentation**: See docs/ folder

## 🌟 Star History

If you find this project useful, please consider giving it a star! ⭐

## 🔗 Links

- **GitHub**: https://github.com/51bitquant/ai-hedge-fund-crypto
- **Documentation**: See README.md and docs/
- **Binance Referral**: [Sign up](https://www.binance.com/futures/ref/51bitquant)

---

**Built with ❤️ for the crypto trading community**

Ready to deploy? See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md)

Want to contribute? See [CONTRIBUTING.md](CONTRIBUTING.md)

Have questions? Open an issue!
