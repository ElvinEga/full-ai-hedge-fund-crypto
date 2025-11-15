import os
import sys
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
import json

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.backtest.backtester import Backtester
from src.agent.agent import Agent
from src.utils.settings import settings as current_settings
from src.utils.constants import Interval

app = FastAPI(title="AI Hedge Fund Crypto API")

origins = ["http://localhost:3000", "http://127.0.0.1:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class BacktestParams(BaseModel):
    start_date: datetime
    end_date: datetime
    initial_cash: int
    tickers: List[str]
    intervals: List[str]
    strategies: List[str]

@app.get("/")
def read_root():
    return {"message": "AI Hedge Fund Crypto API is running."}

@app.post("/api/backtest")
async def run_backtest(params: BacktestParams):
    try:
        backtester = Backtester(
            primary_interval=Interval.from_string(params.intervals[0]),
            intervals=[Interval.from_string(i) for i in params.intervals],
            tickers=params.tickers,
            start_date=params.start_date,
            end_date=params.end_date,
            initial_capital=params.initial_cash,
            strategies=params.strategies,
            model_name=current_settings.model.name,
            model_provider=current_settings.model.provider,
            model_base_url=current_settings.model.base_url,
            show_agent_graph=False,
            show_reasoning=False
        )
        
        print("Starting backtest via API...")
        performance_metrics = backtester.run_backtest()
        performance_df = backtester.analyze_performance()

        portfolio_history = performance_df.reset_index().to_dict(orient='records')
        
        return {
            "performance_metrics": performance_metrics,
            "portfolio_history": portfolio_history
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.websocket("/ws/backtest")
async def websocket_backtest(websocket: WebSocket):
    await websocket.accept()
    try:
        params_json = await websocket.receive_text()
        params_dict = json.loads(params_json)
        params = BacktestParams(**params_dict)

        backtester = Backtester(
            primary_interval=Interval.from_string(params.intervals[0]),
            intervals=[Interval.from_string(i) for i in params.intervals],
            tickers=params.tickers,
            start_date=params.start_date,
            end_date=params.end_date,
            initial_capital=params.initial_cash,
            strategies=params.strategies,
            model_name=current_settings.model.name,
            model_provider=current_settings.model.provider,
            model_base_url=current_settings.model.base_url,
            show_agent_graph=False,
            show_reasoning=False
        )
        
        for update in backtester.run_backtest_stream():
            await websocket.send_json(update)
        
        await websocket.send_json({"type": "complete"})

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        await websocket.close()

@app.get("/api/live-signals")
async def get_live_signals():
    portfolio_stub = {
        "cash": 100000,
        "positions": {},
        "margin_requirement": 0.0,
        "margin_used": 0.0,
        "realized_gains": {}
    }
    
    agent = Agent(
        intervals=[Interval.from_string(i) for i in current_settings.signals.intervals],
        strategies=current_settings.signals.strategies,
        show_agent_graph=False,
    )

    result = agent.run(
        primary_interval=current_settings.primary_interval,
        tickers=current_settings.signals.tickers,
        end_date=datetime.now(),
        portfolio=portfolio_stub,
        show_reasoning=True,
        model_name=current_settings.model.name,
        model_provider=current_settings.model.provider,
        model_base_url=current_settings.model.base_url
    )
    return result.get('decisions', {})
