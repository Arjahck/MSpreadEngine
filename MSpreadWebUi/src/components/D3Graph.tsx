import React, { useEffect, useRef, useMemo } from 'react';
import * as d3 from 'd3';

export interface D3Node extends d3.SimulationNodeDatum {
  id: string;
  label: string;
  type: 'firewall' | 'server' | 'client' | 'threat' | 'router' | 'infected' | 'healthy' | 'workstation';
  status?: 'healthy' | 'infected';
}

export interface D3Edge extends d3.SimulationLinkDatum<D3Node> {
  source: string | D3Node;
  target: string | D3Node;
  label?: string;
}

interface D3GraphProps {
  nodes: D3Node[];
  edges: D3Edge[];
  width?: number;
  height?: number;
}

export const D3Graph: React.FC<D3GraphProps> = ({ nodes, edges, width = 800, height = 600 }) => {
  const svgRef = useRef<SVGSVGElement>(null);

  // Deep copy nodes and edges for D3 simulation to avoid mutating props
  const simulationData = useMemo(() => {
    const d3Nodes: D3Node[] = nodes.map(n => ({ ...n }));
    const d3Edges: D3Edge[] = edges.map(e => ({ ...e }));
    return { nodes: d3Nodes, edges: d3Edges };
  }, [nodes, edges]);

  useEffect(() => {
    if (!svgRef.current) return;

    const svg = d3.select(svgRef.current);
    svg.selectAll('*').remove();

    const g = svg.append('g');

    // Add zoom behavior
    const zoom = d3.zoom<SVGSVGElement, unknown>()
      .scaleExtent([0.1, 4])
      .on('zoom', (event) => {
        g.attr('transform', event.transform);
      });

    svg.call(zoom);

    const simulation = d3.forceSimulation<D3Node>(simulationData.nodes)
      .force('link', d3.forceLink<D3Node, D3Edge>(simulationData.edges).id(d => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(40));

    // Draw edges
    const link = g.append('g')
      .selectAll('line')
      .data(simulationData.edges)
      .enter()
      .append('line')
      .attr('stroke', '#4a5568')
      .attr('stroke-opacity', 0.6)
      .attr('stroke-width', 2);

    // Draw nodes
    const node = g.append('g')
      .selectAll('g')
      .data(simulationData.nodes)
      .enter()
      .append('g')
      .call(d3.drag<SVGGElement, D3Node>()
        .on('start', (event, d) => {
          if (!event.active) simulation.alphaTarget(0.3).restart();
          d.fx = d.x;
          d.fy = d.y;
        })
        .on('drag', (event, d) => {
          d.fx = event.x;
          d.fy = event.y;
        })
        .on('end', (event, d) => {
          if (!event.active) simulation.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }) as any);

    // Node circles
    node.append('circle')
      .attr('r', 25)
      .attr('fill', d => {
        if (d.status === 'infected' || d.type === 'infected' || d.type === 'threat') return '#ff1744';
        if (d.status === 'healthy' || d.type === 'healthy' || d.type === 'client' || d.type === 'workstation') return '#00ff88';
        if (d.type === 'server') return '#00d4ff';
        if (d.type === 'router') return '#7c3aed';
        if (d.type === 'firewall') return '#ffa500';
        return '#cbd5e0';
      })
      .attr('stroke', '#0a0e27')
      .attr('stroke-width', 2)
      .attr('class', 'filter drop-shadow-lg');

    // Node labels
    node.append('text')
      .text(d => d.label || d.id)
      .attr('text-anchor', 'middle')
      .attr('dy', '.35em')
      .attr('fill', '#0a0e27')
      .attr('font-size', '10px')
      .attr('font-weight', 'bold')
      .style('pointer-events', 'none');

    simulation.on('tick', () => {
      link
        .attr('x1', d => (d.source as D3Node).x!)
        .attr('y1', d => (d.source as D3Node).y!)
        .attr('x2', d => (d.target as D3Node).x!)
        .attr('y2', d => (d.target as D3Node).y!);

      node
        .attr('transform', d => `translate(${d.x},${d.y})`);
    });

    return () => simulation.stop();
  }, [simulationData, width, height]);

  return (
    <div className="w-full h-full bg-cyber-darker relative overflow-hidden border border-cyber-blue/20 rounded-xl">
      <svg 
        ref={svgRef} 
        width="100%" 
        height="100%" 
        viewBox={`0 0 ${width} ${height}`}
        className="cursor-move"
      />
      <div className="absolute bottom-4 left-4 bg-cyber-dark/80 backdrop-blur-sm p-3 border border-cyber-blue/30 rounded text-xs text-cyber-blue">
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-cyber-green"></div> Healthy
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-cyber-red"></div> Infected
        </div>
        <div className="flex items-center gap-2 mb-1">
          <div className="w-3 h-3 rounded-full bg-cyber-blue"></div> Server
        </div>
        <div className="flex items-center gap-2">
          <div className="w-3 h-3 rounded-full bg-cyber-purple"></div> Router
        </div>
      </div>
    </div>
  );
};
