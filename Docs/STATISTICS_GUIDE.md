# Statistics Guide: Network & Simulation Metrics

MSpreadEngine collects comprehensive statistics to help analyze network vulnerability and malware behavior. This guide explains the available metrics.

## 1. Network Topology Statistics

These metrics describe the structural properties of your network before or during simulation.

### Core Metrics
- **`num_nodes`**: Total number of devices in the network.
- **`num_edges`**: Total number of connections between devices.
- **`density`**: The ratio of actual connections to potential connections. A value of 1.0 means a fully connected network.

### Structural Vulnerability (Medium/High Cost)
*Note: These are calculated unless `skip_expensive=True` is passed to `get_statistics()`.*

- **`avg_degree`**: Average number of connections per device. Higher values usually mean faster malware spread.
- **`max_degree`**: The number of connections on the most connected device (the "Hub"). In scale-free networks, hubs are critical targets.
- **`num_components`**: Number of isolated sub-networks. A value of 1 means all devices are reachable.
- **`giant_component_size`**: The number of nodes in the largest connected part of the network.
- **`avg_clustering`**: Measures the degree to which nodes tend to cluster together (forming "cliques").
- **`assortativity`**: Measures if highly connected nodes tend to connect to other highly connected nodes. Positive assortativity means the network core is very dense.
- **`diameter`**: The longest shortest path between any two nodes. Represents the maximum "distance" malware has to travel.

### Attribute Demographics
- **`admin_ratio`**: Percentage of nodes with `admin_user=True`.
- **`os_breakdown`**: A count of devices per operating system (e.g., Windows, Linux).

---

## 2. Simulation Performance Statistics

These metrics describe how the malware behaved during a specific run.

### Spread Severity
- **`total_infected`**: Final count of compromised devices.
- **`infection_percentage`**: Severity of the outbreak relative to network size.
- **`total_steps`**: How many time-steps the simulation ran before stopping.

### Velocity & Dynamics (`performance`)
- **`peak_velocity`**: The maximum number of new infections that occurred in a single time-step.
- **`step_at_peak`**: The time-step when the spread was at its most aggressive.
- **`steps_to_50_percent`**: How many steps it took to compromise half the network.
- **`steps_to_90_percent`**: How many steps it took to reach near-total saturation.

### Target Analysis (`infected_demographics`)
- **`os_breakdown`**: Provides a breakdown of which operating systems were actually infected. This helps verify if your malware targeted specific OS types correctly.

---

## 3. Best Practices for Large Networks

Calculating global metrics like **diameter** or **clustering** on networks with >10,000 nodes can be very slow ($O(n^2)$ or $O(n^3)$).

**Recommendations:**
- Use `skip_expensive=True` when running large-scale simulations (>5,000 nodes) if you only need infection counts.
- For structural analysis, use smaller sample networks (100–1,000 nodes) to understand the topology properties.
- Use the **Peak Velocity** metric to identify when your defense countermeasures (if implemented) should have triggered.
