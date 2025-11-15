# Phase 20: Non-Blocking Backtest Execution

## Problem Statement
The original WebSocket implementation ran backtests synchronously on the main event loop, blocking all other API requests (like `/api/live-signals` or `/api/settings`) until the backtest completed. This made the API unresponsive during long-running backtests.

## Solution: AsyncIO Thread Pool Executor

Instead of implementing a complex Redis-based job queue system, we use Python's built-in `asyncio.run_in_executor()` to run CPU-intensive backtest operations in a thread pool while keeping the WebSocket connection responsive.

## Implementation

### Modified: `api.py`

**Key Changes:**
1. Added `asyncio` import
2. Wrapped backtest execution in `loop.run_in_executor(None, run_backtest_sync)`
3. Moved all blocking operations (Backtester instantiation and iteration) into sync functions
4. Executor runs these sync functions in a separate thread pool

**Architecture:**
```
Client Request → WebSocket Accept → Executor Thread (Backtest) → Stream Results → Complete
                      ↓
                 Main Event Loop (Free to handle other requests)
```

### How It Works

1. **WebSocket Connection**: Client connects and sends parameters
2. **Async Wrapper**: `run_backtest_async()` function coordinates the work
3. **Thread Pool Execution**: 
   - `run_backtest_sync()` runs in executor thread
   - Collects all backtest updates in memory
   - Returns complete list of updates
4. **Result Streaming**: Main event loop sends updates to client via WebSocket
5. **Database Update**: Final metrics saved to database
6. **Multi-Strategy Comparison**: Each strategy also runs in executor

### Benefits

✅ **Non-Blocking**: API remains responsive during backtests
✅ **Simple**: No external dependencies (Redis, RabbitMQ)
✅ **No Code Changes**: Frontend works unchanged
✅ **Thread-Safe**: Each backtest runs in isolated thread
✅ **Scalable**: Thread pool handles multiple concurrent requests

### Trade-offs

**Pros:**
- Zero infrastructure overhead
- Easy to understand and maintain
- Works with existing WebSocket architecture
- No message broker setup required

**Cons:**
- Limited to single-server deployment
- Thread pool size limits concurrent backtests
- Not suitable for distributed systems
- Memory overhead (stores all updates before streaming)

## Testing

### Verify Non-Blocking Behavior

**Terminal 1: Start Backend**
```bash
source .venv/bin/activate
uvicorn api:app --reload --port 8000
```

**Terminal 2: Start Frontend**
```bash
cd frontend
bun run dev
```

**Test Steps:**
1. Open browser to `http://localhost:3000/backtest`
2. Start a long backtest (e.g., 30+ days)
3. While backtest is running, open new tab
4. Navigate to `http://localhost:3000/live` or `http://localhost:3000/settings`
5. Verify these pages load instantly (not blocked)
6. Check backtest continues streaming in original tab

## Future Enhancements

For production deployments with high concurrency needs, consider:

### Option 1: Process Pool (No External Dependencies)
```python
from concurrent.futures import ProcessPoolExecutor
executor = ProcessPoolExecutor(max_workers=4)
await loop.run_in_executor(executor, run_backtest_sync)
```

### Option 2: Redis + Celery (Distributed)
- Separate worker processes
- Horizontal scaling
- Job persistence
- Better monitoring

### Option 3: Kubernetes Jobs
- Container-based workers
- Auto-scaling
- Resource isolation
- Cloud-native

## Performance Considerations

**Thread Pool Size:**
- Default: `min(32, os.cpu_count() + 4)`
- Adjust with: `uvicorn api:app --workers 4`

**Memory Usage:**
- Each backtest stores full update history in memory
- Monitor with long backtests (>1000 timesteps)
- Consider streaming directly if memory becomes issue

**Concurrent Backtests:**
- Limited by thread pool size
- Each backtest uses 1 thread
- Additional requests queue automatically

## Conclusion

This implementation provides a pragmatic solution that:
- Solves the blocking issue immediately
- Requires no infrastructure changes
- Maintains code simplicity
- Scales adequately for small-to-medium deployments

For applications requiring higher concurrency or distributed execution, the architecture can be upgraded to Redis/Celery without changing the frontend.
