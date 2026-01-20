import React, { useState } from 'react';
import type { SimulationRequest, NetworkConfig, MalwareConfig, SubnetConfig } from '../services/simulationAPI';

interface SimulationControlProps {
  onRun: (config: SimulationRequest) => void;
  isSimulating: boolean;
}

export const SimulationControl: React.FC<SimulationControlProps> = ({ onRun, isSimulating }) => {
  const [mode, setMode] = useState<'simple' | 'advanced'>('simple');
  
  // Simple Config State
  const [numNodes, setNumNodes] = useState(100);
  const [networkType, setNetworkType] = useState<NetworkConfig['network_type']>('scale_free');
  
  // Malware Config State
  const [malwareType, setMalwareType] = useState<MalwareConfig['malware_type']>('worm');
  const [infectionRate, setInfectionRate] = useState(0.35);
  const [latency, setLatency] = useState(1);
  const [spreadPattern, setSpreadPattern] = useState<MalwareConfig['spread_pattern']>('random');
  const [avoidsAdmin, setAvoidsAdmin] = useState(false);
  const [requiresInteraction, setRequiresInteraction] = useState(false);
  
  // Device Attributes
  const [os, setOs] = useState('Windows 11');
  const [firewall, setFirewall] = useState(true);
  const [antivirus, setAntivirus] = useState(true);
  const [adminUser, setAdminUser] = useState(false);

  // Advanced Config State
  const [subnets, setSubnets] = useState<SubnetConfig[]>([
    { num_nodes: 50, network_type: 'scale_free', device_attributes: { device_type: 'server', admin_user: true } }
  ]);

  const handleRun = () => {
    const config: SimulationRequest = {
      network_config: mode === 'simple' ? {
        num_nodes: numNodes,
        network_type: networkType,
        device_attributes: {
          os,
          firewall_enabled: firewall,
          antivirus,
          admin_user: adminUser
        }
      } : {
        network_type: 'segmented',
        subnets,
        interconnects: subnets.length > 1 ? [{
          source_subnet: 0,
          target_subnet: 1,
          firewall: true
        }] : []
      },
      malware_config: {
        malware_type: malwareType,
        infection_rate: infectionRate,
        latency,
        spread_pattern: spreadPattern,
        avoids_admin: avoidsAdmin,
        requires_interaction: requiresInteraction
      },
      max_steps: 200,
      initial_infected: ['device_0']
    };
    onRun(config);
  };

  const addSubnet = () => {
    setSubnets([...subnets, { num_nodes: 50, network_type: 'random' }]);
  };

  return (
    <div className="space-y-8 animate-in fade-in slide-in-from-right-4 duration-500">
      {/* Network Settings */}
      <section className="space-y-4">
        <h4 className="text-[10px] font-black text-cyber-blue uppercase tracking-[0.2em] opacity-80">Network Topology</h4>
        
        {/* Mode Selector */}
        <div className="flex p-1 bg-black/40 rounded-lg border border-white/5">
          <button 
            onClick={() => setMode('simple')}
            className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-widest rounded transition-all ${mode === 'simple' ? 'bg-cyber-blue text-cyber-darker shadow-[0_0_15px_rgba(0,212,255,0.3)]' : 'text-gray-500 hover:text-gray-300'}`}
          >
            Simple
          </button>
          <button 
            onClick={() => setMode('advanced')}
            className={`flex-1 py-2 text-[10px] font-bold uppercase tracking-widest rounded transition-all ${mode === 'advanced' ? 'bg-cyber-blue text-cyber-darker shadow-[0_0_15px_rgba(0,212,255,0.3)]' : 'text-gray-500 hover:text-gray-300'}`}
          >
            Segmented
          </button>
        </div>

        {mode === 'simple' ? (
          <div className="space-y-4">
            <div>
              <label className="block text-[11px] text-gray-500 mb-2 uppercase font-bold">Node Count: <span className="text-white">{numNodes}</span></label>
              <input 
                type="range" min="10" max="1000" step="10" 
                value={numNodes} onChange={(e) => setNumNodes(Number(e.target.value))}
                className="w-full h-1.5 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-cyber-blue"
              />
            </div>
            <div>
              <label className="block text-[11px] text-gray-500 mb-2 uppercase font-bold">Type</label>
              <select 
                value={networkType} onChange={(e) => setNetworkType(e.target.value as any)}
                className="w-full bg-black/50 border border-white/10 rounded p-2 text-xs focus:border-cyber-blue outline-none transition-colors"
              >
                <option value="scale_free">Scale Free</option>
                <option value="small_world">Small World</option>
                <option value="random">Random</option>
                <option value="complete">Complete</option>
              </select>
            </div>
          </div>
        ) : (
          <div className="space-y-3">
            {subnets.map((s, i) => (
              <div key={i} className="p-3 bg-white/5 border border-white/10 rounded flex justify-between items-center">
                <div>
                  <div className="text-[10px] font-bold text-white">Subnet {i+1}</div>
                  <div className="text-[9px] text-gray-500 uppercase">{s.num_nodes} Nodes • {s.network_type}</div>
                </div>
                <button onClick={() => setSubnets(subnets.filter((_, idx) => idx !== i))} className="text-cyber-red opacity-50 hover:opacity-100">×</button>
              </div>
            ))}
            <button 
              onClick={addSubnet}
              className="w-full py-2 border border-dashed border-cyber-blue/30 text-cyber-blue text-[10px] font-bold uppercase hover:bg-cyber-blue/5 transition-colors rounded"
            >
              + Add Subnet
            </button>
          </div>
        )}
      </section>

      {/* Malware Settings */}
      <section className="space-y-4">
        <h4 className="text-[10px] font-black text-cyber-red uppercase tracking-[0.2em] opacity-80">Payload Config</h4>
        <div className="grid grid-cols-2 gap-3">
          <div className="col-span-2">
            <label className="block text-[11px] text-gray-500 mb-2 uppercase font-bold">Infection Rate: <span className="text-white">{(infectionRate * 100).toFixed(0)}%</span></label>
            <input 
              type="range" min="0" max="1" step="0.05" 
              value={infectionRate} onChange={(e) => setInfectionRate(Number(e.target.value))}
              className="w-full h-1.5 bg-gray-800 rounded-lg appearance-none cursor-pointer accent-cyber-red"
            />
          </div>
          <div>
            <label className="block text-[11px] text-gray-500 mb-2 uppercase font-bold">Malware Type</label>
            <select 
              value={malwareType} onChange={(e) => setMalwareType(e.target.value as any)}
              className="w-full bg-black/50 border border-white/10 rounded p-2 text-xs outline-none"
            >
              <option value="worm">Worm</option>
              <option value="virus">Virus</option>
              <option value="ransomware">Ransomware</option>
              <option value="trojan">Trojan</option>
            </select>
          </div>
          <div>
            <label className="block text-[11px] text-gray-500 mb-2 uppercase font-bold">Pattern</label>
            <select 
              value={spreadPattern} onChange={(e) => setSpreadPattern(e.target.value as any)}
              className="w-full bg-black/50 border border-white/10 rounded p-2 text-xs outline-none"
            >
              <option value="random">Random</option>
              <option value="bfs">BFS Flood</option>
              <option value="dfs">DFS Targeted</option>
            </select>
          </div>
        </div>

        <div className="space-y-2">
           <label className="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" checked={avoidsAdmin} onChange={(e) => setAvoidsAdmin(e.target.checked)} className="sr-only peer" />
              <div className="w-8 h-4 bg-gray-800 rounded-full peer peer-checked:bg-cyber-red relative after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:after:translate-x-4"></div>
              <span className="text-[10px] text-gray-400 uppercase font-bold group-hover:text-gray-200">Avoids Admin Nodes</span>
           </label>
           <label className="flex items-center gap-3 cursor-pointer group">
              <input type="checkbox" checked={requiresInteraction} onChange={(e) => setRequiresInteraction(e.target.checked)} className="sr-only peer" />
              <div className="w-8 h-4 bg-gray-800 rounded-full peer peer-checked:bg-cyber-red relative after:content-[''] after:absolute after:top-0.5 after:left-0.5 after:bg-white after:rounded-full after:h-3 after:w-3 after:transition-all peer-checked:after:translate-x-4"></div>
              <span className="text-[10px] text-gray-400 uppercase font-bold group-hover:text-gray-200">Requires Interaction</span>
           </label>
        </div>
      </section>

      {/* Device Presets */}
      <section className="space-y-4">
        <h4 className="text-[10px] font-black text-gray-500 uppercase tracking-[0.2em] opacity-80">Device Hardening</h4>
        <div className="grid grid-cols-2 gap-4">
           <label className="flex flex-col gap-2">
              <span className="text-[9px] uppercase font-black text-gray-600">Firewall</span>
              <button onClick={() => setFirewall(!firewall)} className={`py-1 rounded text-[10px] font-bold uppercase ${firewall ? 'bg-cyber-green/20 text-cyber-green border border-cyber-green/30' : 'bg-white/5 text-gray-600 border border-white/5'}`}>
                {firewall ? 'Enabled' : 'Disabled'}
              </button>
           </label>
           <label className="flex flex-col gap-2">
              <span className="text-[9px] uppercase font-black text-gray-600">Antivirus</span>
              <button onClick={() => setAntivirus(!antivirus)} className={`py-1 rounded text-[10px] font-bold uppercase ${antivirus ? 'bg-cyber-green/20 text-cyber-green border border-cyber-green/30' : 'bg-white/5 text-gray-600 border border-white/5'}`}>
                {antivirus ? 'Active' : 'None'}
              </button>
           </label>
        </div>
      </section>

      {/* Run Button */}
      <button 
        disabled={isSimulating}
        onClick={handleRun}
        className={`w-full py-4 rounded-lg font-black uppercase tracking-[0.3em] text-sm transition-all shadow-2xl ${
          isSimulating 
            ? 'bg-gray-800 text-gray-600 cursor-not-allowed' 
            : 'bg-cyber-blue text-cyber-darker hover:scale-[1.02] active:scale-[0.98] hover:shadow-[0_0_30px_rgba(0,212,255,0.4)]'
        }`}
      >
        {isSimulating ? 'Processing...' : 'Initialize Simulation'}
      </button>
    </div>
  );
};
