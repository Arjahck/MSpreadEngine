# MSpread WebUI - Copilot Instructions

## Project Overview

MSpread WebUI is a cybersecurity malware spread visualization dashboard that integrates with **MSpreadEngine** to run simulations. Built with:
- **React 19** with TypeScript
- **Vite 7** for fast development and building
- **Cytoscape.js** for interactive network topology visualization
- **Plotly.js** for advanced data analytics and charting
- **Tailwind CSS 4** with cyber-themed color scheme
- **MSpreadEngine API** (Python FastAPI) for malware simulations

## Architecture

### Frontend (MSpreadWebUI)
- React components for UI
- Cytoscape.js for network visualization
- Plotly.js for analytics
- HTTP API client for MSpreadEngine communication

### Backend (MSpreadEngine)
- Python malware simulation engine
- FastAPI REST API on http://localhost:8000
- NetworkX-based network topology
- Multiple malware types (worm, virus, ransomware)

## Project Structure

```
MSpreadWebUi/
├── src/
│   ├── components/
│   │   ├── CytoscapeGraph.tsx      # Network visualization (infected/healthy nodes)
│   │   ├── PlotlyChart.tsx         # Analytics and charts
│   │   ├── StatCard.tsx            # Statistics display
│   │   ├── SimulationControl.tsx   # Simulation parameter form
│   │   └── index.ts                # Component exports
│   ├── services/
│   │   └── simulationAPI.ts        # MSpreadEngine API client
│   ├── utils/
│   │   └── simulationTransform.ts  # API response transformation
│   ├── assets/                     # Static assets
│   ├── App.tsx                     # Main application (3-tab layout)
│   ├── App.css                     # App styles
│   ├── index.css                   # Global styles (Tailwind)
│   └── main.tsx                    # Entry point
├── public/                         # Public assets
├── tailwind.config.js              # Tailwind CSS configuration
├── postcss.config.js               # PostCSS configuration
├── vite.config.ts                  # Vite configuration
├── tsconfig.json                   # TypeScript main config
├── package.json                    # Dependencies and scripts
└── index.html                      # HTML entry point
```

## Development Workflow

### Getting Started

1. Start MSpreadEngine API:
```bash
# In MSpreadEngine directory
python main.py run
# API available at http://localhost:8000
```

2. Start MSpreadWebUI dev server:
```bash
# In MSpreadWebUi directory
npm install
npm run dev
# Available at http://localhost:5173/
```

### Building
```bash
npm run build      # Production build
npm run preview    # Preview production build
npm run lint       # Run ESLint
```

## Key Components

### SimulationControl Component
User interface for configuring and running simulations:
- **Network Configuration**: Nodes (10-500), Topology (scale-free, small-world, random, complete)
- **Malware Configuration**: Type (worm, virus, ransomware), Infection Rate (0.05-1.0)
- **Simulation Parameters**: Max Steps (10-500)
- **API Status**: Health check indicator and connection status
- **Error Handling**: User-friendly error messages

Located: [src/components/SimulationControl.tsx](src/components/SimulationControl.tsx)

### CytoscapeGraph Component
Interactive network visualization:
- **Node Types**: 
  - `infected`: Red nodes (malware-infected devices)
  - `healthy`: Green nodes (uninfected devices)
  - `firewall`, `server`, `client`, `router`, `threat`: Architecture nodes
- **Auto-layout**: CoSE algorithm for automatic positioning
- **Responsive**: Resizes with window
- **Styling**: Color-coded by type/status

Located: [src/components/CytoscapeGraph.tsx](src/components/CytoscapeGraph.tsx)

### PlotlyChart Component
Analytics visualization:
- Infection timeline (area chart showing spread over time)
- Infection distribution (pie chart of infected vs healthy)
- Dark cyber theme
- Interactive (hover, zoom, pan)

Located: [src/components/PlotlyChart.tsx](src/components/PlotlyChart.tsx)

### StatCard Component
Displays key metrics:
- Total devices, infected count, simulation steps, malware type
- Trend indicators (up/down/stable)
- Color-coded backgrounds
- Icon support

Located: [src/components/StatCard.tsx](src/components/StatCard.tsx)

## API Integration

### simulationAPI Service

Located: [src/services/simulationAPI.ts](src/services/simulationAPI.ts)

**Endpoints:**
- `POST /api/v1/simulate` - Run simulation
  - Request: Network config, malware config, max steps
  - Response: Simulation results with infection history
- `GET /health` - Health check

**Usage:**
```typescript
const result = await simulationAPI.runSimulation({
  network_config: {
    num_nodes: 50,
    network_type: 'scale_free'
  },
  malware_config: {
    malware_type: 'worm',
    infection_rate: 0.35
  },
  max_steps: 100
});
```

### Data Transformation

Located: [src/utils/simulationTransform.ts](src/utils/simulationTransform.ts)

**Functions:**
- `transformSimulationToNetwork()` - Convert API response to Cytoscape format
- `getInfectionTimeline()` - Prepare infection history for timeline chart
- `getMalwareDistribution()` - Prepare distribution data for pie chart

## Application Flow

1. **Overview Tab**: User configures simulation
   - Sets network topology (nodes, type)
   - Sets malware config (type, infection rate)
   - Clicks "Run Simulation"

2. **API Call**: 
   - SimulationControl calls simulationAPI.runSimulation()
   - Request sent to http://localhost:8000/api/v1/simulate
   - Displays loading state

3. **Results Processing**:
   - Response transformed using simulationTransform utilities
   - Network data → Cytoscape format
   - History → Chart data

4. **Visualization**:
   - Auto-switches to Network tab (infected/healthy nodes)
   - Analytics tab shows infection timeline & distribution
   - Overview tab displays statistics

## Styling Guide

### Tailwind CSS with Cyber Theme

Colors defined in [tailwind.config.js](tailwind.config.js):
- `cyber-dark`: #0a0e27 (main dark background)
- `cyber-darker`: #050810 (darker backgrounds)
- `cyber-blue`: #00d4ff (primary accent, text)
- `cyber-purple`: #7c3aed (secondary accent)
- `cyber-red`: #ff1744 (danger, infected)
- `cyber-green`: #00ff88 (success, healthy)
- `cyber-yellow`: #ffaa00 (warning)

### Color Usage Patterns
- Primary text/borders: `text-cyber-blue`, `border-cyber-blue`
- Backgrounds: `bg-cyber-dark`, `bg-cyber-darker`
- Infected nodes: Red (#ff1744)
- Healthy nodes: Green (#00ff88)
- Hover states: Use `/30` opacity for borders

## Configuration

### API Base URL
Change in [src/services/simulationAPI.ts](src/services/simulationAPI.ts):
```typescript
const API_BASE_URL = 'http://localhost:8000';
```

### Default Simulation Parameters
Change in [src/components/SimulationControl.tsx](src/components/SimulationControl.tsx):
- Initial node count
- Default topology type
- Default malware type
- Initial infection rate
- Default max steps

### Network Sampling
In [src/utils/simulationTransform.ts](src/utils/simulationTransform.ts):
- `sampleSize` parameter (default 100)
- Limits visualization to N nodes for performance

## Common Development Tasks

### Adding a New Malware Type
1. MSpreadEngine backend: Add to malware_engine/
2. SimulationControl: Add to malware_type select options
3. simulationAPI: Type already supports string type

### Modifying Network Node Colors
Edit node styles in [src/components/CytoscapeGraph.tsx](src/components/CytoscapeGraph.tsx) under `node.infected` and `node.healthy` selectors.

### Changing Chart Styling
Edit layout defaults in [src/components/PlotlyChart.tsx](src/components/PlotlyChart.tsx) `defaultLayout` object.

### Adding New Statistics Cards
Create StatCard instances in [src/App.tsx](src/App.tsx) with result data.

### Adjusting Simulation Parameters
Modify range/select inputs in [src/components/SimulationControl.tsx](src/components/SimulationControl.tsx).

## Error Handling & UX

### API Connection Errors
- Health check on component mount
- Visual indicator (red dot with "Disconnected")
- Error messages for failed requests
- "Check" button to retry connection
- Run button disabled if disconnected

### Simulation Errors
- Catch API errors in simulationAPI service
- Display error message in SimulationControl
- No state change on error (user can retry)

### Data Validation
- Ensure API response has required fields
- Handle empty history arrays
- Sample nodes if network too large

## Performance Notes

**Bundle Size:**
- Plotly.js: ~2MB (charting)
- Cytoscape.js: ~500KB (network viz)
- Total: ~5.5MB minified

**Optimization:**
- Dynamic imports for visualization components
- Network node sampling for large simulations
- Vite code-splitting enabled

**Simulation Performance:**
- Reduce node count for faster UI updates
- 50-100 nodes: responsive (< 1s)
- 500+ nodes: may take several seconds
- Check MSpreadEngine logs for bottlenecks

## Browser Support

- Chrome/Chromium (latest)
- Firefox (latest)
- Safari (latest)
- Edge (latest)
- Requires ES2022+ support

## Troubleshooting

### "API server is not responding"
- Ensure MSpreadEngine running: `python main.py run`
- Check http://localhost:8000/health in browser
- Verify no firewall blocking

### Simulation takes too long
- Reduce num_nodes (start with 50)
- Reduce max_steps
- Check server CPU/memory usage

### Empty network visualization
- Verify API returned valid data
- Check browser console for errors
- Ensure simulation completed successfully

### TypeScript errors
- Run `npm run build` to see full errors
- Clear `node_modules` if needed: `npm clean-install`
- Check tsconfig.json strict mode settings

## Next Steps for Enhancement

1. **Real-time Updates**: WebSocket for live simulation progress
2. **Export Features**: Download network graph, charts, CSV data
3. **Comparison Tools**: Run multiple simulations side-by-side
4. **Countermeasures**: Model firewall/patch interventions
5. **Prediction ML**: Use historical data for forecast
6. **Custom Networks**: Upload network topology files
7. **Recording**: Replay simulations with timeline scrubbing
8. **Mobile Responsive**: Adapt for tablet/mobile viewing

## Resources

- [React Documentation](https://react.dev)
- [Vite Guide](https://vite.dev)
- [TypeScript Handbook](https://www.typescriptlang.org/docs)
- [Cytoscape.js Documentation](https://cytoscape.org)
- [Plotly.js Documentation](https://plotly.com/javascript)
- [Tailwind CSS Documentation](https://tailwindcss.com)
- [MSpreadEngine API](../MSpreadEngine/README.md)
