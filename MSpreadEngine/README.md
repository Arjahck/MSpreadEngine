# MSpread: Malware Spreading Simulation and Visualization Tool

## Overview

MSpread is a comprehensive framework for modeling and visualizing malware propagation across networks—ranging from small corporate environments to country-wide infrastructures. Built with Python and NetworkX, MSpread provides a powerful simulation engine and REST API for analyzing malware spread patterns.

## Features

- **Multiple Malware Types**: Simulate worms, viruses, ransomware, and trojans with distinct behaviors
- **Network Topology Models**: Support for scale-free, small-world, random, and custom network topologies
- **Flexible Simulation Engine**: Time-step based simulation with customizable infection rates and spreading patterns
- **REST API**: FastAPI-based API for running simulations programmatically
- **Data Export**: JSON export of network topology and simulation results
- **Extensible Architecture**: Easy to add new malware types and network models

## Project Structure

```
malware_simulation_poc/
│
├── network_model/           # Graph-based network representation
│   ├── __init__.py
│   ├── network_graph.py     # NetworkX-based network model
│   └── ...
│
├── malware_engine/          # Malware spread logic
│   ├── __init__.py
│   ├── malware_base.py      # Base classes for malware types
│   ├── worm.py              # Worm-specific behavior
│   ├── virus.py             # Virus-specific behavior
│   ├── ransomware.py        # Ransomware-specific behavior
│   └── ...
│
├── simulation/              # Core simulation loop
│   ├── __init__.py
│   ├── simulator.py         # Main simulation engine
│   └── ...
│
├── api/                     # API layer (FastAPI)
│   ├── __init__.py
│   └── api.py              # API endpoints
│
├── data/                    # Input/output data
│   ├── input/
│   │   ├── network_topology.json
│   │   └── malware_params.json
│   └── output/
│       ├── simulation_results.json
│       └── ...
│
├── tests/                   # Unit/integration tests
│   ├── test_network_model.py
│   ├── test_malware_engine.py
│   └── ...
│
├── __init__.py
├── main.py                 # Application entry point
├── README.md               # This file
└── requriementes.txt   
```

## Installation

### Requirements

- Python 3.8+
- networkx
- fastapi
- uvicorn
- pydantic

### Setup

1. Clone or download the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Initialize the application:
   ```bash
   python main.py init
   ```

## Usage

### Initialize Configuration Files

```bash
python main.py init
```

This creates sample configuration files in `data/input/`:
- `network_topology.json`: Network configuration
- `malware_params.json`: Malware parameters

### Run API Server

```bash
python main.py run
```

The API will be available at `http://127.0.0.1:8000`

**API Documentation**: 
- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

### Run Demonstration Simulation

```bash
python main.py demo
```

This runs a sample simulation showing malware propagation across a 30-node scale-free network.

### Programmatic Usage

```python
from malware_simulation_poc.network_model import NetworkGraph
from malware_simulation_poc.malware_engine.malware_base import Worm
from malware_simulation_poc.simulation import Simulator

# Create network
network = NetworkGraph(network_type="scale_free")
network.generate_topology(num_nodes=50)

# Create malware
malware = Worm("worm_1", infection_rate=0.35)

# Run simulation
simulator = Simulator(network, malware)
simulator.initialize(["device_0"])
results = simulator.run(max_steps=100)

# Get statistics
stats = simulator.get_statistics()
print(f"Infected: {stats['total_infected']} / {stats['total_devices']}")
```

## API Endpoints

### POST `/api/v1/simulate`

Run a malware simulation.

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

## Configuration Files

### network_topology.json
```json
{
  "network_type": "scale_free",
  "num_nodes": 50,
  "topology_description": "Scale-free network topology"
}
```

### malware_params.json
```json
{
  "malware_profiles": [
    {
      "id": "worm_1",
      "type": "worm",
      "infection_rate": 0.4,
      "latency": 1
    }
  ]
}
```

## Testing

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

- [ ] Real-time visualization with Plotly/D3.js
- [ ] Multi-threaded simulation engine
- [ ] Machine learning for infection pattern prediction
- [ ] Integration with real network data
- [ ] Countermeasure modeling (firewalls, patches, quarantine)
- [ ] Advanced statistics and analytics

## License

MIT License

## Contact

For questions or contributions, please contact the development team.

## References

- NetworkX Documentation: https://networkx.org/
- FastAPI Documentation: https://fastapi.tiangolo.com/
- Graph Theory in Network Security: [Academic papers on malware propagation]
