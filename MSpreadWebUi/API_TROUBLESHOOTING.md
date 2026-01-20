# API Connection Troubleshooting Guide

## Problem
MSpreadWebUI shows "API server is not responding" even though the API is running and responds with 200 OK.

## Root Cause
This is a **CORS (Cross-Origin Resource Sharing)** issue. The browser blocks requests from one origin (http://localhost:5173) to another (http://localhost:8000) unless the API includes proper CORS headers.

## Solution Steps

### 1. Enable CORS in MSpreadEngine API

Open your `MSpreadEngine/api/api.py` or `main.py` and add CORS middleware:

```python
from fastapi import FastAPI
from fastapi.cors import CORSMiddleware

app = FastAPI(title="MSpreadEngine API", version="1.0.0")

# Add CORS middleware (place this BEFORE any route definitions)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # MSpreadWebUI Vite dev server
        "http://localhost:3000",       # Alternative port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Your existing routes...
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/simulate")
async def simulate(request):
    # Your simulation code...
    pass
```

### 2. Restart MSpreadEngine

```bash
# Kill any running instance (Ctrl+C)
# Then restart:
python main.py run
```

You should see output like:
```
INFO:     Started server process [xxxx]
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 3. Verify the Fix

#### Option A: Using Browser DevTools
1. Open http://localhost:5173/
2. Open DevTools: Press **F12**
3. Go to **Network** tab
4. Click "Check" button in Simulation Control panel
5. Look for `/health` request
6. In the Response headers, you should see:
   ```
   access-control-allow-origin: http://localhost:5173
   access-control-allow-methods: GET, POST, OPTIONS
   access-control-allow-headers: *
   ```

If these headers are missing → CORS is NOT enabled yet.

#### Option B: Using curl from terminal

```bash
curl -i -X GET http://localhost:8000/health
```

Look for these headers in the response:
```
Access-Control-Allow-Origin: http://localhost:5173
Access-Control-Allow-Methods: GET, POST, OPTIONS
```

### 4. Test the WebUI

1. Refresh MSpreadWebUI page (Ctrl+R)
2. In Simulation Control panel, click **"Check"** button
3. Should show green dot and "Connected" status
4. Configure simulation and click **"Run Simulation"**
5. Results should display in Network and Analytics tabs

## Debugging Checklist

### ✓ API Server Checks
- [ ] MSpreadEngine running on localhost:8000?
  ```bash
  curl http://localhost:8000/health
  ```
  Should return: `{"status":"healthy"}`

- [ ] CORS middleware added to API code?
  - [ ] `from fastapi.cors import CORSMiddleware`
  - [ ] `app.add_middleware(CORSMiddleware, ...)`
  - [ ] Middleware added BEFORE routes

- [ ] API restarted after changes?
  ```bash
  # Stop with Ctrl+C, then:
  python main.py run
  ```

### ✓ WebUI Checks
- [ ] MSpreadWebUI running on localhost:5173?
  ```bash
  npm run dev
  ```

- [ ] Browser DevTools checked (F12)?
  - [ ] Console tab for errors
  - [ ] Network tab to see API calls
  - [ ] Response headers for CORS headers

### ✓ Browser Checks
- [ ] No CORS error in console?
  - [ ] "No 'Access-Control-Allow-Origin' header"?
  - [ ] "CORS policy: Cross-Origin Request Blocked"?

- [ ] Try different browser?
  - Chrome, Firefox, Safari, Edge

### ✓ Connectivity Checks
- [ ] Firewall blocking port 8000?
  - Try: `telnet localhost 8000`

- [ ] Antivirus blocking requests?
  - Check antivirus logs

## Common CORS Error Messages

### "No 'Access-Control-Allow-Origin' header"
**Means:** API doesn't have CORS middleware
**Fix:** Add CORSMiddleware to MSpreadEngine API

### "CORS policy: Cross-Origin Request Blocked"
**Means:** Browser blocked the request
**Fix:** Check API CORS headers include your origin

### "Failed to fetch"
**Means:** Could be CORS or connection issue
**Fix:** 
1. Check API is running: `curl http://localhost:8000/health`
2. Check API includes CORS headers
3. Check firewall/antivirus

## Production Deployment

When deploying to production, use restrictive CORS:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://yourdomain.com",
        "https://www.yourdomain.com",
    ],
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["Content-Type"],
)
```

## Complete Example: api.py with CORS

```python
from fastapi import FastAPI
from fastapi.cors import CORSMiddleware
from pydantic import BaseModel

# Models
class NetworkConfig(BaseModel):
    num_nodes: int
    network_type: str

class MalwareConfig(BaseModel):
    malware_type: str
    infection_rate: float
    latency: int = 1

class SimulationRequest(BaseModel):
    network_config: NetworkConfig
    malware_config: MalwareConfig
    initial_infected: list[str] = ["device_0"]
    max_steps: int

# Create app
app = FastAPI(
    title="MSpreadEngine API",
    version="1.0.0",
    description="Malware Spread Simulation Engine"
)

# CORS MUST come BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS", "DELETE", "PUT"],
    allow_headers=["*"],
)

# Routes
@app.get("/health")
async def health():
    return {"status": "healthy"}

@app.post("/api/v1/simulate")
async def simulate(request: SimulationRequest):
    try:
        # Your simulation logic here
        # ...
        return {
            "total_steps": 15,
            "total_devices": 50,
            "total_infected": 42,
            "infection_percentage": 84.0,
            "malware_type": "worm",
            "history": []
        }
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Still Having Issues?

1. **Check browser console (F12 → Console)** for exact error
2. **Check Network tab** to see API response headers
3. **Check API terminal** for any error messages
4. **Verify CORS code is actually in your api.py** (not just added to a comment)
5. **Confirm you restarted the API** after making changes
6. **Try accessing from curl** to rule out browser issues:
   ```bash
   curl -i http://localhost:8000/health
   ```

If still stuck, share the exact error message from the browser console (F12).
