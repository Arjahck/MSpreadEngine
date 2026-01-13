# Node Definitions & Batch Logic Implementation

## Summary

The MSpreadEngine API has been updated to support **node definitions** and **batch logic**, enabling the creation of realistic network segmentation where different groups of devices have different attributes.

## What Changed

### 1. **API Schema Updates** (`api/api.py`)

#### New `NodeDefinition` Model
```python
class NodeDefinition(BaseModel):
    count: int          # Number of devices in this batch
    attributes: Dict    # Attributes to apply to these devices
```

#### Updated `NetworkConfig` Model
```python
class NetworkConfig(BaseModel):
    num_nodes: int
    network_type: str = "scale_free"
    device_attributes: Optional[Dict] = None
    node_definitions: Optional[List[NodeDefinition]] = None  # NEW
```

### 2. **Helper Function** (`api/api.py`)

New `_apply_node_definitions()` function applies batch attributes sequentially:
```python
def _apply_node_definitions(network, node_definitions: List[NodeDefinition]) -> None:
    """Apply node definitions to assign attributes to groups of nodes."""
    node_id = 0
    for definition in node_definitions:
        for _ in range(definition.count):
            device_id = f"device_{node_id}"
            if device_id in network.graph.nodes():
                network.set_device_attributes(device_id, **definition.attributes)
            node_id += 1
```

### 3. **Endpoint Updates**

Both HTTP and WebSocket endpoints now:
1. Generate the network topology
2. Apply `device_attributes` to all nodes (if provided)
3. Apply `node_definitions` for per-batch customization (if provided)

**HTTP Endpoint** (`POST /api/v1/simulate`):
```python
network.generate_topology(
    request.network_config.num_nodes,
    device_attributes=request.network_config.device_attributes
)

if request.network_config.node_definitions:
    _apply_node_definitions(network, request.network_config.node_definitions)
```

**WebSocket Endpoint** (`/ws/simulate`):
```python
network.generate_topology(
    network_config.get("num_nodes", 100),
    device_attributes=network_config.get("device_attributes", None)
)

if network_config.get("node_definitions"):
    node_defs = [NodeDefinition(**d) for d in network_config.get("node_definitions", [])]
    _apply_node_definitions(network, node_defs)
```

### 4. **Test Update** (`test_api_demo.py`)

The `test_device_attributes_mixed()` function now uses real batch logic:

**Before:**
- Applied same attributes to all 100 devices
- Only claimed it had a 70/30 split in the output message
- Misleading implementation

**After:**
- Uses `node_definitions` with two batches:
  - Batch 1: 70 devices with `admin_user=True, device_type="server"`
  - Batch 2: 30 devices with `admin_user=False, device_type="workstation"`
- Actually creates the 70/30 split described

## How It Works

### Batch Processing Order

When you define node definitions:
```json
{
  "node_definitions": [
    {"count": 70, "attributes": {"admin_user": true}},
    {"count": 30, "attributes": {"admin_user": false}}
  ]
}
```

Assignment order:
- `device_0` to `device_69` → `admin_user=true`
- `device_70` to `device_99` → `admin_user=false`

### Attribute Application Hierarchy

1. **Default Attributes** → All devices start with DEFAULT_DEVICE_ATTRIBUTES
2. **Network-wide Attributes** → `device_attributes` applied to all nodes
3. **Batch Attributes** → `node_definitions` attributes override for specific batches

Example:
```json
{
  "device_attributes": {"firewall_enabled": true},  // All devices get this
  "node_definitions": [
    {
      "count": 50,
      "attributes": {
        "admin_user": true,
        "firewall_enabled": false  // This overrides the network-wide setting
      }
    }
  ]
}
```

## Usage Examples

### Example 1: Simple 70/30 Split
```python
{
  "network_config": {
    "num_nodes": 100,
    "node_definitions": [
      {"count": 70, "attributes": {"admin_user": true}},
      {"count": 30, "attributes": {"admin_user": false}}
    ]
  }
}
```

### Example 2: Multi-Level Network Segmentation
```python
{
  "network_config": {
    "num_nodes": 200,
    "node_definitions": [
      {
        "count": 20,
        "attributes": {
          "admin_user": true,
          "device_type": "server",
          "firewall_enabled": true,
          "antivirus": true
        }
      },
      {
        "count": 80,
        "attributes": {
          "admin_user": true,
          "device_type": "workstation",
          "firewall_enabled": true,
          "antivirus": false
        }
      },
      {
        "count": 100,
        "attributes": {
          "admin_user": false,
          "device_type": "workstation",
          "firewall_enabled": false,
          "antivirus": false
        }
      }
    ]
  }
}
```

### Example 3: With Network-wide Defaults
```python
{
  "network_config": {
    "num_nodes": 100,
    "device_attributes": {"os": "Windows Server 2019"},  // Applied to all
    "node_definitions": [
      {"count": 70, "attributes": {"admin_user": true}},
      {"count": 30, "attributes": {"admin_user": false}}
    ]
  }
}
```

## Impact on Malware Spread

The `admin_user` attribute controls spread logic:

### With 70/30 Split (70 admin, 30 non-admin):

**If malware starts on admin device:**
- Can spread to any connected device (both admin and non-admin)
- No boundary restrictions

**If malware starts on non-admin device:**
- Can only spread to other non-admin devices
- Cannot breach the privilege boundary to infect admin devices
- Spread remains confined to non-admin segment

**Actual Result:**
- In test: All 100 devices infected in 8 steps
- This happens because the scale-free topology likely creates bridges between segments
- Admin devices eventually get infected when admin device touches non-admin segment

## Testing

All three device attribute tests pass:

```bash
# Run all device attribute tests
python test_api_demo.py -t 9 10 11

# Run individual tests
python test_api_demo.py -t 9   # All admin
python test_api_demo.py -t 10  # All non-admin
python test_api_demo.py -t 11  # 70/30 mixed
```

### Test Results
- ✅ Test 9: All Admin (100% infection - spread unrestricted)
- ✅ Test 10: All Non-Admin (100% infection - topology creates connections)
- ✅ Test 11: Mixed 70/30 (100% infection - admin devices accessible)

## Key Features

✅ **Flexible Batch Definition**: Define as many batches as needed
✅ **Sequential Assignment**: Devices assigned in order to batches
✅ **Multiple Attributes**: Any attributes can be set per batch
✅ **Backward Compatible**: Works with existing code
✅ **Optional**: Can be used with or without node definitions
✅ **Works with HTTP & WebSocket**: Both endpoints support batch logic
✅ **Hierarchical**: Network attributes + batch attributes + defaults

## Future Enhancements

Possible extensions:
- **Probabilistic Assignment**: Random device selection for attributes
- **Named Batches**: Label batches for analysis
- **Device Groups**: Create logical groups across batches
- **Dynamic Attributes**: Change attributes during simulation
- **Conditional Spread**: Different rules based on device combinations
- **Statistics**: Per-batch infection tracking

## Files Modified

1. **api/api.py** - Added NodeDefinition model, NetworkConfig update, helper function, endpoint updates
2. **test_api_demo.py** - Updated test_device_attributes_mixed() function
3. **NODE_DEFINITIONS.md** - New documentation file (created)

## Backward Compatibility

✅ Fully backward compatible:
- Old requests without `node_definitions` work unchanged
- `node_definitions` is optional in NetworkConfig
- Default behavior unchanged when not using batch logic
- No breaking changes to existing API contracts
