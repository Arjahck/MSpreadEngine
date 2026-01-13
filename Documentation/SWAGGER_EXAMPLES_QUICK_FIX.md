# Accessing Swagger Examples - Quick Guide

## 🔴 Issue: Examples Not Showing?

If you're not seeing the 7 examples in Swagger UI, here's how to fix it:

## ✅ Solution Steps

### 1. Access Swagger UI
Open your browser and go to:
```
http://localhost:8000/docs
```

### 2. Find the POST /api/v1/simulate Endpoint
Scroll down and click on the **blue** `POST /api/v1/simulate` section to expand it.

### 3. Look for "Examples" Dropdown
Inside the request body section, you should see:

```
Request body
├─ Required ✓
├─ application/json
└─ Examples (▼ dropdown)
    ├─ Simple 70/30 Admin/Non-Admin Split
    ├─ Enterprise Three-Tier Network
    ├─ Mixed Operating Systems
    ├─ Progressive Security Hardening
    ├─ Sequential Distribution (Clustered)
    ├─ Simple Homogeneous Network
    └─ Multiple Initial Infections
```

### 4. Select an Example
Click on the example name (e.g., "Enterprise Three-Tier Network") to load it.

The JSON request body will auto-populate with that example's data.

### 5. Execute the Request
- Click **"Try it out"** button
- (Optional) Edit any values
- Click **"Execute"** button
- View the response below

## 📋 The 7 Examples

| # | Name | Size | Focus |
|---|------|------|-------|
| 1 | **Simple 70/30 Split** | 100 nodes | Basic admin/non-admin ratio |
| 2 | **Enterprise Three-Tier** | 500 nodes | Realistic layered network |
| 3 | **Mixed Operating Systems** | 150 nodes | Windows/Linux heterogeneity |
| 4 | **Progressive Hardening** | 120 nodes | Security layer comparison |
| 5 | **Sequential (Clustered)** | 100 nodes | Shows clustering problem (for comparison) |
| 6 | **Homogeneous Network** | 50 nodes | All identical devices (baseline) |
| 7 | **Multi-Source Infections** | 200 nodes | Multiple initial infected devices |

## 🔗 Other Documentation URLs

| URL | Purpose |
|-----|---------|
| `/docs` | **Swagger UI** (interactive, examples, try-it-out) |
| `/redoc` | **ReDoc** (API reference, comprehensive schema) |
| `/openapi.json` | **OpenAPI Schema** (machine-readable specification) |

## 🎯 Use Cases

### Want to understand the API?
→ Start with `/docs` (Swagger UI)

### Need complete API reference?
→ Check `/redoc` (ReDoc)

### Building a client library?
→ Use `/openapi.json` (OpenAPI schema)

### Running WebSocket simulations?
→ See `WEBSOCKET_DOCUMENTATION.md`

## 💡 Pro Tips

### Tip 1: Copy JSON for Scripts
```javascript
// From Swagger UI, copy the selected example and paste into script
fetch('http://localhost:8000/api/v1/simulate', {
  method: 'POST',
  headers: {'Content-Type': 'application/json'},
  body: JSON.stringify({
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
  })
})
```

### Tip 2: Modify Examples
Load an example and change values to test different scenarios:
- Increase `num_nodes` for larger networks
- Change `network_type` to test different topologies
- Adjust `infection_rate` to test spread intensity
- Toggle `node_distribution` between "sequential" and "random"

### Tip 3: Test Different Malware Types
Use examples as templates but change:
```json
"malware_config": {
  "malware_type": "virus",        // or "ransomware"
  "infection_rate": 0.25,          // Lower spread = harder to detect
  "latency": 2                      // Delayed infection spread
}
```

## ❓ Troubleshooting

### Problem: Examples still not showing?

**Solution 1:** Clear browser cache
- Press Ctrl+Shift+Delete
- Clear all cache
- Reload http://localhost:8000/docs

**Solution 2:** Try a different browser
- Chrome: Better Swagger UI support
- Firefox: Good ReDoc support
- Edge: Works well

**Solution 3:** Check API is running
```bash
curl http://localhost:8000/health
# Should return: {"status":"healthy"}
```

**Solution 4:** Verify OpenAPI schema loads
```bash
curl http://localhost:8000/openapi.json | jq '.paths."/api/v1/simulate"'
# Should show POST endpoint with examples
```

### Problem: Swagger UI loads but examples dropdown missing?

This happens with older FastAPI versions. The API has been updated to explicitly enable docs:

```python
app = FastAPI(
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc",    # ReDoc
    openapi_url="/openapi.json"  # Schema
)
```

If still not working:
1. Check Python/FastAPI version: `pip list | grep fastapi`
2. Ensure Pydantic is v1 (v2 has different example handling)
3. Verify api/api.py line ~373 has `docs_url="/docs"`

## 🚀 Quick Start: First Simulation

1. **Open Swagger UI:**
   ```
   http://localhost:8000/docs
   ```

2. **Expand POST /api/v1/simulate**

3. **Select "Simple 70/30 Admin/Non-Admin Split" from Examples dropdown**

4. **Click "Try it out"**

5. **Click "Execute"**

6. **View results:**
   ```json
   {
     "total_devices": 100,
     "total_infected": 87,
     "infection_percentage": 87.0,
     "total_steps": 6,
     "initial_infected": ["device_0"]
   }
   ```

## 📚 Related Documentation

- **SWAGGER_DOCUMENTATION.md** - Detailed explanation of all 7 examples
- **SWAGGER_UI_GUIDE.md** - Visual guide to Swagger UI features
- **WEBSOCKET_DOCUMENTATION.md** - Real-time streaming simulations
- **SWAGGER_QUICK_REFERENCE.md** - Parameter reference and tips

---

**Questions?** Check the documentation files or review the example JSON in Swagger UI.
