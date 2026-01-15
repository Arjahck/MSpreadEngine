# MSpreadEngine Documentation

## 🎯 Welcome

This folder contains the complete documentation for the MSpreadEngine API.

## 📚 Core Documentation

| File | Purpose | Read Time |
|------|---------|-----------|
| **[SWAGGER_DOCUMENTATION.md](SWAGGER_DOCUMENTATION.md)** | **Start Here**. Detailed explanation of the API and examples | 10 min |
| **[SWAGGER_UI_GUIDE.md](SWAGGER_UI_GUIDE.md)** | Visual guide to using the Swagger UI | 8 min |
| **[WEBSOCKET_DOCUMENTATION.md](WEBSOCKET_DOCUMENTATION.md)** | Guide to real-time streaming API | 15 min |
| **[SWAGGER_QUICK_REFERENCE.md](SWAGGER_QUICK_REFERENCE.md)** | Cheat sheet for parameters and usage | 5 min |
| **[ARCHITECTURE_DIAGRAM.md](ARCHITECTURE_DIAGRAM.md)** | System design and data flow | 5 min |
| **[DOCUMENTATION_ROADMAP.md](DOCUMENTATION_ROADMAP.md)** | Map of all documentation files | 5 min |

## 🧩 Feature Documentation

| File | Purpose |
|------|---------|
| **[NODE_DEFINITIONS.md](NODE_DEFINITIONS.md)** | Guide to batch logic and node attributes |
| **[DEVICE_ATTRIBUTES.md](DEVICE_ATTRIBUTES.md)** | Reference for available device attributes |
| **[ADMIN_USER_LOGIC.md](ADMIN_USER_LOGIC.md)** | Explanation of privilege-based spreading |

## 🚀 Quick Start

**Step 1: Open Swagger UI**
```
Go to: http://localhost:8000/docs
```

**Step 2: Find the POST endpoint**
```
Scroll down and click blue box: POST /api/v1/simulate
```

**Step 3: Look for Examples dropdown**
```
Inside request body section, find: "Examples" dropdown
Should show 7 options (e.g., "Enterprise Three-Tier Network")
```

**Step 4: Execute**
```
Click "Try it out" -> Select Example -> Click "Execute"
```

## ❓ Common Questions

### Q: "How do I see the examples?"
**A**: Go to `/docs` and use the Examples dropdown in the request body.

### Q: "How do I use WebSocket?"
**A**: Read [WEBSOCKET_DOCUMENTATION.md](WEBSOCKET_DOCUMENTATION.md).

### Q: "What's the difference between sequential and random?"
**A**: Read [SWAGGER_DOCUMENTATION.md](SWAGGER_DOCUMENTATION.md).

### Q: "I need the full API reference"
**A**: Open http://localhost:8000/redoc

---

**Start with [SWAGGER_DOCUMENTATION.md](SWAGGER_DOCUMENTATION.md)**

