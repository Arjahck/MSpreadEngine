import type { SimulationResult } from '../services/simulationAPI';

export interface NetworkNode {
  id: string;
  label: string;
  type: 'infected' | 'healthy' | 'threat';
}

export interface NetworkEdge {
  source: string;
  target: string;
  label?: string;
}

/**
 * Transform simulation API response into network graph format for Cytoscape
 */
export function transformSimulationToNetwork(
  result: SimulationResult,
  sampleSize: number = 100,
): { nodes: NetworkNode[]; edges: NetworkEdge[] } {
  // For visualization purposes, sample nodes if too many
  const totalNodes = result.total_devices;
  const nodes: NetworkNode[] = [];
  const edges: NetworkEdge[] = [];

  // Determine which nodes to show
  let nodesToShow = Math.min(sampleSize, totalNodes);
  const nodeIds = new Set<string>();

  // Get infected nodes from history
  const infectedIds = new Set(
    result.history.flatMap((step) => step.newly_infected).slice(0, nodesToShow / 2),
  );

  // Add infected nodes
  infectedIds.forEach((id) => {
    nodes.push({
      id,
      label: `${id}`,
      type: 'infected',
    });
    nodeIds.add(id);
  });

  // Add healthy nodes
  for (let i = nodesToShow - infectedIds.size; i > 0; i--) {
    const nodeId = `device_${nodes.length}`;
    if (!nodeIds.has(nodeId)) {
      nodes.push({
        id: nodeId,
        label: `${nodeId}`,
        type: 'healthy',
      });
      nodeIds.add(nodeId);
    }
  }

  // Create random edges to simulate network topology
  for (let i = 0; i < Math.min(nodes.length * 1.5, 150); i++) {
    const sourceIdx = Math.floor(Math.random() * nodes.length);
    const targetIdx = Math.floor(Math.random() * nodes.length);

    if (sourceIdx !== targetIdx) {
      edges.push({
        source: nodes[sourceIdx].id,
        target: nodes[targetIdx].id,
      });
    }
  }

  return { nodes, edges };
}

/**
 * Get infection timeline data for Plotly chart
 */
export function getInfectionTimeline(result: SimulationResult) {
  const steps = result.history.map((h) => h.step);
  const infectedCounts = result.history.map((h) => h.infected_count);
  const healthyCounts = result.history.map((h) => result.total_devices - h.infected_count);

  return [
    {
      x: steps,
      y: infectedCounts,
      name: 'Infected Devices',
      fill: 'tozeroy',
      line: { color: '#ff1744', width: 3 },
      fillcolor: 'rgba(255, 23, 68, 0.1)',
    },
    {
      x: steps,
      y: healthyCounts,
      name: 'Healthy Devices',
      fill: 'tozeroy',
      line: { color: '#00ff88', width: 3 },
      fillcolor: 'rgba(0, 255, 136, 0.1)',
    },
  ];
}

/**
 * Get malware type distribution pie chart data
 */
export function getMalwareDistribution(result: SimulationResult) {
  const labels = ['Infected', 'Healthy'];
  const values = [result.total_infected, result.total_devices - result.total_infected];
  const colors = ['#ff1744', '#00ff88'];

  return [
    {
      labels,
      values,
      type: 'pie',
      marker: { colors },
      textposition: 'inside',
      textinfo: 'label+percent',
    },
  ];
}
