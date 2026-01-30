# MSpreadEngine Frontend Development Context

## Project Overview
MSpreadEngine is a backend simulation engine for malware propagation over networks. The frontend needs to visualize these simulations in real-time (using WebSockets) or display static results (using REST).

**Base URL:** `http://localhost:8000`
**WebSocket URL:** `ws://localhost:8000`

---

## 1. API Integration

### A. Real-Time Simulation (Primary)
**Endpoint:** `ws://localhost:8000/ws/simulate`
**Protocol:** WebSocket

**Flow:**
1.  **Connect** to WebSocket.
2.  **Send Configuration** (JSON) immediately upon connection.
3.  **Listen** for incoming messages (Types: `initialized`, `step`, `complete`, `error`).

**Client -> Server (Configuration Payload):**
```json
{
  "network_config": {
    "num_nodes": 100,             // Integer: 10 - 30000+
    "network_type": "scale_free", // Enum: "scale_free", "small_world", "random", "complete"
    "device_attributes": {        // Optional: Default settings for all nodes
      "os": "Windows Server 2019",
      "firewall_enabled": true,
      "antivirus": true,
      "admin_user": true          // Crucial: controls lateral movement capabilities
    }
  },
  "malware_config": {
    "malware_type": "worm",       // Enum: "worm", "virus", "ransomware", "trojan", "custom"
    "infection_rate": 0.35,       // Float: 0.0 - 1.0 (Probability)
    "latency": 1,                 // Integer: Steps before becoming infectious
    "spread_pattern": "random",   // Enum: "random", "bfs", "dfs"
    "avoids_admin": false,        // Boolean: If true, won't attack admin nodes from non-admin
    "requires_interaction": false // Boolean: Reduces infection chance
  },
  "initial_infected": ["device_0"], // List[str]: ID of patient zero
  "max_steps": 100                  // Integer: Safety limit
}
```

**Server -> Client (Message Types):**

1.  **Initialized:**
    ```json
    { 
      "type": "initialized", 
      "total_devices": 100, 
      "initial_infected": 1,
      "initial_infected_ids": ["device_0"] 
    }
    ```
    *UI Action:* specific "Reset graph", draw nodes. **Crucial:** Immediately apply "Infected" styling (Red) to all nodes listed in `initial_infected_ids`.

2.  **Step Update:**
    ```json
    {
      "type": "step",
      "step": 5,
      "newly_infected": 3,
      "total_infected": 15,
      "devices_infected": ["device_10", "device_45", "device_99"]
    }
    ```
    *UI Action:* Update progress bar, turn specific node IDs red/infected color, update live counters.

3.  **Complete:**
    ```json
    {
      "type": "complete",
      "statistics": { /* Full summary object */ }
    }
    ```
    *UI Action:* Close socket, show final stats modal.

### B. Static Simulation (Batch)
**Endpoint:** `POST /api/v1/simulate`
**Usage:** For generating data without watching the animation.
**Request Body:** Same as WebSocket Configuration Payload.
**Response:** Returns the full simulation history and stats in one JSON object.

### C. Health Check
**Endpoint:** `GET /health`
**Response:** `{ "status": "healthy" }`

---

## 2. UI Controls & Parameters

The frontend should generate a form with the following inputs mapping to the JSON payload.

### A. Standard Node Network (Single Topology)
Used for creating a single, uniform network (e.g., one office or one server cluster).

*   **Topology:** Dropdown [`scale_free`, `small_world`, `random`, `complete`]
*   **Node Count:** Slider/Input [Range: 10 - 5000].
*   **Device Attributes:**
    *   **OS / Device Type:** **Hybrid Input (Combobox)**.
        *   *Presets:* "Windows 11 Enterprise", "Windows Server 2022", "Ubuntu 22.04 LTS", "macOS Sonoma".
        *   *Custom:* User can type any string (e.g., "Legacy SCADA System").
    *   **Security:** Toggle for "Firewall Enabled", Toggle for "Admin User".
    *   **Vulnerabilities (CVEs):** **Tag Input / Multi-select**.
        *   User can add CVE IDs (e.g., `CVE-2021-44228`).
        *   This maps to the `default_vulnerabilities` array in the JSON.

### B. Segmented Node Network (Advanced Enterprise)
Used for creating multiple interconnected subnets (e.g., Corporate LAN + Server Farm + DMZ).
*   **Mode Switch:** Toggle between "Standard Node Network" and "Segmented Node Network".
*   **Subnet Builder:** Allow adding multiple groups (subnets), each with their own "Standard Node Network" settings (OS, CVEs, etc.).
*   **Interconnects:** UI to draw or define links between these subnets (optionally adding Firewalls on the bridges).

### Malware Settings
*   **Type:** Dropdown [`worm` (standard), `virus` (high spread), `ransomware` (destructive), `trojan` (stealthy)].
*   **Infection Rate:** Slider [0.0 - 1.0].
*   **Spreading Logic:** Dropdown [`random` (Standard), `bfs` (Aggressive flood), `dfs` (Targeted)].
*   **Behaviors:** Toggles for "Avoids Admin", "Requires User Interaction".

### Segmented Node Network (Advanced)
If `network_type` is `segmented`, the `subnets` and `interconnects` arrays are required (as defined in previous contexts).

---

## 4. Visualization Requirements

### Graph Visualization
*   The backend works with Node IDs formatted as `device_0`, `device_1`, etc.
*   **Technique:** Use a library like `D3.js`.
*   **Logic:**
    1.  Generate visual nodes `0` to `N` based on `network_config.num_nodes`.
    2.  Links/Edges are determined by the topology (Note: The backend *calculates* the topology. For exact visual replication, the frontend might need to either mock the topology generation locally or request the edge list from the backend if an endpoint exists. *Current API implies frontend generates visual graph, backend simulates logic on matching IDs*).

### Dashboard Metrics
1.  **Infected Count:** `total_infected` / `total_devices` (Big Number & Gauge).
2.  **Timeline:** Line chart updating every `step` message (X=Step, Y=Infected Count).
3.  **Logs:** Scrollable text area showing `devices_infected` arrays per step.

---

## 4. Key Logic Notes
*   **Admin User Attribute:** If a node has `admin_user: false`, it cannot spread malware to a node with `admin_user: true` if `avoids_admin` is set.
*   **Latency:** A node infected at step `X` with latency `2` starts spreading at step `X+2`.
