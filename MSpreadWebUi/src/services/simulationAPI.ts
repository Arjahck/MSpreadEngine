// API service for MSpreadEngine integration

export interface DeviceAttributes {
  os?: string;
  firewall_enabled?: boolean;
  antivirus?: boolean;
  admin_user?: boolean;
  device_type?: 'server' | 'workstation' | 'router' | 'firewall';
}

export interface SubnetConfig {
  num_nodes: number;
  network_type: 'scale_free' | 'small_world' | 'random' | 'complete';
  device_attributes?: DeviceAttributes;
}

export interface Interconnect {
  source_subnet: number;
  target_subnet: number;
  source_node?: number;
  target_node?: number;
  firewall?: boolean;
}

export interface NetworkConfig {
  num_nodes?: number;
  network_type: 'scale_free' | 'small_world' | 'random' | 'complete' | 'segmented';
  device_attributes?: DeviceAttributes;
  subnets?: SubnetConfig[];
  interconnects?: Interconnect[];
}

export interface MalwareConfig {
  malware_type: 'worm' | 'virus' | 'ransomware' | 'trojan' | 'custom';
  infection_rate: number;
  latency?: number;
  spread_pattern?: 'random' | 'bfs' | 'dfs';
  avoids_admin?: boolean;
  requires_interaction?: boolean;
}

export interface SimulationRequest {
  network_config: NetworkConfig;
  malware_config: MalwareConfig;
  initial_infected?: string[];
  max_steps: number;
}

export interface SimulationResult {
  total_steps: number;
  total_devices: number;
  total_infected: number;
  infection_percentage: number;
  malware_type: string;
  history: Array<{
    step: number;
    infected_count: number;
    newly_infected: string[];
    devices_infected?: string[]; // Added for WS updates
  }>;
}

export interface WSMessage {
  type: 'initialized' | 'step' | 'complete' | 'error';
  total_devices?: number;
  initial_infected?: number;
  step?: number;
  newly_infected?: number;
  total_infected?: number;
  devices_infected?: string[];
  statistics?: SimulationResult;
  message?: string;
}

const API_BASE_URL = 'http://localhost:8000';
const WS_BASE_URL = 'ws://localhost:8000';

export const simulationAPI = {
  getWSUrl: () => `${WS_BASE_URL}/ws/simulate`,

  async runSimulation(config: SimulationRequest): Promise<SimulationResult> {
    try {
      const response = await fetch(`${API_BASE_URL}/api/v1/simulate`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(config),
        mode: 'cors',
        credentials: 'omit',
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.statusText}`);
      }

      return await response.json();
    } catch (error) {
      const message = error instanceof Error ? error.message : 'Unknown error';
      console.error('Simulation API Error:', message);
      throw new Error(`Failed to run simulation: ${message}`);
    }
  },

  async healthCheck(): Promise<boolean> {
    try {
      const response = await fetch(`${API_BASE_URL}/health`, {
        method: 'GET',
        mode: 'cors',
        credentials: 'omit',
      });
      console.log('Health check response:', response.status, response.statusText);
      return response.ok;
    } catch (error) {
      console.error('Health check failed:', error);
      return false;
    }
  },
};
