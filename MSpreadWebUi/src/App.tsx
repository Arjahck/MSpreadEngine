import { useState, useEffect, useCallback, useRef } from 'react';
import './App.css';
import { D3Graph, PlotlyChart, StatCard, SimulationControl } from './components';
import type { SimulationResult, WSMessage, SimulationRequest } from './services/simulationAPI';
import { simulationAPI } from './services/simulationAPI';
import type { D3Node, D3Edge } from './components/D3Graph';

function App() {
  const [activeTab, setActiveTab] = useState<'settings' | 'analytics' | 'logs'>('settings');
  const [simulationResult, setSimulationResult] = useState<SimulationResult | null>(null);
  const [nodes, setNodes] = useState<D3Node[]>([]);
  const [edges, setEdges] = useState<D3Edge[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [isHealthy, setIsHealthy] = useState(false);
  const [currentStep, setCurrentStep] = useState(0);
  const [logs, setLogs] = useState<string[]>([]);
  const wsRef = useRef<WebSocket | null>(null);

  // Periodic Health Check
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const healthy = await simulationAPI.healthCheck();
        setIsHealthy(healthy);
      } catch (e) {
        setIsHealthy(false);
      }
    };

    checkHealth();
    const interval = setInterval(checkHealth, 5000); // Check every 5s
    return () => clearInterval(interval);
  }, []);

  // Initialize graph with some default nodes
  useEffect(() => {
    const initialNodes: D3Node[] = Array.from({ length: 20 }, (_, i) => ({
      id: `device_${i}`,
      label: `Device ${i}`,
      type: 'workstation',
      status: 'healthy'
    }));
    
    // Simple ring topology for initial view
    const initialEdges: D3Edge[] = initialNodes.map((node, i) => ({
      source: node.id,
      target: initialNodes[(i + 1) % initialNodes.length].id
    }));

    setNodes(initialNodes);
    setEdges(initialEdges);
  }, []);

  const handleRunSimulation = useCallback((config: SimulationRequest) => {
    if (wsRef.current) {
      wsRef.current.close();
    }

    setLogs([]);
    setCurrentStep(0);
    setIsSimulating(true);
    setSimulationResult(null);

    const ws = new WebSocket(simulationAPI.getWSUrl());
    wsRef.current = ws;

    ws.onopen = () => {
      console.log('WS Connected');
      ws.send(JSON.stringify(config));
    };

    ws.onmessage = (event) => {
      const msg: WSMessage = JSON.parse(event.data);
      console.log('WS Message:', msg);

      switch (msg.type) {
        case 'initialized':
          setLogs(prev => [...prev, `Simulation initialized with ${msg.total_devices} devices.`]);
          // Re-generate nodes if count changed
          if (msg.total_devices) {
             const newNodes: D3Node[] = Array.from({ length: msg.total_devices }, (_, i) => ({
                id: `device_${i}`,
                label: `Device ${i}`,
                type: 'workstation',
                status: 'healthy'
              }));
              setNodes(newNodes);
              // For now, edges are generated locally or we'd need them from API
              // For visualization, we'll generate a random topology if not provided
              const newEdges: D3Edge[] = [];
              for(let i=0; i < newNodes.length; i++) {
                if (i > 0) newEdges.push({ source: `device_${i-1}`, target: `device_${i}` });
              }
              setEdges(newEdges);
          }
          break;

        case 'step':
          setCurrentStep(msg.step || 0);
          setLogs(prev => [...prev, `Step ${msg.step}: ${msg.newly_infected} new infections.`]);
          
          if (msg.devices_infected) {
            setNodes(prevNodes => prevNodes.map(node => ({
              ...node,
              status: msg.devices_infected?.includes(node.id) ? 'infected' : node.status
            })));
          }
          break;

        case 'complete':
          setIsSimulating(false);
          setSimulationResult(msg.statistics || null);
          setLogs(prev => [...prev, 'Simulation complete!']);
          setActiveTab('analytics');
          ws.close();
          break;

        case 'error':
          setLogs(prev => [...prev, `Error: ${msg.message}`]);
          setIsSimulating(false);
          ws.close();
          break;
      }
    };

    ws.onerror = (err) => {
      console.error('WS Error:', err);
      setIsSimulating(false);
    };

    ws.onclose = () => {
      console.log('WS Closed');
    };
  }, []);

  return (
    <div className="h-screen w-screen bg-cyber-darker flex flex-col overflow-hidden text-gray-100 font-sans">
      {/* Header */}
      <header className="h-16 border-b border-cyber-blue/30 bg-cyber-dark flex items-center justify-between px-6 shrink-0">
        <div className="flex items-center gap-4">
          <div className="w-8 h-8 bg-cyber-blue rounded-md flex items-center justify-center font-bold text-cyber-darker">MS</div>
          <h1 className="text-xl font-bold tracking-tight text-cyber-blue uppercase">MSpread</h1>
        </div>
        <div className="flex items-center gap-6">
          <div className="flex items-center gap-2">
            <div className={`w-2 h-2 rounded-full ${isSimulating ? 'bg-cyber-red animate-pulse' : isHealthy ? 'bg-cyber-green' : 'bg-gray-600'}`}></div>
            <span className="text-xs font-mono uppercase tracking-widest">
              {isSimulating ? 'Simulating' : isHealthy ? 'Engine Ready' : 'Engine Offline'}
            </span>
          </div>
          <div className="text-xs font-mono text-gray-500 uppercase">v0.0.4-beta</div>
        </div>
      </header>

      {/* Main Body */}
      <div className="flex-1 flex overflow-hidden">
        {/* Left: D3 Graph */}
        <div className="flex-1 relative bg-[#050810]">
          <D3Graph nodes={nodes} edges={edges} />
          
          {/* Overlay Info */}
          <div className="absolute top-4 left-4 flex gap-4">
             <div className="bg-cyber-dark/80 backdrop-blur-md border border-cyber-blue/20 p-4 rounded-lg shadow-2xl">
                <div className="text-[10px] text-cyber-blue uppercase font-bold mb-1 tracking-tighter">Current Step</div>
                <div className="text-3xl font-black text-white leading-none">{currentStep}</div>
             </div>
             <div className="bg-cyber-dark/80 backdrop-blur-md border border-cyber-red/20 p-4 rounded-lg shadow-2xl">
                <div className="text-[10px] text-cyber-red uppercase font-bold mb-1 tracking-tighter">Infections</div>
                <div className="text-3xl font-black text-white leading-none">
                  {nodes.filter(n => n.status === 'infected').length}
                </div>
             </div>
          </div>
        </div>

        {/* Right: Sidebar Tabs */}
        <div className="w-96 border-l border-cyber-blue/30 bg-cyber-dark flex flex-col overflow-hidden">
          {/* Tab Headers */}
          <div className="flex border-b border-cyber-blue/20">
            {(['settings', 'analytics', 'logs'] as const).map(tab => (
              <button
                key={tab}
                onClick={() => setActiveTab(tab)}
                className={`flex-1 py-4 text-[11px] font-bold uppercase tracking-widest transition-all ${
                  activeTab === tab 
                    ? 'text-cyber-blue border-b-2 border-cyber-blue bg-cyber-blue/5' 
                    : 'text-gray-500 hover:text-gray-300'
                }`}
              >
                {tab}
              </button>
            ))}
          </div>

          {/* Tab Content */}
          <div className="flex-1 overflow-y-auto p-6 scrollbar-thin scrollbar-thumb-cyber-blue/20">
            {activeTab === 'settings' && (
              <SimulationControl onRun={handleRunSimulation} isSimulating={isSimulating} />
            )}

            {activeTab === 'analytics' && (
              <div className="space-y-6">
                <h3 className="text-sm font-bold text-cyber-blue uppercase tracking-widest border-b border-cyber-blue/10 pb-2">Results Summary</h3>
                {simulationResult ? (
                  <div className="space-y-6">
                    <div className="grid grid-cols-2 gap-3">
                      <StatCard title="Total Devices" value={simulationResult.total_devices} unit="nodes" color="blue" />
                      <StatCard title="Total Infected" value={simulationResult.total_infected} unit="nodes" color="red" />
                      <StatCard title="Infection %" value={simulationResult.infection_percentage.toFixed(1)} unit="%" color="yellow" />
                      <StatCard title="Total Steps" value={simulationResult.total_steps} unit="steps" color="purple" />
                    </div>
                    <div className="h-64 mt-4 bg-black/20 rounded-xl p-2 border border-white/5">
                      <PlotlyChart 
                        title="MALWARE PROPAGATION TIMELINE"
                        data={[{
                          x: simulationResult.history.map(h => h.step),
                          y: simulationResult.history.map(h => h.infected_count || (h as any).total_infected),
                          type: 'scatter',
                          mode: 'lines+markers',
                          fill: 'tozeroy',
                          line: { color: '#00d4ff', width: 2 },
                          fillcolor: 'rgba(0, 212, 255, 0.1)',
                          name: 'Infected'
                        }]}
                        layout={{
                          xaxis: { title: { text: 'SIMULATION STEP', font: { size: 8 } } },
                          yaxis: { title: { text: 'DEVICES INFECTED', font: { size: 8 } } }
                        }}
                      />
                    </div>
                  </div>
                ) : (
                  <div className="text-center py-20 border-2 border-dashed border-cyber-blue/10 rounded-xl">
                    <p className="text-gray-600 text-xs italic">No simulation data yet.</p>
                  </div>
                )}
              </div>
            )}

            {activeTab === 'logs' && (
              <div className="h-full flex flex-col">
                <h3 className="text-sm font-bold text-cyber-blue uppercase tracking-widest border-b border-cyber-blue/10 pb-2 mb-4">Event Stream</h3>
                <div className="flex-1 font-mono text-[10px] space-y-1 bg-black/30 p-4 rounded border border-white/5 overflow-y-auto">
                  {logs.length === 0 && <span className="text-gray-700">Waiting for stream...</span>}
                  {logs.map((log, i) => (
                    <div key={i} className="flex gap-2">
                      <span className="text-cyber-blue/50">[{new Date().toLocaleTimeString()}]</span>
                      <span className={log.includes('Error') ? 'text-cyber-red' : 'text-gray-400'}>{log}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;
