# Node Definitions & Batch Logic

## Overview

The MSpreadEngine API now supports **node definitions** and **batch logic** to assign different attributes to groups of devices in your network. This enables realistic network segmentation where devices have different security levels, roles, or configurations.

## Features

### 1. Node Definitions (Batch Logic)
Define batches of nodes with specific attributes that will be applied sequentially.

### 2. Device Attributes
Each batch can have its own set of attributes:
- `admin_user`: Boolean (True/False)
- `device_type`: String (server, workstation, etc.)
- `os`: String (Windows, Linux, MacOS, etc.)
- `patch_status`: String (patched, unpatched, mixed)
- `firewall_enabled`: Boolean
- `antivirus`: Boolean or String

## How It Works

When you provide `node_definitions` in a simulation request:

1. **Topology Generation**: Network is created with `num_nodes` devices
2. **Batch Processing**: Attributes are applied sequentially to device groups
3. **Sequential Assignment**: First batch gets `device_0` to `device_(count-1)`, second batch gets `device_count` to `device_(count+count2-1)`, etc.

## API Usage

### Example: 70/30 Admin/Non-Admin Split

```json
{
  "network_config": {
    "num_nodes": 100,
    "network_type": "scale_free",
    "node_definitions": [
      {
        "count": 70,
        "attributes": {
          "admin_user": true,
          "device_type": "server"
        }
      },
      {
        "count": 30,
        "attributes": {
          "admin_user": false,
          "device_type": "workstation"
        }
      }
    ]
  },
  "malware_config": {
    "malware_type": "worm",
    "infection_rate": 0.35,
    "latency": 1
  },
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

### Example: Multiple Batches with Different Configurations

```json
{
  "network_config": {
    "num_nodes": 200,
    "network_type": "scale_free",
    "node_definitions": [
      {
        "count": 50,
        "attributes": {
          "admin_user": true,
          "device_type": "server",
          "firewall_enabled": true,
          "antivirus": true
        }
      },
      {
        "count": 100,
        "attributes": {
          "admin_user": true,
          "device_type": "workstation",
          "firewall_enabled": true,
          "antivirus": false
        }
      },
      {
        "count": 50,
        "attributes": {
          "admin_user": false,
          "device_type": "workstation",
          "firewall_enabled": false,
          "antivirus": false
        }
      }
    ]
  },
  "malware_config": {
    "malware_type": "virus",
    "infection_rate": 0.25,
    "latency": 2
  },
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

## Python/Programmatic Usage

```python
import requests
import json

API_BASE_URL = "http://localhost:8000"

# Define node batches
request_data = {
    "network_config": {
        "num_nodes": 100,
        "network_type": "scale_free",
        "node_definitions": [
            {"count": 70, "attributes": {"admin_user": True}},
            {"count": 30, "attributes": {"admin_user": False}}
        ]
    },
    "malware_config": {
        "malware_type": "worm",
        "infection_rate": 0.35,
        "latency": 1
    },
    "initial_infected": ["device_0"],
    "max_steps": 50
}

response = requests.post(
    f"{API_BASE_URL}/api/v1/simulate",
    json=request_data,
    timeout=60
)

if response.status_code == 200:
    results = response.json()
    print(f"Total Infected: {results['total_infected']}/{results['total_devices']}")
    print(f"Spread limited by admin_user attribute boundaries")
```

## WebSocket Support

Node definitions also work with WebSocket streaming:

```python
import asyncio
import websockets
import json

async def stream_simulation():
    async with websockets.connect("ws://localhost:8000/ws/simulate") as ws:
        payload = {
            "network_config": {
                "num_nodes": 100,
                "network_type": "scale_free",
                "node_definitions": [
                    {"count": 70, "attributes": {"admin_user": True}},
                    {"count": 30, "attributes": {"admin_user": False}}
                ]
            },
            "malware_config": {
                "malware_type": "worm",
                "infection_rate": 0.35,
                "latency": 1
            },
            "initial_infected": ["device_0"],
            "max_steps": 50
        }
        
        await ws.send(json.dumps(payload))
        
        while True:
            message = await ws.recv()
            data = json.loads(message)
            print(f"Message type: {data['type']}")
            if data['type'] == 'complete':
                print(f"Simulation finished: {data['statistics']}")
                break

asyncio.run(stream_simulation())
```

## Implementation Details

### API Components

**File**: `api/api.py`

1. **NodeDefinition Model**
   ```python
   class NodeDefinition(BaseModel):
       count: int              # Number of nodes in this batch
       attributes: Dict        # Attributes to apply to nodes
   ```

2. **NetworkConfig Update**
   ```python
   class NetworkConfig(BaseModel):
       num_nodes: int
       network_type: str = "scale_free"
       device_attributes: Optional[Dict] = None
       node_definitions: Optional[List[NodeDefinition]] = None  # NEW
   ```

3. **Helper Function**
   ```python
   def _apply_node_definitions(network, node_definitions: List[NodeDefinition]):
       """Apply batch logic to assign attributes to device groups"""
       node_id = 0
       for definition in node_definitions:
           for _ in range(definition.count):
               device_id = f"device_{node_id}"
               if device_id in network.graph.nodes():
                   network.set_device_attributes(device_id, **definition.attributes)
               node_id += 1
   ```

### Spread Logic Impact

When `admin_user=False` devices spread malware:
- They can **only spread to other non-admin devices**
- They **cannot spread to admin devices** (admin_user=True)

When `admin_user=True` devices spread malware:
- They can **spread to any neighboring device** (both admin and non-admin)

## Testing

Run the device attributes test with 70/30 split:

```bash
python test_api_demo.py -t 11
```

This test verifies:
- Node definitions are properly applied
- 70 devices are assigned as admin_user=True
- 30 devices are assigned as admin_user=False
- Malware spread respects the admin_user boundaries

## Compatibility

- **Backward Compatible**: Existing code without `node_definitions` continues to work
- **Optional**: `node_definitions` is an optional field in NetworkConfig
- **Works with**: Both HTTP REST API and WebSocket endpoints
- **Performance**: No performance impact for simulations without node definitions

## Future Enhancements

Possible extensions to batch logic:

1. **Weighted Attributes**: Probabilistic assignment of attributes
2. **Named Batches**: Label batches for easier reference in results
3. **Conditional Spread**: Different spread rules based on device_type combinations
4. **Device Groups**: Create logical groups for advanced analysis
5. **Migration Logic**: Change device attributes during simulation
