# MSpreadEngine: Malware Spreading Simulation Engine

## Overview

**MSpreadEngine** is the core simulation engine component of the **MSpread** platform. It provides a powerful framework for modeling and simulating malware propagation across networks—ranging from small corporate environments to country-wide infrastructures. Built with Python and NetworkX, MSpreadEngine enables realistic malware spread analysis through a flexible simulation engine and REST API.

### MSpread vs MSpreadEngine

- **MSpread**: The overall solution that includes visualization, analytics, and reporting tools (future)
- **MSpreadEngine**: The core engine (this folder) focused on malware simulation and API services

## Features

- **Multiple Malware Types**: Simulate worms, viruses, ransomware, and trojans with distinct behaviors
- **Network Topology Models**: Support for scale-free, small-world, random, and custom network topologies
- **Flexible Simulation Engine**: Time-step based simulation with customizable infection rates and spreading patterns
- **REST API**: FastAPI-based API for running simulations programmatically via HTTP
- **WebSocket Support**: Real-time simulation streaming with continuous step-by-step updates
- **CORS Enabled**: Cross-origin requests allowed for frontend integration
- **Extensible Architecture**: Easy to add new malware types and network models
- **Performance Optimized**: Multi-threaded network generation for large-scale simulations (30k+ nodes)

## Project Structure

```
MSpreadEngine/
│
├── network_model/              # Graph-based network representation
│   ├── __init__.py
│   └── network_graph.py        # NetworkX-based network model (optimized for large graphs)
│
├── malware_engine/             # Malware spread logic
│   ├── __init__.py
│   └── malware_base.py         # Base classes for malware types (Worm, Virus, Ransomware)
│
├── simulation/                 # Core simulation loop
│   ├── __init__.py
│   └── simulator.py            # Main simulation engine with time-step execution
│
├── api/                        # API layer (FastAPI)
│   ├── __init__.py
│   └── api.py                  # REST API endpoints for running simulations
│
├── tests/                      # Unit/integration tests
│   ├── test_network_model.py
│   ├── test_malware_engine.py
│   └── ...
│
├── main.py                     # Application entry point (CLI)
├── test_api_demo.py           # Comprehensive API test suite
├── __init__.py
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Installation

### Requirements

- Python 3.8+
- networkx >= 2.6
- fastapi >= 0.95.0
- uvicorn >= 0.21.0
- pydantic >= 1.10.0
- tqdm >= 4.60.0

### Setup

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Start API Server

```bash
python main.py run
```

The API will be available at `http://127.0.0.1:8000`

**Interactive API Documentation**: 
- Swagger UI: `http://127.0.0.1:8000/docs`

**Custom Host/Port:**
```bash
python main.py run --host 0.0.0.0              # Listen on all interfaces
python main.py run --port 8080                 # Custom port
python main.py run --reload                    # Enable auto-reload for development
```

### Run Demonstration Simulation

```bash
# Run with defaults (30k nodes, worm, 0.35 infection rate)
python main.py demo

# Custom parameters
python main.py demo --nodes 100                # Smaller network
python main.py demo --nodes 500 --type virus   # Different malware type
python main.py demo --topology small_world     # Different topology
python main.py demo --rate 0.5                 # Higher infection rate
python main.py demo --steps 100                # More simulation steps

# Full example with all parameters
python main.py demo --nodes 200 --topology scale_free --type ransomware --rate 0.3 --steps 50
```

### Test the API

Use the comprehensive test suite to verify API functionality:

```bash
# Terminal 1: Start the API server
python main.py run

# Terminal 2: Run the test suite
python test_api_demo.py
```

The test suite (`test_api_demo.py`) includes:
- ✅ Server health checks
- ✅ All malware type simulations (worm, virus, ransomware)
- ✅ Different network topologies comparison
- ✅ Infection rate impact analysis
- ✅ Multiple initial infection scenarios
- ✅ WebSocket real-time streaming tests
- ✅ Color-coded test results with detailed output

### Programmatic Usage

```python
from network_model import NetworkGraph
from malware_engine.malware_base import Worm
from simulation import Simulator

# Create network
network = NetworkGraph(network_type="scale_free")
network.generate_topology(num_nodes=500, use_parallel=True, num_workers=8)

# Create malware
malware = Worm("worm_1", infection_rate=0.35)

# Run simulation
simulator = Simulator(network, malware)
simulator.initialize(["device_0"])
results = simulator.run(max_steps=100)

# Get statistics
stats = simulator.get_statistics()
print(f"Infected: {stats['total_infected']} / {stats['total_devices']}")
print(f"Steps: {stats['total_steps']}")
print(f"Percentage: {stats['infection_percentage']:.2f}%")
```

## API Endpoints

### POST `/api/v1/simulate`

Run a malware simulation (HTTP request - returns complete results).

**Request Body**:
```json
{
  "network_config": {
    "num_nodes": 50,
    "network_type": "scale_free"
  },
  "malware_config": {
    "malware_type": "worm",
    "infection_rate": 0.35,
    "latency": 1
  },
  "initial_infected": ["device_0"],
  "max_steps": 100
}
```

**Response**:
```json
{
  "total_steps": 15,
  "total_devices": 50,
  "total_infected": 42,
  "infection_percentage": 84.0,
  "malware_type": "worm",
  "history": [...]
}
```

### WebSocket `/ws/simulate`

Run a malware simulation with real-time streaming updates (WebSocket).

**Connection URL**: `ws://localhost:8000/ws/simulate`

**Client sends (initial configuration)**:
```json
{
  "network_config": {
    "num_nodes": 50,
    "network_type": "scale_free"
  },
  "malware_config": {
    "malware_type": "worm",
    "infection_rate": 0.35,
    "latency": 1
  },
  "initial_infected": ["device_0"],
  "max_steps": 100
}
```

**Server responses** (streaming):

1. **Initialization Message**:
```json
{
  "type": "initialized",
  "total_devices": 50,
  "initial_infected": 1
}
```

2. **Step Updates** (one per simulation step):
```json
{
  "type": "step",
  "step": 1,
  "newly_infected": 5,
  "total_infected": 6,
  "devices_infected": ["device_1", "device_2", ...]
}
```

3. **Completion Message**:
```json
{
  "type": "complete",
  "statistics": {
    "total_steps": 15,
    "total_devices": 50,
    "total_infected": 42,
    "infection_percentage": 84.0,
    "malware_type": "worm",
    "history": [...]
  }
}
```

4. **Error Message** (if applicable):
```json
{
  "type": "error",
  "message": "Error description"
}
```

**WebSocket Advantages**:
- Real-time step-by-step progress updates
- Ideal for live dashboards and visualization
- Lower latency compared to polling HTTP requests
- Enables animated network infection spreading display

**Example Client Code** (Python):
```python
import asyncio
import websockets
import json

async def run_simulation():
    async with websockets.connect('ws://localhost:8000/ws/simulate') as ws:
        # Send simulation config
        config = {
            "network_config": {"num_nodes": 100, "network_type": "scale_free"},
            "malware_config": {"malware_type": "worm", "infection_rate": 0.35, "latency": 1},
            "initial_infected": ["device_0"],
            "max_steps": 100
        }
        await ws.send(json.dumps(config))
        
        # Receive updates
        while True:
            message = await ws.recv()
            data = json.loads(message)
            
            if data["type"] == "step":
                print(f"Step {data['step']}: {data['newly_infected']} newly infected")
            elif data["type"] == "complete":
                print(f"Done! Total infected: {data['statistics']['total_infected']}")
                break

asyncio.run(run_simulation())
```

### GET `/health`

Health check endpoint.

**Response**:
```json
{
  "status": "healthy"
}
```

## Malware Types

### Worm
- **Characteristics**: Self-replicating, network-aware, aggressive spreading
- **Infection Rate**: High (typically 0.3-0.5)
- **Spread Pattern**: Active spreading to all neighbors

### Virus
- **Characteristics**: Requires user interaction, selective spreading
- **Infection Rate**: Medium (typically 0.2-0.4)
- **Spread Pattern**: Reduced infection rate compared to worms

### Ransomware
- **Characteristics**: Careful spreading, file encryption, ransom demands
- **Infection Rate**: Medium-High (typically 0.25-0.45)
- **Spread Pattern**: Balanced between detection avoidance and infection

## Network Topology Models

### Scale-Free
Power-law degree distribution. Realistic for real-world networks.
```python
NetworkGraph(network_type="scale_free")
```

### Small-World
High clustering with low average path length.
```python
NetworkGraph(network_type="small_world")
```

### Random (Erdős-Rényi)
Randomly connected nodes.
```python
NetworkGraph(network_type="random")
```

### Complete
Fully connected network.
```python
NetworkGraph(network_type="complete")
```

## Unit Tests

Run unit tests:

```bash
python -m pytest tests/
```

Run specific test file:

```bash
python -m pytest tests/test_network_model.py
```

## Development

### Adding a New Malware Type

1. Extend `Malware` class in `malware_engine/malware_base.py`
2. Implement `spread()` and `get_behavior()` methods
3. Add unit tests in `tests/test_malware_engine.py`

### Adding a Custom Network Topology

1. Extend `NetworkGraph` class in `network_model/network_graph.py`
2. Modify `generate_topology()` method
3. Test with sample data

## Performance Considerations

- **Large Networks**: For 1000+ nodes, consider using sparse network representations
- **Simulation Steps**: Typical malware reaches equilibrium in 20-100 steps
- **Parallelization**: Can parallelize independent simulation runs

## Future Enhancements

- [X] Websocket implementation
- [ ] Improve amount of parameter for nodes and malwares
- [ ] Countermeasure modeling (firewalls, patches, quarantine)
- [ ] Multi-threaded simulation engine
- [ ] Machine learning for infection pattern prediction
- [ ] Advanced statistics and analytics
- [ ] LLMVirus simulation (PoC - Virus)
- [ ] Real-time visualization with Plotly/D3.js

## License

MIT License

## References

- NetworkX Documentation: https://networkx.org/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Graph Theory in Network Security: [Academic papers on malware propagation]
