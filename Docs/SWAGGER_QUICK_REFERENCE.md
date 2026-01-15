# Swagger Documentation Quick Reference

## 🚀 Quick Start

1. Start server: `python main.py run`
2. Open: `http://localhost:8000/docs`
3. Click: POST /api/v1/simulate
4. Select: Example from dropdown
5. Execute: Click "Try it out"

## 📋 The 7 Examples at a Glance

| # | Example | Devices | Distribution | Focus | Malware |
|---|---------|---------|--------------|-------|---------|
| 1 | 70/30 Split | 100 | Random | Basic segmentation | Worm |
| 2 | Enterprise 3-Tier | 500 | Random | Complex network | Worm |
| 3 | Mixed OS | 150 | Random | Heterogeneous systems | Virus |
| 4 | Security Hardening | 120 | Random | Defense layers | Ransomware |
| 5 | Sequential (Clustered) | 100 | Sequential | Comparison study | Worm |
| 6 | Homogeneous | 50 | - | Baseline | Worm |
| 7 | Multi-source | 200 | Random | Multiple infections | Virus |

## 🎯 Use Cases

**Want to learn basics?** → Example 1 (Simple 70/30)
**Simulate enterprise?** → Example 2 (Three-Tier)
**Test mixed OS?** → Example 3 (Mixed OS)
**Study defenses?** → Example 4 (Security Hardening)
**Compare strategies?** → Examples 5 vs 1 (Sequential vs Random)
**Need baseline?** → Example 6 (Homogeneous)
**Multi-infection?** → Example 7 (Multiple Sources)

## 📊 Topology Types Shown

```
Example 1-4, 6-7: scale_free     (Power-law, realistic)
Example 5:        scale_free     (For comparison)
Example 7:        small_world    (Clustering + shortcuts)
```

## 🦠 Malware Types Shown

```
Worm (latency=1):       Examples 1, 2, 5, 6
Virus (latency=2):      Examples 3, 7
Ransomware (latency=3): Example 4
```

## 🏗️ Structure Template

All examples follow this structure:

```json
{
  "network_config": {
    "num_nodes": <count>,
    "network_type": "<type>",
    "device_attributes": { /* optional */ },
    "node_definitions": [ /* optional */ ],
    "node_distribution": "<sequential|random>"
  },
  "malware_config": {
    "malware_type": "<worm|virus|ransomware>",
    "infection_rate": <0.0-1.0>,
    "latency": <0+>
  },
  "initial_infected": ["device_0"],
  "max_steps": <count>
}
```

## 🔧 Modify Examples

1. Select an example
2. Change `num_nodes` for different network size
3. Change `infection_rate` for different spread speed
4. Change `malware_type` for different behavior
5. Change `node_distribution` to see clustering effects
6. Add more `initial_infected` for multi-source spread
7. Click Execute to test

## 🎓 Learning Path

```
1. Read: Simple 70/30 (Example 1)
   ↓
2. Try: Homogeneous baseline (Example 6)
   ↓
3. Compare: Sequential vs Random (Examples 5 vs 1)
   ↓
4. Explore: Enterprise network (Example 2)
   ↓
5. Study: Mixed OS (Example 3)
   ↓
6. Analyze: Security hardening (Example 4)
   ↓
7. Advanced: Multiple infections (Example 7)
```

## 📝 Key Fields

**network_config:**
- `num_nodes`: 50-500 (adjust size)
- `network_type`: "scale_free" (realistic)
- `node_distribution`: "random" (recommended)

**malware_config:**
- `malware_type`: "worm" (fast), "virus" (medium), "ransomware" (slow)
- `infection_rate`: 0.25-0.4 (typical)
- `latency`: 1-3 (different types)

**Other:**
- `initial_infected`: Start with "device_0" or multiple
- `max_steps`: 50-100 (adjust simulation length)

## 🔍 Field Reference

| Field | Type | Example | Range |
|-------|------|---------|-------|
| num_nodes | int | 100 | 1+ |
| network_type | str | "scale_free" | scale_free, small_world, random, complete |
| infection_rate | float | 0.35 | 0.0-1.0 |
| latency | int | 1 | 0+ |
| malware_type | str | "worm" | worm, virus, ransomware |
| node_distribution | str | "random" | sequential, random |

## 💡 Pro Tips

1. **Copy to Postman**: Right-click → Copy JSON
2. **Test Different Rates**: Try infection_rate 0.1 to 0.9
3. **Compare Topologies**: Change network_type between examples
4. **Study Privilege**: Set admin_user true/false in node_definitions
5. **Measure Speed**: Check infection_percentage and total_steps
6. **Trace Spread**: Look at history array for infection path
7. **Mix Attributes**: Add custom attributes to node_definitions

## 🚨 Common Edits

**Larger network:**
```json
"num_nodes": 500  // was 100
```

**Slower spread:**
```json
"infection_rate": 0.1  // was 0.35
```

**More initial infections:**
```json
"initial_infected": ["device_0", "device_50", "device_100"]
```

**Different topology:**
```json
"network_type": "small_world"  // was scale_free
```

**Longer simulation:**
```json
"max_steps": 200  // was 50
```

## 📚 Related Documentation

- **Full Docs**: NODE_DEFINITIONS.md
- **Technical**: BATCH_LOGIC_IMPLEMENTATION.md
- **UI Guide**: SWAGGER_UI_GUIDE.md
- **Examples**: example_node_definitions.py

## ✅ Checklist for New Users

- [ ] Start API server
- [ ] Open Swagger UI at /docs
- [ ] Select Example 1 (70/30 Split)
- [ ] Click "Try it out"
- [ ] Execute request
- [ ] View response
- [ ] Try Example 6 (Homogeneous) for baseline
- [ ] Compare results
- [ ] Try modifying values
- [ ] Test different malware types
- [ ] Explore enterprise example

## 🎯 Expected Outcomes

Example 1 (70/30 Random):
- ~85-95% infection (worm is aggressive)
- ~6-10 steps to spread
- Random mixing shows realistic topology

Example 6 (Homogeneous Baseline):
- 95-100% infection (all admin)
- 5-8 steps (no barriers)
- Fastest spread scenario

Example 4 (Security Hardening):
- ~70-85% infection (defenses matter)
- ~8-12 steps (slower)
- Shows impact of layers

## 🔗 URLs

| URL | Purpose |
|-----|---------|
| http://localhost:8000/docs | Interactive Swagger UI |
| http://localhost:8000/redoc | ReDoc documentation |
| http://localhost:8000/openapi.json | OpenAPI schema |

## 📞 Support

- Check field descriptions in Swagger
- Read SWAGGER_UI_GUIDE.md for detailed help
- Review examples for valid payloads
- Modify examples incrementally to learn
- Check NODE_DEFINITIONS.md for features

---

**Summary**: 7 production-ready examples covering all features, from simple to enterprise scenarios. Use as learning tool, reference, or starting point for your simulations.
