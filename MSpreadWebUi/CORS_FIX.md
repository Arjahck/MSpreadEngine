# CORS Configuration Fix for MSpreadEngine

## Problem
The MSpreadWebUI running on `http://localhost:5173/` cannot communicate with the MSpreadEngine API on `http://localhost:8000/` due to CORS (Cross-Origin Resource Sharing) restrictions.

Even though the API responds with 200 OK, the browser blocks the response because the API doesn't include proper CORS headers.

## Solution
Add CORS middleware to the MSpreadEngine FastAPI server.

### Step 1: Update MSpreadEngine/requirements.txt

Add the following line to include the CORS middleware library:
```
python-multipart>=0.0.5
```

Or if you're using FastAPI >= 0.93, it's already included. Just ensure you have FastAPI installed.

### Step 2: Update MSpreadEngine/api/api.py

Add CORS middleware to your FastAPI app. Here's the updated code:

```python
from fastapi import FastAPI
from fastapi.cors import CORSMiddleware
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(title="MSpreadEngine API", version="1.0.0")

# Add CORS middleware - Allow requests from MSpreadWebUI
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Local Vite dev server
        "http://localhost:3000",       # Alternative local port
        "http://127.0.0.1:5173",       # 127.0.0.1 variant
        "http://127.0.0.1:3000",       # Alternative
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rest of your API code follows...
```

### Step 3: If using main.py CLI

Make sure the FastAPI app setup in your `main.py` includes the CORS configuration:

```python
from fastapi.cors import CORSMiddleware

def create_app():
    app = FastAPI(title="MSpreadEngine API", version="1.0.0")
    
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            "http://localhost:5173",
            "http://localhost:3000",
            "http://127.0.0.1:5173",
            "http://127.0.0.1:3000",
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Rest of your app setup...
    return app
```

## Testing the Fix

### 1. Restart MSpreadEngine API
```bash
python main.py run
```

### 2. Open MSpreadWebUI
```bash
npm run dev
```

### 3. Test the Health Check
- Open http://localhost:5173/
- Click "Check" button in Simulation Control panel
- Should now show green "Connected" status

### 4. Check Browser Console
Open DevTools (F12) → Console tab and verify no CORS errors appear.

### 5. Run a Simulation
- Configure simulation parameters
- Click "Run Simulation"
- Should complete successfully

## Debugging

If it still doesn't work, check the browser console for errors:

1. **F12 → Network tab**: Look for the API requests
2. **F12 → Console tab**: Check for specific error messages
3. **API Server logs**: Check MSpreadEngine terminal for actual errors

### Common CORS Error Messages
- `"No 'Access-Control-Allow-Origin' header"`
- `"CORS policy: Cross-Origin Request Blocked"`
- `"has been blocked by CORS policy"`

All of these mean the API server isn't returning CORS headers, which the CORS middleware fix addresses.

## Production Deployment

For production, use more restrictive CORS settings:

```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://your-domain.com",
        "https://www.your-domain.com",
    ],
    allow_credentials=True,
    allow_methods=["POST", "GET", "OPTIONS"],
    allow_headers=["Content-Type"],
)
```

## Complete api.py Example

Here's a complete example of what your api.py should look like:

```python
from fastapi import FastAPI
from fastapi.cors import CORSMiddleware

from network_model import NetworkGraph
from malware_engine.malware_base import Worm, Virus, Ransomware
from simulation import Simulator
from pydantic import BaseModel

# Define request/response models
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

# Create FastAPI app
app = FastAPI(
    title="MSpreadEngine API",
    version="1.0.0",
    description="Malware Spread Simulation Engine API"
)

# Add CORS middleware BEFORE routes
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",      # Vite dev server
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type"],
)

# Health check endpoint
@app.get("/health")
async def health():
    return {"status": "healthy"}

# Simulation endpoint
@app.post("/api/v1/simulate")
async def simulate(request: SimulationRequest):
    try:
        # Your simulation logic here
        network = NetworkGraph(network_type=request.network_config.network_type)
        network.generate_topology(num_nodes=request.network_config.num_nodes)
        
        malware_class = {
            "worm": Worm,
            "virus": Virus,
            "ransomware": Ransomware,
        }[request.malware_config.malware_type]
        
        malware = malware_class(
            request.malware_config.malware_type,
            infection_rate=request.malware_config.infection_rate
        )
        
        simulator = Simulator(network, malware)
        simulator.initialize(request.initial_infected)
        simulator.run(max_steps=request.max_steps)
        
        # Return results
        return {
            "total_steps": simulator.get_statistics()["total_steps"],
            "total_devices": simulator.get_statistics()["total_devices"],
            "total_infected": simulator.get_statistics()["total_infected"],
            "infection_percentage": simulator.get_statistics()["infection_percentage"],
            "malware_type": request.malware_config.malware_type,
            "history": simulator.get_history(),
        }
    except Exception as e:
        return {"error": str(e)}, 500

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
```

## Summary

The fix requires adding just a few lines to your MSpreadEngine API:

1. Import `CORSMiddleware` from `fastapi.cors`
2. Call `app.add_middleware()` with appropriate origins
3. Restart the API server

After this, all CORS issues should be resolved and the MSpreadWebUI will communicate successfully with the API.
