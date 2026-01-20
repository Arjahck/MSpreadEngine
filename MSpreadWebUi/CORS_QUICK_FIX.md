# Quick Fix: CORS for MSpreadEngine

## The Problem
✗ MSpreadWebUI (localhost:5173) → Cannot reach MSpreadEngine (localhost:8000)
Browser shows: "API server is not responding"
But API is running and returns 200 OK

## The Solution
Add 6 lines to `MSpreadEngine/api/api.py` (or `main.py`):

```python
from fastapi.cors import CORSMiddleware

app = FastAPI(...)

# ADD THIS (before any @app.get/@app.post routes):
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Steps to Fix

### 1. Open MSpreadEngine API file
```
MSpreadEngine/api/api.py
# or
MSpreadEngine/main.py
```

### 2. Add import at the top
```python
from fastapi.cors import CORSMiddleware
```

### 3. Add middleware after `app = FastAPI(...)`
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

**Important:** Add this BEFORE any `@app.get()` or `@app.post()` route definitions!

### 4. Restart API
```bash
# Press Ctrl+C to stop current process
# Then:
python main.py run
```

### 5. Refresh WebUI
- Go to http://localhost:5173/
- Press F5 to refresh
- Click "Check" button → should show green "Connected"

## Verification

Open DevTools (F12) → Network tab → Click "Check" in WebUI

You should see these response headers:
```
access-control-allow-origin: http://localhost:5173
access-control-allow-methods: *
access-control-allow-headers: *
```

## Complete Example

Here's what the top of your api/api.py should look like:

```python
from fastapi import FastAPI
from fastapi.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="MSpreadEngine API", version="1.0.0")

# CORS Middleware - MUST be before routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Now add your routes
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/simulate")
async def simulate(request):
    # Your code...
    pass
```

That's it! The CORS issue should be fixed.

For detailed troubleshooting, see [API_TROUBLESHOOTING.md](API_TROUBLESHOOTING.md)
