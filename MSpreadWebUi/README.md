# MSpread WebUI

MSpread WebUI is a high-performance, cybersecurity-themed dashboard for visualizing malware propagation simulations. It integrates with the **MSpreadEngine** backend to provide real-time insights into how different malware types spread across various network topologies.

## 🚀 Features

- **Real-Time Visualization**: Dynamic network graph powered by **D3.js** with live infection state updates via WebSockets.
- **Advanced Network Configuration**:
  - Multiple topologies: Scale-Free, Small-World, Random, and Complete.
  - **Segmented Networks**: Build complex architectures with interconnected subnets.
  - Device hardening presets (Firewall, AV, Admin rights).
- **Malware Simulation**:
  - Multiple payload types: Worms, Viruses, Ransomware, and Trojans.
  - Configurable spread patterns (BFS, DFS, Random).
  - Behavioral logic like "Avoids Admin Nodes".
- **Deep Analytics**:
  - Live propagation timeline charts using **Plotly.js**.
  - Detailed statistical summary (Infection rate, spread velocity, efficiency).
- **Modern Cyber UI**: Dark-themed, high-contrast interface built with **Tailwind CSS 4** and **React 19**.

## 🛠️ Tech Stack

- **Frontend**: React 19, TypeScript, Vite 7.
- **Styling**: Tailwind CSS 4.
- **Visualization**: D3.js (Network), Plotly.js (Analytics).
- **API**: WebSocket & REST communication with MSpreadEngine.

## 🏁 Getting Started

### Prerequisites

- Node.js (v18+)
- [MSpreadEngine](https://github.com/Arjahck/MSpreadEngine) (Backend API) running on `http://localhost:8000`.

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/Arjahck/MSpreadWebUi.git
   cd MSpreadWebUi
   ```

2. Install dependencies:
   ```bash
   npm install
   ```

3. Start the development server:
   ```bash
   npm run dev
   ```

4. Open your browser to `http://localhost:5173`.

## 📡 API Integration

The UI connects to the MSpreadEngine via:
- **WebSocket**: `ws://localhost:8000/ws/simulate` (Real-time updates)
- **REST**: `POST /api/v1/simulate` (Batch simulation)
- **Health**: `GET /health` (Connectivity monitoring)

## Project Structure

```
src/
├── components/                # Reusable React components
│   ├── CytoscapeGraph.tsx          # Network topology visualization
│   ├── PlotlyChart.tsx             # Analytics charts
│   ├── StatCard.tsx                # Statistics cards
│   ├── SimulationControl.tsx       # Simulation parameter controls
│   └── index.ts                    # Component exports
├── services/
│   └── simulationAPI.ts        # MSpreadEngine API client
├── utils/
│   └── simulationTransform.ts  # Data transformation utilities
├── assets/                     # Static assets
├── App.tsx                     # Main application component
├── App.css                     # Application styles
├── index.css                   # Global styles with Tailwind
└── main.tsx                    # Application entry point
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:5173/`

### Available Scripts

- `npm run dev` - Start development server with hot module replacement
- `npm run build` - Build for production with TypeScript type checking
- `npm run lint` - Run ESLint to check code quality
- `npm run preview` - Preview production build locally

## Usage

### Running Simulations

1. **Overview Tab**: Configure simulation parameters
   - **Network Configuration**: Set number of nodes and topology type
     - Scale-Free: Realistic power-law networks
     - Small-World: High clustering networks
     - Random: Erdős-Rényi networks
     - Complete: Fully connected networks
   - **Malware Configuration**: Choose malware type and infection rate
     - Worm: Fast, aggressive spreading
     - Virus: Selective spreading
     - Ransomware: Balanced approach
   - **Simulation Parameters**: Set maximum simulation steps

2. **Network Tab**: View live network topology
   - Red nodes: Infected devices
   - Green nodes: Healthy devices
   - Shows network structure during malware propagation

3. **Analytics Tab**: Analyze infection patterns
   - **Infection Timeline**: Graph showing infection growth over time
   - **Infection Distribution**: Pie chart of infected vs healthy devices

### API Integration

The application connects to MSpreadEngine API endpoints:

- **POST /api/v1/simulate**: Run a malware simulation
  ```json
  {
    "network_config": {
      "num_nodes": 50,
      "network_type": "scale_free"
    },
    "malware_config": {
      "malware_type": "worm",
      "infection_rate": 0.35,
      "latency": 1
    },
    "initial_infected": ["device_0"],
    "max_steps": 100
  }
  ```

- **GET /health**: Health check endpoint

## Components

### SimulationControl
Provides user interface for simulation configuration:
- Network configuration (nodes, topology)
- Malware configuration (type, infection rate)
- Simulation parameters (max steps)
- API health status indicator
- Error handling and feedback

### CytoscapeGraph
Renders interactive network topology:
- Supports multiple node types (infected, healthy, firewall, server, etc.)
- Auto-layouts using CoSE algorithm
- Responsive to window resizing
- Color-coded nodes for easy identification

### PlotlyChart
Displays analytics with cyber theme:
- Infection timeline (area chart)
- Infection distribution (pie chart)
- Dark theme with cyber colors
- Responsive and interactive

### StatCard
Shows key metrics with indicators:
- Real-time statistics
- Trend indicators
- Color-coded themes
- Custom icons

## Customization

### API Configuration

Edit the API base URL in [src/services/simulationAPI.ts](src/services/simulationAPI.ts):
```typescript
const API_BASE_URL = 'http://localhost:8000'; // Change this
```

### Colors

Cyber-themed colors in [tailwind.config.js](tailwind.config.js):
- `cyber-dark`: #0a0e27
- `cyber-darker`: #050810
- `cyber-blue`: #00d4ff
- `cyber-purple`: #7c3aed
- `cyber-red`: #ff1744
- `cyber-green`: #00ff88
- `cyber-yellow`: #ffaa00

### Simulation Parameters

Modify default values in [src/components/SimulationControl.tsx](src/components/SimulationControl.tsx):
- Default node count
- Default topology type
- Default malware type
- Default infection rate
- Default max steps

## Building for Production

Create an optimized production build:
```bash
npm run build
```

Output will be in the `dist/` directory.

## API Error Handling

The application includes:
- API health check on startup
- Connection status indicator
- Error messages for failed requests
- Graceful fallback to sample data
- Automatic reconnection hints

## Troubleshooting

### "API server is not responding"
- Ensure MSpreadEngine is running: `python main.py run`
- Check API is on localhost:8000
- Click "Check" button in Simulation Control to verify connection

### Simulation runs slowly
- Reduce number of nodes (10-100 for responsive UI)
- Reduce max steps
- Check that MSpreadEngine is not resource-constrained

### Empty network visualization
- Ensure simulation has completed successfully
- Check for API error messages
- Verify simulation returned valid network data

## Browser Support

- Chrome/Edge (latest)
- Firefox (latest)
- Safari (latest)
- Requires ES2022+ support

## Dependencies

### Main Dependencies
- react: ^19.0.0-rc
- react-dom: ^19.0.0-rc
- cytoscape: ^3.30.3
- plotly.js: ^2.34.0
- react-plotly.js: ^2.0.0

### Dev Dependencies
- vite: ^7.3.1
- typescript: ^5.6.3
- tailwindcss: ^4.0.0
- @tailwindcss/postcss: ^4.0.0
- autoprefixer: ^10.4.20
- postcss: ^8.4.47

## Performance Notes

Bundle includes large visualization libraries:
- Plotly.js: ~2MB (interactive charting)
- Cytoscape.js: ~500KB (network visualization)

For optimization:
- Consider dynamic imports for components
- Use build tool code splitting
- Enable gzip compression on production server

## Next Steps

1. **Scale Improvements**: Dynamic sampling for large networks
2. **Real-time Updates**: WebSocket integration for live simulations
3. **Export Features**: Download simulation data and visualizations
4. **Countermeasures**: Model defense mechanisms
5. **Comparison Tools**: Compare different simulation scenarios
6. **Machine Learning**: Predict infection patterns

## License

Proprietary - MSpread Project

## Support

For issues or questions:
1. Check MSpreadEngine API is running and healthy
2. Review error messages in Simulation Control
3. Check browser console for debugging information
4. Refer to MSpreadEngine documentation for simulation parameters

