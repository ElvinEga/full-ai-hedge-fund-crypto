# Phase 21: Persistent Backtest State with Zustand

## Problem Statement
When navigating away from the backtest page during a running backtest and returning, all progress was lost. This happened because React components unmount when navigating away, destroying all local state (`useState` values).

## Root Cause: Component Lifecycle

1. **Mount**: Visit `/backtest` → Component renders with initial state
2. **Run**: Start backtest → Local state updates with progress
3. **Navigate Away**: Go to `/dashboard` → Component unmounts, state destroyed
4. **Return**: Back to `/backtest` → New component instance, fresh initial state

The WebSocket connection also closed on unmount, losing the stream.

## Solution: Global State Management with Zustand

Zustand provides a global store that persists across component mount/unmount cycles, surviving page navigation within the same browser tab.

## Implementation

### Installed: `zustand@5.0.8`
```bash
bun add zustand
```

### New: `frontend/store/backtest.ts`

**Store Structure:**
```typescript
{
  isBacktesting: boolean
  progress: ProgressRow[]
  results: { performance_metrics, portfolio_history }
  latestAnalysis: any
  multiModelHistory: any[]
  latestSummary: LiveSummaryData
}
```

**Actions:**
- `setIsBacktesting(value)` - Update backtest status
- `addProgress(row)` - Append progress row
- `setLatestAnalysis(data)` - Update analysis details
- `setLatestSummary(data)` - Update live summary
- `setResults(data)` - Update final metrics/history
- `setMultiModelHistory(data)` - Update comparison chart data
- `reset()` - Clear all state for new backtest

### Modified: `frontend/app/backtest/page.tsx`

**Before (Local State):**
```typescript
const [isBacktesting, setIsBacktesting] = useState(false);
const [progress, setProgress] = useState<ProgressRow[]>([]);
// ... 5 more useState hooks
```

**After (Global State):**
```typescript
const {
  isBacktesting,
  progress,
  results,
  // ... all state from store
  setIsBacktesting,
  addProgress,
  // ... all actions from store
  reset,
} = useBacktestStore();
```

**Key Changes:**
1. Replaced all `useState` hooks with Zustand store
2. `onSubmit` calls `reset()` before starting new backtest
3. Message handler uses store actions instead of `setState`
4. Component reads state from store on every render

## How It Works

### State Persistence Flow

```
User starts backtest → Store updates → Navigate away → Component unmounts
                                              ↓
                                        Store persists
                                              ↓
Navigate back → New component mounts → Reads from store → Shows progress
```

### WebSocket Reconnection

The `socketUrl` state remains local (not in store) because:
- It's derived from form submission
- WebSocket hook handles connection lifecycle
- Store only tracks backtest data, not connection state

When returning to the page:
1. Component mounts with fresh `socketUrl = null`
2. Reads `isBacktesting`, `progress`, etc. from store
3. Displays all accumulated progress immediately
4. User can start new backtest (resets store and creates new WebSocket)

## Benefits

✅ **Navigation Persistence**: Progress survives page changes
✅ **Seamless UX**: Return to see exactly where you left off
✅ **No Backend Changes**: Works with existing WebSocket implementation
✅ **Simple API**: Clean actions for state updates
✅ **Type Safety**: Full TypeScript support
✅ **Minimal Overhead**: Zustand is tiny (~1KB)

## User Experience

### Before
1. Start backtest on `/backtest`
2. Navigate to `/dashboard`
3. Return to `/backtest`
4. ❌ All progress lost, blank page

### After
1. Start backtest on `/backtest`
2. Navigate to `/dashboard` (check live signals)
3. Return to `/backtest`
4. ✅ See all accumulated progress, live summary, charts

## Limitations

**Tab-Scoped Persistence:**
- State persists within a single browser tab
- Closing tab or refreshing page resets state
- Different tabs have independent stores

**No Cross-Session Persistence:**
- State doesn't survive browser restart
- For that, use localStorage or database queries

## Future Enhancements

### Option 1: LocalStorage Persistence
```typescript
import { persist } from 'zustand/middleware';

export const useBacktestStore = create(
  persist(
    (set) => ({ /* ... */ }),
    { name: 'backtest-storage' }
  )
);
```

### Option 2: Resume from Database
- Store `run_id` in Zustand
- On mount, check if backtest is running
- Fetch progress from `/api/backtests/{run_id}`
- Resume WebSocket connection

### Option 3: Multiple Concurrent Backtests
- Store array of backtest runs
- Each with unique `job_id`
- Switch between active backtests
- View history of completed runs

## Testing

**Test Persistence:**
1. Start backtest at `http://localhost:3000/backtest`
2. Wait for some progress rows to appear
3. Click "Dashboard" in navigation
4. Click "Backtest" to return
5. ✅ Verify all progress is still visible
6. ✅ Verify live summary shows latest values
7. ✅ Verify charts render if backtest completed

**Test Reset:**
1. Complete a backtest
2. Click "Run Backtest" again
3. ✅ Verify old progress clears
4. ✅ Verify new progress starts fresh

## Technical Details

**Zustand vs Redux:**
- Simpler API (no actions/reducers boilerplate)
- Smaller bundle size (~1KB vs ~10KB)
- No Provider wrapper needed
- Direct state updates (no immutability helpers)

**Zustand vs Context:**
- Better performance (no unnecessary re-renders)
- Easier to use (no Provider/Consumer)
- Built-in devtools support
- Middleware ecosystem (persist, immer, etc.)

## Conclusion

Zustand provides a lightweight, elegant solution for persisting backtest state across navigation. The implementation is minimal, type-safe, and significantly improves UX by allowing users to freely navigate the app without losing their backtest progress.
