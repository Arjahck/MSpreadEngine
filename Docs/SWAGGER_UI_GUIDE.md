# Swagger Documentation: What You'll See

## Visual Overview

When you open `http://localhost:8000/docs`, the POST `/api/v1/simulate` endpoint now shows:

```
POST /api/v1/simulate
  └─ Simulate Malware Spreading
     
     Request Body:
     ├─ NetworkConfig
     │  ├─ num_nodes (integer, required)
     │  ├─ network_type (string, default="scale_free")
     │  ├─ device_attributes (object, optional)
     │  ├─ node_definitions (array of NodeDefinition, optional)
     │  └─ node_distribution (string, default="sequential")
     │
     ├─ MalwareConfig
     │  ├─ malware_type (string, required)
     │  ├─ infection_rate (number, 0.0-1.0)
     │  └─ latency (integer, >=0)
     │
     ├─ initial_infected (array of strings, required)
     └─ max_steps (integer, default=100)
     
     Examples:
     ├─ Simple 70/30 Admin/Non-Admin Split
     ├─ Enterprise Three-Tier Network
     ├─ Mixed Operating Systems
     ├─ Progressive Security Hardening
     ├─ Sequential Distribution (Clustered)
     ├─ Simple Homogeneous Network
     └─ Multiple Initial Infections
```

## Field Descriptions in Swagger

### NetworkConfig Fields

**num_nodes** (integer, required)
- Description: "Number of devices in the network"
- Example: 100
- Minimum: 1
- Used in: All examples

**network_type** (string, default="scale_free")
- Description: "Type of network topology: scale_free, small_world, random, complete"
- Example: "scale_free"
- Options: scale_free, small_world, random, complete

**device_attributes** (object, optional)
- Description: "Attributes to apply to ALL nodes uniformly"
- Example: `{"os": "Windows Server 2019", "firewall_enabled": true}`
- Note: Can be overridden by node_definitions

**node_definitions** (array of NodeDefinition, optional)
- Description: "Batch definitions for per-group device attributes (creates network segmentation)"
- Used for: Creating device groups with different attributes
- Example format:
  ```json
  [
    {"count": 70, "attributes": {"admin_user": true}},
    {"count": 30, "attributes": {"admin_user": false}}
  ]
  ```

**node_distribution** (string, default="sequential")
- Description: "Distribution mode: 'sequential' (clusters devices by type) or 'random' (mixes device types throughout network)"
- Options: sequential, random
- Example: "random"

### MalwareConfig Fields

**malware_type** (string, required)
- Description: "Type of malware: worm, virus, ransomware"
- Example: "worm"
- Options: worm, virus, ransomware

**infection_rate** (number, required, 0.0-1.0)
- Description: "Probability of infection spreading to each neighbor (0.0-1.0)"
- Example: 0.35
- Range: 0.0 to 1.0
- Typical: 0.25-0.40

**latency** (integer, required, >=0)
- Description: "Number of steps before infection can spread"
- Example: 1
- Typical: worm=1, virus=2, ransomware=3

### SimulationRequest Fields

**network_config** (NetworkConfig, required)
- The network topology configuration

**malware_config** (MalwareConfig, required)
- The malware behavior configuration

**initial_infected** (array of strings, required)
- Description: "List of initially infected device IDs"
- Example: ["device_0", "device_5"]
- Format: "device_N" where N is an integer

**max_steps** (integer, default=100)
- Description: "Maximum simulation steps to run"
- Example: 50
- Minimum: 1

## Example Selection UI

In Swagger, under "Request body", you'll see:

```
Request body:
  
  [Select Example] ▼

  Example Options:
  ✓ Simple 70/30 Admin/Non-Admin Split
    Enterprise Three-Tier Network
    Mixed Operating Systems
    Progressive Security Hardening
    Sequential Distribution (Clustered)
    Simple Homogeneous Network
    Multiple Initial Infections
```

Click the dropdown to switch between examples. The JSON body updates automatically.

## Each Example Shows

### Summary (one-liner)
"Simple 70/30 Admin/Non-Admin Split"

### Description (detailed)
"Basic simulation with devices split into admin and non-admin groups"

### Complete JSON Payload
Full, ready-to-execute request body

## Response Schema

The endpoint returns:
```json
{
  "total_devices": 100,
  "total_infected": 85,
  "infection_percentage": 85.0,
  "total_steps": 12,
  "malware_type": "worm",
  "history": [
    {
      "step": 1,
      "newly_infected": 3,
      "total_infected": 4,
      "devices_infected": ["device_0", "device_5", "device_12", "device_18"]
    }
  ]
}
```

## How to Use

### Method 1: Interactive Testing (Recommended)

1. Start API: `python main.py run`
2. Open: `http://localhost:8000/docs`
3. Find: POST /api/v1/simulate
4. Click: "Try it out"
5. Select: Example from dropdown
6. Click: "Execute"
7. View: Response and timing

### Method 2: Copy and Modify

1. Open: `http://localhost:8000/docs`
2. Select: Example you like
3. Copy: JSON payload
4. Modify: As needed
5. Use: In your application

### Method 3: Use Generated OpenAPI Schema

The schema is available at:
- JSON: `http://localhost:8000/openapi.json`
- Can be imported into Postman, Insomnia, etc.

## Keyboard Shortcuts in Swagger

- **Ctrl+A / Cmd+A**: Select all in text area
- **Ctrl+C / Cmd+C**: Copy selected text
- **Tab**: Auto-complete suggestions

## Tips

1. **Start Simple**: Use "Simple Homogeneous Network" first
2. **Understand Basics**: Try the 70/30 split example
3. **Compare**: Use sequential vs random for comparison
4. **Enterprise**: Try three-tier network for complexity
5. **Validate**: Check field descriptions before modifying

## Sharing Examples

The examples are:
- ✅ Self-contained and runnable
- ✅ Representative of real scenarios
- ✅ Include explanations and summaries
- ✅ Progressive in complexity
- ✅ Easy to modify and extend

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Examples not showing | Try refreshing the page |
| Dropdown empty | Check browser console for errors |
| JSON invalid | Click "Try it out" first |
| Response error | Check field types match schema |

## Additional Documentation

For more details, see:
- **NODE_DEFINITIONS.md** - Feature overview
- **SWAGGER_DOCUMENTATION.md** - This file
- **BATCH_LOGIC_IMPLEMENTATION.md** - Technical details
- **example_node_definitions.py** - Programmatic examples

## Schema Validation

All examples are validated against the Pydantic models:
- ✅ Field types correct
- ✅ Required fields present
- ✅ Value ranges valid
- ✅ Array formats correct
- ✅ Nested objects valid

Every example is a working, tested request payload.
