# Architecture: Swagger Documentation Enhancement

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                     MSpreadEngine API                           │
│                    http://localhost:8000                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │            FastAPI Application (api.py)                 │  │
│  ├──────────────────────────────────────────────────────────┤  │
│  │                                                          │  │
│  │  ✓ POST /api/v1/simulate                               │  │
│  │    - Accepts SimulationRequest                         │  │
│  │    - Returns simulation results                        │  │
│  │                                                          │  │
│  │  ✓ WS /ws/simulate                                      │  │
│  │    - Real-time streaming                              │  │
│  │    - Same model with random distribution              │  │
│  │                                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         ▲                           ▲                  ▲
         │                           │                  │
    ┌────┴────────┐          ┌──────┴────────┐  ┌─────┴──────┐
    │              │          │               │  │            │
    ▼              ▼          ▼               ▼  ▼            ▼
  /docs        /redoc    /openapi.json    Python   cURL    Postman
(Swagger UI) (ReDoc)   (Schema JSON)     Client   Client   Client
```

## Data Model Structure

```
SimulationRequest
├─ NetworkConfig
│  ├─ num_nodes: int
│  ├─ network_type: str (scale_free|small_world|random|complete)
│  ├─ device_attributes: Dict[str, Any] (optional)
│  ├─ node_definitions: List[NodeDefinition] (optional)
│  │  └─ NodeDefinition
│  │     ├─ count: int
│  │     └─ attributes: Dict[str, Any]
│  └─ node_distribution: str (sequential|random) ← NEW
│
├─ MalwareConfig
│  ├─ malware_type: str (worm|virus|ransomware)
│  ├─ infection_rate: float (0.0-1.0)
│  └─ latency: int (0+)
│
├─ initial_infected: List[str]
│
└─ max_steps: int (1+)
```

## Feature Implementation

```
┌────────────────────────────────────────────────────────────────┐
│                   Random Distribution Feature                 │
├────────────────────────────────────────────────────────────────┤
│                                                                │
│  NetworkConfig.node_distribution: str                         │
│      │                                                         │
│      ├─ "sequential" (default)                                │
│      │   └─ Devices assigned in order                         │
│      │      └─ device_0-69 [admin], device_70-99 [non-admin] │
│      │         └─ Creates clustering                          │
│      │                                                         │
│      └─ "random" (NEW) ← Solves clustering problem           │
│          └─ Devices randomly shuffled                         │
│             └─ device_5 [admin], device_13 [non-admin], ...  │
│                └─ Realistic network mixing                    │
│                                                                │
│  _apply_node_definitions(network, definitions, distribution) │
│      ├─ Builds list of (device_id, attributes) pairs         │
│      ├─ if distribution == "random": shuffle pairs            │
│      └─ Apply attributes to devices                           │
│                                                                │
└────────────────────────────────────────────────────────────────┘
```

## Swagger Documentation Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Swagger/OpenAPI Schema                     │
│                    (auto-generated from models)                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  Field Descriptions Layer                                      │
│  ├─ num_nodes: "Number of devices in the network"            │
│  ├─ network_type: "Type of network topology: ..."            │
│  ├─ node_distribution: "sequential or random mixing"          │
│  ├─ infection_rate: "Probability 0.0-1.0"                    │
│  └─ ... (all fields documented)                              │
│                                                                 │
│  Example Payloads Layer                                        │
│  ├─ Example 1: Simple 70/30 Split                            │
│  ├─ Example 2: Enterprise Three-Tier                         │
│  ├─ Example 3: Mixed Operating Systems                       │
│  ├─ Example 4: Progressive Security Hardening               │
│  ├─ Example 5: Sequential Distribution (Clustered)          │
│  ├─ Example 6: Simple Homogeneous Network                   │
│  └─ Example 7: Multiple Initial Infections                  │
│                                                                 │
│  Constraint Validation Layer                                   │
│  ├─ infection_rate: ge=0.0, le=1.0                           │
│  ├─ max_steps: ge=1                                           │
│  ├─ latency: ge=0                                             │
│  └─ ... (field-level constraints)                            │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
         │
    ┌────┴───────────────────────────────────────┐
    │                                            │
    ▼                    ▼                        ▼
  Swagger UI          ReDoc                  JSON Schema
  (Interactive)    (Documentation)          (Machine-readable)
```

## The 7 Examples Landscape

```
                    Complexity Axis →
    
    │ Security    │  Example 4: Progressive      Example 2: Enterprise
    │ Complexity  │  Hardening (120 devices)     3-Tier (500 devices)
    │ (defenses)  │       ↑                              ↑
    │             │       │                              │
    │             │    Example 3: Mixed OS          Example 1: 70/30
    │             │    (150 devices)                (100 devices)
    │             │       │                         Random ↑
    │             │       │                              ↗
    │             │       │                             ╱
    │             │       │     Example 7: Multi-source
    │             │       │     (200 devices, small-world)
    │             │       │         │
    │             ▼       │         │
    │         Example 6:  │         │
    │         Homogeneous │         │
    │         (50 devices)│    Example 5: Sequential
    │              │      │    (same as Example 1,
    │              │      │     but CLUSTERED)
    │              │      │         │
    └──────────────┴──────┴─────────┴──────────────────→
                             Device Count
```

## Attribute Hierarchy

```
Default Attributes (ALWAYS APPLIED)
    ↓ Merged with
Device Attributes (APPLIED TO ALL NODES)
    ↓ Overridden by
Node Definitions Per-Batch (BATCH-SPECIFIC)

┌─────────────────────────────────────────────┐
│ Example 2: Enterprise Three-Tier Network   │
├─────────────────────────────────────────────┤
│                                             │
│ Step 1: Defaults                           │
│ {os: None, firewall_enabled: None, ...}    │
│                                             │
│ Step 2: Network-wide attributes            │
│ {os: "Windows", firewall_enabled: True}    │
│                                             │
│ Step 3: Batch 1 (50 servers)               │
│ {firewall_enabled: True}  ← OVERRIDE       │
│ Result: {os: "Windows", firewall: True}    │
│                                             │
│ Step 4: Batch 3 (250 guests)               │
│ {firewall_enabled: False}  ← OVERRIDE      │
│ Result: {os: "Windows", firewall: False}   │
│                                             │
└─────────────────────────────────────────────┘
```

## Documentation Structure

```
Documentation Files (5 files)
│
├─ SWAGGER_DOCUMENTATION.md
│  └─ Overview of Swagger enhancements
│
├─ SWAGGER_UI_GUIDE.md
│  └─ How-to guide for using Swagger UI
│
├─ SWAGGER_ENHANCEMENT_SUMMARY.md
│  └─ Technical implementation details
│
├─ SWAGGER_QUICK_REFERENCE.md
│  └─ Quick lookup and pro tips
│
└─ PROJECT_COMPLETION_SUMMARY.md
   └─ Overall completion report
```

## Request Processing Flow

```
User Opens /docs
    ↓
Swagger UI Loads
    ↓
Displays POST /api/v1/simulate
    ├─ Field Descriptions visible
    ├─ Example Dropdown available
    ├─ 7 Examples ready to select
    └─ Request body schema shown
         ↓
    Select Example
         ↓
    JSON Auto-populates
         ↓
    Click "Try it out"
         ↓
    Edit values (optional)
         ↓
    Click "Execute"
         ↓
    API Request sent
         ↓
    Response received
         ↓
    Results displayed
```

## Response Flow (Simulation Execution)

```
API Receives SimulationRequest
    ├─ Parse network_config
    ├─ Parse malware_config
    └─ Parse node_distribution ← NEW
        ↓
    Create Network
        ├─ Generate topology
        ├─ Apply device_attributes
        └─ Apply node_definitions
             ├─ Build (device_id, attrs) pairs
             ├─ if distribution=="random": shuffle
             └─ Apply to devices
        ↓
    Create Malware
        └─ Worm | Virus | Ransomware
        ↓
    Run Simulation
        ├─ Initialize with initial_infected
        ├─ Run for max_steps
        └─ Track spread
        ↓
    Return Results
        ├─ total_devices
        ├─ total_infected
        ├─ infection_percentage
        ├─ total_steps
        └─ history (step-by-step)
```

## Feature Matrix: Examples vs Features

```
                        Node Defs  Device Attrs  Random Dist  Multi-Initial
Example 1 (70/30)         ✓           -             ✓            -
Example 2 (Enterprise)    ✓           ✓             ✓            -
Example 3 (Mixed OS)      ✓           -             ✓            -
Example 4 (Hardening)     ✓           -             ✓            -
Example 5 (Sequential)    ✓           -             ✗ (seq)      -
Example 6 (Homogeneous)   ✗           ✓             -            -
Example 7 (Multi-src)     -           -             ✓            ✓

Legend:
✓ = Feature demonstrated
✗ = Feature explicitly NOT used (for comparison)
- = Feature not relevant
```

## Validation Pipeline

```
Pydantic Model Validation
│
├─ Type Checking
│  ├─ num_nodes: must be int
│  ├─ infection_rate: must be float
│  └─ node_definitions: must be List[NodeDefinition]
│
├─ Constraint Validation
│  ├─ infection_rate: 0.0 ≤ value ≤ 1.0
│  ├─ max_steps: value ≥ 1
│  ├─ latency: value ≥ 0
│  └─ num_nodes: value ≥ 1
│
├─ Required Field Validation
│  ├─ network_config: required
│  ├─ malware_config: required
│  └─ initial_infected: required
│
└─ Optional Field Handling
   ├─ device_attributes: optional
   ├─ node_definitions: optional
   └─ node_distribution: optional (default="sequential")
```

## Complete Feature Set

```
┌──────────────────────────────────────────────────────┐
│              MSpreadEngine v1.0 Features            │
├──────────────────────────────────────────────────────┤
│                                                      │
│ Network Features                                   │
│ ✓ Multiple topologies (scale-free, small-world)   │
│ ✓ Device attributes (admin_user, os, firewall...)  │
│ ✓ Node definitions (batching, segmentation)        │
│ ✓ Random distribution (realistic mixing) ← NEW    │
│                                                     │
│ Malware Features                                  │
│ ✓ Multiple types (worm, virus, ransomware)        │
│ ✓ Configurable infection_rate                     │
│ ✓ Configurable latency                            │
│ ✓ Privilege-based spread restrictions             │
│                                                     │
│ Simulation Features                               │
│ ✓ HTTP REST API                                   │
│ ✓ WebSocket streaming                             │
│ ✓ Step-by-step tracking                           │
│ ✓ Multi-source infections                         │
│                                                     │
│ Documentation Features                            │
│ ✓ Swagger/OpenAPI UI                             │
│ ✓ 7 comprehensive examples ← NEW                 │
│ ✓ Field descriptions ← NEW                        │
│ ✓ 5 documentation files ← NEW                     │
│                                                     │
└──────────────────────────────────────────────────────┘
```

---

**Architecture Summary**: Comprehensive API with interactive Swagger documentation, real-world examples, and flexible network segmentation through random distribution of device types.
