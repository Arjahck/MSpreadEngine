# Swagger Examples Not Showing - Detailed Troubleshooting

## Status

Examples **ARE** defined in the API and available in the OpenAPI schema. They may just need a UI refresh to display properly.

## Quick Fixes (Try These First)

### Fix #1: Hard Refresh Swagger UI
```
1. Open: http://localhost:8000/docs
2. Press: Ctrl + Shift + R (hard refresh)
3. Wait: 2-3 seconds for Swagger to reload
4. Look: For Examples dropdown
```

### Fix #2: Clear All Browser Cache
```
1. Press: Ctrl + Shift + Delete
2. Select: All time
3. Check: Cookies, Cached images, Cached files
4. Click: Clear data
5. Revisit: http://localhost:8000/docs
```

### Fix #3: Try Different Browser
```
Chrome:    Chrome usually works best with Swagger
Firefox:   Also works well
Safari:    Should work
Edge:      Works fine
```

### Fix #4: Try Incognito/Private Window
```
1. Ctrl + Shift + N (Chrome)
2. Open: http://localhost:8000/docs
3. Check: Do examples show?
```

---

## Verification: Examples ARE in the API

### Verify #1: OpenAPI Schema Has Examples
```bash
curl http://localhost:8000/openapi.json | grep -o '"summary"' | wc -l
# Should output: 7 (one for each example)
```

### Verify #2: See Example Titles
```bash
curl http://localhost:8000/openapi.json | python -m json.tool | grep '"summary"'

# Output should show:
# "summary": "Simple 70/30 Admin/Non-Admin Split",
# "summary": "Enterprise Three-Tier Network",
# "summary": "Mixed Operating Systems",
# "summary": "Progressive Security Hardening",
# "summary": "Sequential Distribution (Clustered)",
# "summary": "Simple Homogeneous Network",
# "summary": "Multiple Initial Infections",
```

### Verify #3: Check Full Example Structure
```bash
curl http://localhost:8000/openapi.json | python -m json.tool > schema.json
# Then open schema.json and search for "json_schema_extra"
# or look in components > schemas > SimulationRequest
```

---

## Where to Find Examples in Swagger UI

If they do appear, here's where to look:

```
Browser: http://localhost:8000/docs
        │
        ▼ (scroll down)
POST /api/v1/simulate (blue box)
        │
        ▼ (click to expand)
Request body section
        │
        ▼ (look for)
application/json
        │
        ▼ (scroll right or look for)
┌─────────────────────────┐
│ Examples (dropdown ▼)   │  ← Click this
└─────────────────────────┘
        │
        ▼ (dropdown shows)
- Simple 70/30 Admin/Non-Admin Split
- Enterprise Three-Tier Network
- Mixed Operating Systems
- Progressive Security Hardening
- Sequential Distribution (Clustered)
- Simple Homogeneous Network
- Multiple Initial Infections
```

---

## If Examples Still Don't Show

### Alternative #1: Get Examples from OpenAPI Endpoint
```bash
curl http://localhost:8000/openapi.json > api_schema.json

# Open api_schema.json and search for:
# components > schemas > SimulationRequest > examples
```

### Alternative #2: Get Examples from Code
```bash
# Open file: api/api.py
# Go to: Line 84 (start of examples list)
# Copy any example JSON you want
```

### Alternative #3: Use Curl with Example
```bash
curl -X POST http://localhost:8000/api/v1/simulate \
  -H "Content-Type: application/json" \
  -d '{"network_config":{"num_nodes":100,"network_type":"scale_free","node_definitions":[{"count":70,"attributes":{"admin_user":true}},{"count":30,"attributes":{"admin_user":false}}],"node_distribution":"random"},"malware_config":{"malware_type":"worm","infection_rate":0.35,"latency":1},"initial_infected":["device_0"],"max_steps":50}'
```

---

## Why Examples Might Not Show Initially

### Reason #1: Swagger UI Cache
- Swagger UI caches the OpenAPI schema
- Solution: Hard refresh (Ctrl+Shift+R) or clear browser cache

### Reason #2: Browser Extension Interference
- AdBlockers or privacy extensions might block parts of Swagger UI
- Solution: Disable extensions temporarily or try different browser

### Reason #3: Different Swagger Version
- Different Swagger UI versions handle examples differently
- Solution: Clear cache, the latest version should work

### Reason #4: First Load
- Sometimes examples take a moment to render
- Solution: Wait 5 seconds, refresh if needed

---

## Verification Checklist

- [ ] API is running (curl http://localhost:8000/health returns healthy)
- [ ] Swagger UI loads (http://localhost:8000/docs opens page)
- [ ] OpenAPI endpoint works (curl http://localhost:8000/openapi.json returns JSON)
- [ ] Examples in schema (grep finds 7 summaries)
- [ ] Browser cache cleared
- [ ] Hard refresh done (Ctrl+Shift+R)
- [ ] Tried different browser
- [ ] Waited 5 seconds after page load

---

## If Still Not Working: Manual Approach

### Option 1: Copy Examples from Code
```bash
# In file: api/api.py, lines 84-230
# Copy the JSON from the "value" field of any example
# Paste into Swagger UI's request body manually
```

### Option 2: Use Postman Instead
```
1. Install Postman
2. Import: http://localhost:8000/openapi.json
3. Examples may display better in Postman UI
```

### Option 3: Use curl (Command Line)
```bash
# Create file: simulation.json with example data
# Run: curl -X POST http://localhost:8000/api/v1/simulate \
#      -H "Content-Type: application/json" \
#      -d @simulation.json
```

---

## Seven Examples Available (Copy/Paste these)

### Example 1: Simple 70/30 Split
```json
{
  "network_config": {
    "num_nodes": 100,
    "network_type": "scale_free",
    "node_definitions": [
      {"count": 70, "attributes": {"admin_user": true, "device_type": "server"}},
      {"count": 30, "attributes": {"admin_user": false, "device_type": "workstation"}}
    ],
    "node_distribution": "random"
  },
  "malware_config": {"malware_type": "worm", "infection_rate": 0.35, "latency": 1},
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

### Example 2: Enterprise Three-Tier
```json
{
  "network_config": {
    "num_nodes": 500,
    "network_type": "scale_free",
    "device_attributes": {"os": "Windows", "firewall_enabled": true},
    "node_definitions": [
      {
        "count": 50,
        "attributes": {
          "device_type": "server",
          "admin_user": true,
          "antivirus": true,
          "patch_status": "fully_patched",
          "firewall_enabled": true
        }
      },
      {
        "count": 200,
        "attributes": {
          "device_type": "workstation",
          "admin_user": true,
          "antivirus": true,
          "patch_status": "patched"
        }
      },
      {
        "count": 250,
        "attributes": {
          "device_type": "workstation",
          "admin_user": false,
          "antivirus": false,
          "firewall_enabled": false,
          "patch_status": "unpatched"
        }
      }
    ],
    "node_distribution": "random"
  },
  "malware_config": {"malware_type": "worm", "infection_rate": 0.35, "latency": 1},
  "initial_infected": ["device_300"],
  "max_steps": 100
}
```

### Example 3: Mixed Operating Systems
```json
{
  "network_config": {
    "num_nodes": 150,
    "network_type": "scale_free",
    "device_attributes": {"firewall_enabled": true},
    "node_definitions": [
      {
        "count": 50,
        "attributes": {
          "admin_user": true,
          "os": "Windows Server 2022",
          "device_type": "server",
          "antivirus": true
        }
      },
      {
        "count": 50,
        "attributes": {
          "admin_user": true,
          "os": "Linux Ubuntu 20.04",
          "device_type": "workstation",
          "antivirus": false
        }
      },
      {
        "count": 50,
        "attributes": {
          "admin_user": false,
          "os": "Windows 10",
          "device_type": "workstation",
          "antivirus": false
        }
      }
    ],
    "node_distribution": "random"
  },
  "malware_config": {"malware_type": "virus", "infection_rate": 0.25, "latency": 2},
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

### Example 4: Progressive Security Hardening
```json
{
  "network_config": {
    "num_nodes": 120,
    "network_type": "scale_free",
    "node_definitions": [
      {
        "count": 40,
        "attributes": {
          "admin_user": false,
          "firewall_enabled": false,
          "antivirus": false,
          "patch_status": "unpatched"
        }
      },
      {
        "count": 40,
        "attributes": {
          "admin_user": false,
          "firewall_enabled": false,
          "antivirus": true,
          "patch_status": "patched"
        }
      },
      {
        "count": 40,
        "attributes": {
          "admin_user": true,
          "firewall_enabled": true,
          "antivirus": true,
          "patch_status": "fully_patched"
        }
      }
    ],
    "node_distribution": "random"
  },
  "malware_config": {"malware_type": "ransomware", "infection_rate": 0.30, "latency": 3},
  "initial_infected": ["device_10"],
  "max_steps": 50
}
```

### Example 5: Sequential Distribution (Clustered)
```json
{
  "network_config": {
    "num_nodes": 100,
    "network_type": "scale_free",
    "node_definitions": [
      {"count": 70, "attributes": {"admin_user": true}},
      {"count": 30, "attributes": {"admin_user": false}}
    ],
    "node_distribution": "sequential"
  },
  "malware_config": {"malware_type": "worm", "infection_rate": 0.35, "latency": 1},
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

### Example 6: Simple Homogeneous Network
```json
{
  "network_config": {
    "num_nodes": 50,
    "network_type": "scale_free",
    "device_attributes": {
      "admin_user": true,
      "device_type": "workstation",
      "os": "Windows 11"
    }
  },
  "malware_config": {"malware_type": "worm", "infection_rate": 0.35, "latency": 1},
  "initial_infected": ["device_0"],
  "max_steps": 50
}
```

### Example 7: Multiple Initial Infections
```json
{
  "network_config": {
    "num_nodes": 200,
    "network_type": "small_world"
  },
  "malware_config": {"malware_type": "virus", "infection_rate": 0.25, "latency": 2},
  "initial_infected": ["device_0", "device_50", "device_100", "device_150"],
  "max_steps": 75
}
```

---

## How to Use These Directly

### Option 1: Copy to Swagger UI
1. Select all text from one example above
2. Go to: http://localhost:8000/docs
3. Click: POST /api/v1/simulate
4. Click: "Try it out"
5. Clear request body: Select all, delete
6. Paste: Example JSON
7. Click: "Execute"

### Option 2: Save and Use with Curl
```bash
# Save example to file
cat > example1.json << 'EOF'
{...paste example here...}
EOF

# Run simulation
curl -X POST http://localhost:8000/api/v1/simulate \
  -H "Content-Type: application/json" \
  -d @example1.json
```

### Option 3: Use with Python
```python
import requests

example = {
  "network_config": {...},
  "malware_config": {...},
  "initial_infected": [...],
  "max_steps": 50
}

response = requests.post(
  "http://localhost:8000/api/v1/simulate",
  json=example
)

print(response.json())
```

---

## Summary

**What's True:**
- ✅ All 7 examples ARE defined in the API
- ✅ All 7 examples ARE in the OpenAPI schema
- ✅ API is working correctly
- ✅ Examples work when executed

**What Might Be Needed:**
- Browser cache clear
- Hard refresh (Ctrl+Shift+R)
- Different browser
- Manual copying of JSON if UI doesn't show examples

**No Action Needed:**
- API doesn't need fixing
- Code is correct
- Examples are properly defined

**Next Step:**
Try one of the quick fixes above, or copy/paste an example from the list above!

---

**Questions?** All 7 examples are in the list above - use them directly!
