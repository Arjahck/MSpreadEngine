# WebSocket API Documentation

## Overview

The WebSocket endpoint provides **real-time streaming** of simulation results step-by-step, unlike the HTTP REST endpoint which returns complete results only after simulation finishes.

**Endpoint**: `ws://localhost:8000/ws/simulate`

## Why WebSocket vs HTTP?

| Feature | HTTP REST | WebSocket |
|---------|-----------|-----------|
| **Response Type** | Complete results at end | Real-time streaming updates |
| **Wait Time** | Long (entire simulation) | Streaming (updates each step) |
| **Use Case** | Batch processing | Live monitoring, dashboards |
| **Overhead** | Single connection | Persistent connection |

## Connection Protocol

### 1. Connect to WebSocket
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/simulate");
```

### 2. Send Configuration (Same as HTTP POST)
```javascript
ws.onopen = () => {
  const config = {
    "network_config": {
      "num_nodes": 100,
      "network_type": "scale_free",
      "node_definitions": [
        {"count": 70, "attributes": {"admin_user": true}},
        {"count": 30, "attributes": {"admin_user": false}}
      ],
      "node_distribution": "random"
    },
    "malware_config": {
      "malware_type": "worm",
      "infection_rate": 0.35,
      "latency": 1
    },
    "initial_infected": ["device_0"],
    "max_steps": 50
  };
  
  ws.send(JSON.stringify(config));
};
```

### 3. Receive Streaming Updates
```javascript
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  console.log(`Step ${update.step}: ${update.infected_count} infected`);
};
```

### 4. Handle Completion
```javascript
ws.onclose = () => {
  console.log("Simulation complete");
};
```

## Message Format

### Outgoing (Client → Server)

Identical to HTTP POST body:
```json
{
  "network_config": {...},
  "malware_config": {...},
  "initial_infected": [...],
  "max_steps": 50
}
```

### Incoming (Server → Client)

Real-time update messages:
```json
{
  "step": 1,
  "infected_count": 5,
  "total_nodes": 100,
  "newly_infected": ["device_45", "device_23", ...],
  "timestamp": 1234567890.123
}
```

## Complete Examples

### Python Example
```python
import asyncio
import websockets
import json

async def run_simulation():
    uri = "ws://localhost:8000/ws/simulate"
    
    config = {
        "network_config": {
            "num_nodes": 100,
            "network_type": "scale_free",
            "node_definitions": [
                {"count": 70, "attributes": {"admin_user": True}},
                {"count": 30, "attributes": {"admin_user": False}}
            ],
            "node_distribution": "random"
        },
        "malware_config": {
            "malware_type": "worm",
            "infection_rate": 0.35,
            "latency": 1
        },
        "initial_infected": ["device_0"],
        "max_steps": 50
    }
    
    async with websockets.connect(uri) as websocket:
        # Send configuration
        await websocket.send(json.dumps(config))
        
        # Receive updates
        while True:
            try:
                message = await websocket.recv()
                update = json.parse(message)
                print(f"Step {update['step']}: {update['infected_count']} infected")
            except websockets.exceptions.ConnectionClosed:
                break

asyncio.run(run_simulation())
```

### JavaScript/Browser Example
```javascript
function simulateMalware() {
  const ws = new WebSocket("ws://localhost:8000/ws/simulate");
  
  ws.onopen = () => {
    const config = {
      network_config: {
        num_nodes: 100,
        network_type: "scale_free",
        node_definitions: [
          {count: 70, attributes: {admin_user: true}},
          {count: 30, attributes: {admin_user: false}}
        ],
        node_distribution: "random"
      },
      malware_config: {
        malware_type: "worm",
        infection_rate: 0.35,
        latency: 1
      },
      initial_infected: ["device_0"],
      max_steps: 50
    };
    
    ws.send(JSON.stringify(config));
  };
  
  ws.onmessage = (event) => {
    const update = JSON.parse(event.data);
    
    // Update UI in real-time
    document.getElementById("step").textContent = update.step;
    document.getElementById("infected").textContent = update.infected_count;
    document.getElementById("progress").style.width = 
      (update.infected_count / update.total_nodes * 100) + "%";
    
    console.log(`Step ${update.step}: ${update.infected_count}/${update.total_nodes}`);
  };
  
  ws.onerror = (error) => {
    console.error("WebSocket error:", error);
  };
  
  ws.onclose = () => {
    console.log("Simulation complete");
  };
}
```

### cURL (Connect but can't stream well)
```bash
# WebSockets don't work well with curl, use websocat instead:
websocat ws://localhost:8000/ws/simulate

# Then paste JSON:
{"network_config": {...}, "malware_config": {...}, ...}
```

## Configuration (Same as HTTP)

### Network Configuration
- `num_nodes`: Number of devices
- `network_type`: "scale_free", "small_world", "random", "complete"
- `device_attributes`: Optional, applied to ALL devices
- `node_definitions`: Optional, per-batch attributes with `count` and `attributes`
- `node_distribution`: "sequential" (clustered) or "random" (mixed)

### Malware Configuration
- `malware_type`: "worm", "virus", "ransomware"
- `infection_rate`: 0.0-1.0 (spread probability)
- `latency`: Integer, steps before spread can occur

### Simulation Parameters
- `initial_infected`: List of device IDs to start infected
- `max_steps`: Maximum simulation steps

## Error Handling

```javascript
ws.onerror = (event) => {
  console.error("WebSocket error:", event);
};

ws.onclose = (event) => {
  if (event.wasClean) {
    console.log("Clean close");
  } else {
    console.log("Abnormal close:", event.code);
  }
};
```

## Use Cases

### 1. **Live Dashboard**
Stream updates to a real-time dashboard showing infection progress:
```javascript
// Update progress bar, timeline, device status in real-time
ws.onmessage = (event) => {
  updateProgressBar(event.data.infected_count);
  updateTimeline(event.data.step);
};
```

### 2. **Batch Processing**
Run multiple simulations and collect results:
```javascript
async function batchSimulate(configs) {
  for (const config of configs) {
    await runSimulation(config);
  }
}
```

### 3. **Early Stopping**
Stop simulation if certain threshold reached:
```javascript
ws.onmessage = (event) => {
  if (event.data.infected_count > threshold) {
    ws.close(); // Stop simulation
  }
};
```

### 4. **Analytics Collection**
Collect all step-by-step data for analysis:
```javascript
const steps = [];
ws.onmessage = (event) => {
  steps.push(event.data);
};
ws.onclose = () => {
  analyzeSpreadPattern(steps);
};
```

## Comparison with HTTP REST

### HTTP REST (`/api/v1/simulate`)
```python
import requests

response = requests.post(
  "http://localhost:8000/api/v1/simulate",
  json=config
)

# Waits entire simulation...
results = response.json()
print(f"Final: {results['total_infected']} infected")
```

**Pros:**
- Simpler, stateless
- Works with all HTTP clients
- Easy error handling

**Cons:**
- Long wait for response
- No real-time monitoring
- Harder to integrate with dashboards

### WebSocket (`/ws/simulate`)
```javascript
const ws = new WebSocket("ws://localhost:8000/ws/simulate");
ws.send(JSON.stringify(config));

ws.onmessage = (event) => {
  // Real-time updates every step!
  console.log(event.data);
};
```

**Pros:**
- Real-time streaming
- Perfect for dashboards
- Can react mid-simulation

**Cons:**
- Persistent connection
- Slightly more complex
- Need WebSocket client library

## Testing WebSocket

### Using websocat (command-line tool)
```bash
# Install: cargo install websocat (requires Rust)
# Or: npm install -g websocat

websocat ws://localhost:8000/ws/simulate
# Then paste: {"network_config":{...}, "malware_config":{...}, ...}
```

### Using Python websockets
```bash
pip install websockets
# Then use the Python example above
```

### Using Browser DevTools
```javascript
// Open browser console
ws = new WebSocket("ws://localhost:8000/ws/simulate");
ws.send(JSON.stringify({...}));
ws.onmessage = (e) => console.log(e.data);
```

## Summary

| Aspect | Details |
|--------|---------|
| **Endpoint** | `ws://localhost:8000/ws/simulate` |
| **Configuration** | Identical to HTTP REST `/api/v1/simulate` |
| **Response** | Stream of step-by-step updates |
| **Use When** | Need real-time monitoring, dashboards, or early stopping |
| **Best For** | Live visualization, analytics collection, interactive apps |

---

**Note**: WebSocket is not documented in Swagger UI (which only supports HTTP/REST), but uses identical request/response models as the REST endpoint for compatibility.
