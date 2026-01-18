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
├── Docs/                      # Additional documentation
│   ├── ADMIN_USER_LOGIC.md    # Privilege-based spread logic
│   ├── NODE_DEFINITIONS.md    # Batch definition guide
│   ├── DEVICE_ATTRIBUTES.md   # Supported device attributes
│   ├── WEBSOCKET_DOCUMENTATION.md # Real-time streaming API
│   ├── STATISTICS_GUIDE.md    # Guide to network & simulation metrics
│   └── ARCHITECTURE_DIAGRAM.md # System architecture overview
│
├── main.py                     # Application entry point (CLI)
├── test_api_demo.py            # Comprehensive API test suite
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

# Run specific tests
python test_api_demo.py -t 3        # Run test 3 (Worm Simulation)
python test_api_demo.py -t 9 10 11  # Run WebSocket tests (9, 10, 11)
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
from malware_engine.malware_base import Malware
from simulation import Simulator

# Create network
network = NetworkGraph(network_type="scale_free")
network.generate_topology(num_nodes=500, use_parallel=True, num_workers=8)

# Create malware
malware = Malware("malware_1", infection_rate=0.5, spread_pattern="bfs")

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

## Configurable Malware

MSpreadEngine uses a unified, highly configurable malware model. Instead of hardcoded types, you can define malware behavior using parameters.

### Configuration Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `malware_type` | string | `"custom"` | Label for categorization (worm, virus, etc.) |
| `infection_rate` | float | `0.5` | Probability of infection (0.0 - 1.0) |
| `latency` | int | `1` | Steps before newly infected node becomes infectious |
| `spread_pattern` | string | `"random"` | `"random"` (probabilistic), `"bfs"` (aggressive), `"dfs"` (stealthy) |
| `target_os` | list | `None` | List of OS strings to target (e.g., `["windows"]`). If None, targets all. |
| `target_node_types` | list | `None` | List of node types to target. If None, targets all. |
| `avoids_admin` | boolean | `False` | If True, blocks spread from non-admin source to admin target. |
| `requires_interaction` | boolean | `False` | If True, reduces effective infection rate by 40%. |

### Legacy Types (Concept)

While the engine uses a single class, you can simulate classic types by configuring these parameters:

- **Worm**: `infection_rate=0.5`, `spread_pattern="bfs"`
- **Virus**: `infection_rate=0.3`, `requires_interaction=True`
- **Ransomware**: `infection_rate=0.4`, `latency=3`

## Network Topology Models

### Scale-Free
Power-law degree distribution. Realistic for real-world networks.

### Small-World
High clustering with low average path length.


### Random (Erdős-Rényi)
Randomly connected nodes.

### Complete
Fully connected network.

## Device Attributes

Each device (node) in the network can have attributes that define its characteristics. These attributes are used to simulate realistic network conditions and device configurations.

### Available Attributes

| Attribute | Type | Default | Description |
|-----------|------|---------|-------------|
| `os` | string | `None` | Operating system (e.g., "Windows Server 2019", "Ubuntu 20.04", "macOS") |
| `patch_status` | string | `None` | Patching level (e.g., "patched", "unpatched", "partially_patched") |
| `device_type` | string | `"workstation"` | Type of device (e.g., "workstation", "server", "router", "IoT") |
| `firewall_enabled` | boolean | `None` | Whether firewall is enabled on the device |
| `antivirus` | boolean | `None` | Whether antivirus software is installed |
| `admin_user` | boolean | `True` | Whether malware can spread FROM this device (affects lateral movement) |

### Setting Device Attributes

#### Via API (HTTP/WebSocket)

**Example Request with Device Attributes**:
```json
{
  "network_config": {
    "num_nodes": 100,
    "network_type": "scale_free",
    "device_attributes": {
      "os": "Windows Server 2019",
      "patch_status": "patched",
      "device_type": "server",
      "firewall_enabled": true,
      "antivirus": true,
      "admin_user": true
    }
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

#### Programmatically (Python)

```python
from network_model import NetworkGraph
from malware_engine.malware_base import Malware
from simulation import Simulator

# Create network with device attributes
network = NetworkGraph(network_type="scale_free")
network.generate_topology(
    num_nodes=100,
    device_attributes={
        "os": "Windows Server 2019",
        "patch_status": "patched",
        "device_type": "server",
        "firewall_enabled": True,
        "antivirus": True,
        "admin_user": True
    }
)

# Or add/update attributes for specific devices
network.set_device_attributes("device_0", 
    os="Windows 10",
    patch_status="unpatched",
    admin_user=False
)

# Get device attributes
attrs = network.get_device_attributes("device_0")
print(attrs)
```

### Default Behavior

- When no `device_attributes` are provided, all nodes are created with default values
- **Important**: By default, `admin_user=True` for all devices, allowing normal malware spread
- Other attributes default to `None`, which means "not specified" (can be used for future logic)

### Impact on Simulation

- **`admin_user=False`**: Device **cannot spread** malware to neighboring devices with `admin_user=True` (lateral movement is blocked by privilege restrictions)
- **`admin_user=True`**: Device can spread malware **normally to all neighbors** regardless of their admin status
- **Practical Effect**: Non-admin (unprivileged) user accounts cannot propagate malware to admin-protected devices, simulating realistic operating system privilege boundaries
- **Future Implementation**: Other attributes can be used to:
  - Adjust infection rates based on antivirus presence
  - Affect spread based on patch status
  - Block spread based on firewall configuration
  - Create device-specific vulnerabilities

## Development

### Adding a New Malware Type

1. Extend `Malware` class in `malware_engine/malware_base.py`
2. Implement `spread()` and `get_behavior()` methods
3. Add unit tests in `tests/test_malware_engine.py`

### Adding a Custom Network Topology

1. Extend `NetworkGraph` class in `network_model/network_graph.py`
2. Modify `generate_topology()` method
3. Test with sample data

## Future Enhancements

- [X] Websocket implementation
- [X] Improve amount of parameter for nodes 
- [X] Improve amount of parameter for malwares
- [X] Redo the malware_base.py class structure (one class malware ony) 
- [ ] Countermeasure modeling (firewalls, patches, quarantine)
- [ ] Vectorization and batch processing for simulation engine
- [ ] Machine learning for infection pattern prediction (Graph Neural Network (GNN) on real-world network datasets for network_model, Reinforcement Learning (RL) Agents for simulation)
- [ ] Advanced statistics anda nalytics
- [ ] Polymorphic/Metamorphic Malware Simulation (PoC - Virus)
- [ ] Real-time visualization with Plotly/D3.js

## License

MIT License

## References

### Technical Documentation
- **NetworkX**: https://networkx.org/
- **FastAPI**: https://fastapi.tiangolo.com/

### Academic Papers & Research

#### Malware Propagation & Network Theory
- **Epidemic Spreading in Scale-Free Networks**  
  *Pastor-Satorras, R., & Vespignani, A. (2001). Physical Review Letters.*  
  Foundational paper on how viruses spread in scale-free topologies (like the one implemented in `network_graph.py`).

- **Directed-Graph Epidemiological Models of Computer Viruses**  
  *Kephart, J. O., & White, S. R. (1991). IEEE Symposium on Security and Privacy.*  
  Classic model for understanding viral spread probabilities and latency.

#### Graph Neural Networks (GNN)
- **Graph Neural Networks: A Review of Methods and Applications**  
  *Zhou, J., et al. (2020). AI Open.*  
  Comprehensive guide for implementing GNNs, relevant for future "Machine learning for infection pattern prediction".

- **Deep Learning for Spatiotemporal Epidemic Modeling**  
  *Various Authors (Recent field)*  
  Relevant for training models to predict the "next victim" in the simulation.

- **BlackMamba: AI-Synthesized Polymorphic Malware**  
  *Anderson, H., & Ahuja, S. (2023).*  
  Demonstrates malware that uses an LLM to dynamically **rewrite its own code** at runtime (shape-shifting/recoding) to evade EDR detection, perfectly matching the "recode itself" concept.

#### AI-Driven Malware Mutation (Polymorphic/Metamorphic)
- **Generating Adversarial Malware Examples for Black-Box Attacks based on GAN**  
  *Hu, W., & Tan, Y. (2017). arXiv preprint arXiv:1702.05983.*  
  Seminal work on using Generative Adversarial Networks (GANs) to generate "shape-sh