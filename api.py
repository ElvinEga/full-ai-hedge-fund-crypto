import os
import sys
import yaml
import json
from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime
from typing import List, Dict, Any
from sqlalchemy.orm import Session

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.backtest.backtester import Backtester
from src.agent.agent import Agent
from src.utils.settings import settings as current_settings
from src.utils.constants import Interval
from src.database import get_db, BacktestRun

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

@app.get("/api/health")
def health_check():
    """Health check endpoint for deployment monitoring"""
    return {
        "status": "healthy",
        "service": "AI Hedge Fund Crypto API",
        "version": "1.0.0"
    }

@app.get("/api/settings")
async def get_settings():
    """Reads and returns the current config.yaml settings."""
    try:
        with open("config.yaml", "r") as f:
            settings_data = yaml.safe_load(f)
        return settings_data
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="config.yaml not found.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error reading config: {str(e)}")

@app.post("/api/settings")
async def update_settings(new_settings: Dict[str, Any]):
    """Receives new settings and updates config.yaml."""
    try:
        with open("config.yaml", "w") as f:
            yaml.dump(new_settings, f, default_flow_style=False, sort_keys=False)
        return {"message": "Settings updated successfully. Please restart the backend server for changes to take effect."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error writing config: {str(e)}")

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
    db = None
    run_record = None
    
    try:
        params_json = await websocket.receive_text()
        params_dict = json.loads(params_json)
        params = BacktestParams(**params_dict)

        # Create database session and record
        db = next(get_db())
        run_record = BacktestRun(
            start_date=params.start_date,
            end_date=params.end_date,
            initial_capital=params.initial_cash,
            parameters=json.dumps({
                "tickers": params.tickers,
                "intervals": params.intervals,
                "strategies": params.strategies
            })
        )
        db.add(run_record)
        db.commit()
        db.refresh(run_record)

        # Run main ensemble backtest with streaming
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
        
        final_metrics = None
        portfolio_history = None
        
        for update in backtester.run_backtest_stream():
            await websocket.send_json(update)
            if update["type"] == "final_metrics":
                final_metrics = update["data"]
            elif update["type"] == "portfolio_history":
                portfolio_history = update["data"]
        
        # Update database record with final results
        if portfolio_history and len(portfolio_history) > 0:
            final_value = portfolio_history[-1].get("Portfolio Value", params.initial_cash)
            run_record.final_portfolio_value = final_value
            run_record.total_return_pct = ((final_value / params.initial_cash) - 1) * 100
        
        if final_metrics:
            run_record.sharpe_ratio = final_metrics.get("sharpe_ratio")
            run_record.sortino_ratio = final_metrics.get("sortino_ratio")
            run_record.max_drawdown = final_metrics.get("max_drawdown")
        
        if portfolio_history:
            run_record.portfolio_history = json.dumps(portfolio_history)
        
        db.commit()

        # Run individual strategy backtests for comparison
        if len(params.strategies) > 1:
            import pandas as pd
            all_histories = []
            
            # Add ensemble results
            ensemble_df = pd.DataFrame(portfolio_history).set_index("Date")
            ensemble_df = ensemble_df[["Portfolio Value"]].rename(columns={"Portfolio Value": "Ensemble"})
            all_histories.append(ensemble_df)
            
            # Run each strategy individually
            for strategy in params.strategies:
                await websocket.send_json({"type": "status", "message": f"Running {strategy}..."})
                
                strategy_backtester = Backtester(
                    primary_interval=Interval.from_string(params.intervals[0]),
                    intervals=[Interval.from_string(i) for i in params.intervals],
                    tickers=params.tickers,
                    start_date=params.start_date,
                    end_date=params.end_date,
                    initial_capital=params.initial_cash,
                    strategies=[strategy],
                    model_name=current_settings.model.name,
                    model_provider=current_settings.model.provider,
                    model_base_url=current_settings.model.base_url,
                    show_agent_graph=False,
                    show_reasoning=False
                )
                
                strategy_df = strategy_backtester.get_portfolio_history_df()
                if not strategy_df.empty:
                    strategy_df = strategy_df[["Portfolio Value"]].rename(columns={"Portfolio Value": strategy})
                    all_histories.append(strategy_df)
            
            # Merge all results
            if all_histories:
                combined_df = pd.concat(all_histories, axis=1).ffill().reset_index()
                multi_model_history = combined_df.to_dict(orient='records')
                await websocket.send_json({"type": "multi_model_history", "data": multi_model_history})
        
        await websocket.send_json({"type": "complete", "run_id": run_record.id})

    except WebSocketDisconnect:
        print("WebSocket disconnected")
    except Exception as e:
        await websocket.send_json({"type": "error", "message": str(e)})
    finally:
        if db:
            db.close()
        await websocket.close()

@app.get("/api/backtests")
async def list_backtests(db: Session = Depends(get_db)):
    runs = db.query(BacktestRun).order_by(BacktestRun.id.desc()).limit(50).all()
    return runs

@app.get("/api/backtests/{run_id}")
async def get_backtest_details(run_id: int, db: Session = Depends(get_db)):
    run = db.query(BacktestRun).filter(BacktestRun.id == run_id).first()
    if not run:
        raise HTTPException(status_code=404, detail="Backtest not found.")
    
    return {
        "id": run.id,
        "start_date": run.start_date,
        "end_date": run.end_date,
        "initial_capital": run.initial_capital,
        "final_portfolio_value": run.final_portfolio_value,
        "total_return_pct": run.total_return_pct,
        "sharpe_ratio": run.sharpe_ratio,
        "sortino_ratio": run.sortino_ratio,
        "max_drawdown": run.max_drawdown,
        "parameters": json.loads(run.parameters) if run.parameters else {},
        "portfolio_history": json.loads(run.portfolio_history) if run.portfolio_history else []
    }

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
