# Swagger/OpenAPI Documentation Updates

## What's New in `/docs`

The FastAPI Swagger UI documentation at `http://localhost:8000/docs` has been enhanced with comprehensive examples for all features.

## Available Examples in the Swagger UI

When you visit `http://localhost:8000/docs`, you'll see the **POST /api/v1/simulate** endpoint with **7 detailed examples**:

### 1. **Simple 70/30 Admin/Non-Admin Split**
- 100 devices split randomly
- 70 admin servers, 30 non-admin workstations
- Demonstrates basic network segmentation with random distribution

### 2. **Enterprise Three-Tier Network**
- 500 devices with realistic enterprise structure
- Tier 1: 50 critical servers (highly protected)
- Tier 2: 200 admin workstations (protected)
- Tier 3: 250 guest workstations (minimal security)
- Shows privilege boundary effects

### 3. **Mixed Operating Systems**
- 150 devices across three OS types
- Windows servers, Linux workstations, Windows guest devices
- Demonstrates heterogeneous network modeling
- Uses virus with higher latency

### 4. **Progressive Security Hardening**
- 120 devices showing security layers
- Layer 1: 40 unprotected devices (no firewall, antivirus, or patches)
- Layer 2: 40 basic protection (antivirus only)
- Layer 3: 40 full protection (firewall + antivirus + admin + patched)
- Uses ransomware with latency=3

### 5. **Sequential Distribution (Clustered)**
- Shows impact of sequential vs random distribution
- Devices grouped by type (not mixed)
- Useful for comparison studies
- Same 70/30 split as Example 1, but sequential instead of random

### 6. **Simple Homogeneous Network**
- 50 identical devices (all admin)
- All Windows 11 workstations
- Baseline for comparing with segmented networks
- Fastest spread scenario

### 7. **Multiple Initial Infections**
- 200 devices on small-world topology
- Starts with 4 infected devices (device_0, 50, 100, 150)
- Demonstrates epidemic spread from multiple sources
- 75 simulation steps

## Model Documentation

Each model now has detailed field descriptions:

### NetworkConfig
- `num_nodes`: Number of devices (example: 100)
- `network_type`: Topology type (scale_free, small_world, random, complete)
- `device_attributes`: Uniform attributes for all devices
- `node_definitions`: Batch definitions for device segmentation
- `node_distribution`: "sequential" (default) or "random" for mixing

### MalwareConfig
- `malware_type`: worm, virus, or ransomware
- `infection_rate`: 0.0 to 1.0 (probability per neighbor)
- `latency`: Steps before infection spreads (0+)

### SimulationRequest
- Full request schema with all 7 examples
- Each example has summary, description, and complete JSON

## How to Use the Examples

1. **Start the API Server**:
   ```bash
   python main.py run
   ```

2. **Open Swagger UI**:
   ```
   http://localhost:8000/docs
   ```

3. **Find POST /api/v1/simulate**:
   - Click the endpoint to expand
   - Scroll to "Request body"
   - Click "Examples" dropdown
   - Select any example

4. **Test an Example**:
   - Select an example from the dropdown
   - The JSON automatically populates
   - Click "Try it out"
   - Click "Execute"

## Key Feature Highlights in Examples

### Node Definitions
All examples with `node_definitions` show:
- How to create device batches
- Different attribute combinations per batch
- Realistic network segmentation

### Random Distribution
Examples 1, 2, 3, 4 use `"node_distribution": "random"` to:
- Mix different device types throughout the network
- Create realistic topology (not artificially clustered)
- Test privilege boundaries more accurately

### Sequential Distribution
Example 5 uses `"node_distribution": "sequential"` to:
- Show clustered vs mixed comparison
- Demonstrate impact on spread patterns
- Useful for research and benchmarking

### Device Attributes
Examples show various attribute combinations:
- `admin_user`: Privilege level (affects spread)
- `device_type`: server, workstation, iot_device, etc.
- `os`: Windows Server, Linux, Windows, etc.
- `firewall_enabled`: Boolean security feature
- `antivirus`: Boolean security feature
- `patch_status`: unpatched, patched, fully_patched

### Network Topologies
Examples use different topology types:
- `scale_free`: Realistic real-world networks (power-law distribution)
- `small_world`: Networks with clustering (Examples 7)
- Others available: `random`, `complete`

### Malware Types
Examples demonstrate:
- **Worm** (latency=1): Fast spreading, agile
- **Virus** (latency=2): Medium speed, requires interaction
- **Ransomware** (latency=3): Slow, deliberate spread

## Field Validation

All examples respect field constraints:
- `num_nodes`: Positive integer
- `infection_rate`: 0.0 to 1.0
- `latency`: 0 or positive integer
- `max_steps`: 1 or higher
- Device IDs: Format "device_N"

## Accessing Schema Details

In the Swagger UI, you can:
1. Click on any model name to expand its schema
2. See field descriptions, types, and validation rules
3. View example values for each field
4. Understand required vs optional fields

## Integration with Frontend

The Swagger documentation can be used to:
1. **Understand API contracts** - See exact request/response formats
2. **Test endpoints interactively** - No need for curl/postman
3. **Reference examples** - Copy JSON for actual implementations
4. **Validate payloads** - Check field requirements before sending

## Quick Copy-Paste

To use an example:
1. Open Swagger UI
2. Select an example
3. Modify as needed
4. Copy the JSON
5. Use with Python `requests`, curl, or fetch API

## Additional Resources

- **Full documentation**: See NODE_DEFINITIONS.md
- **Technical details**: See BATCH_LOGIC_IMPLEMENTATION.md
- **Usage examples**: Run example_node_definitions.py
- **Test suite**: python test_api_demo.py -t 11

## Schema Location

The OpenAPI/Swagger schema is automatically generated by FastAPI at:
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

All examples are embedded in the schema and displayed in the UI automatically.
