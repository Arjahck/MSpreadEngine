import React, { useEffect, useRef } from 'react';
import cytoscape from 'cytoscape';

export interface Node {
  id: string;
  label: string;
  type: 'firewall' | 'server' | 'client' | 'threat' | 'router' | 'infected' | 'healthy';
}

export interface Edge {
  source: string;
  target: string;
  label?: string;
}

interface CytoscapeGraphProps {
  nodes: Node[];
  edges: Edge[];
  title?: string;
}

export const CytoscapeGraph: React.FC<CytoscapeGraphProps> = ({ nodes, edges, title = 'Network Topology' }) => {
  const containerRef = useRef<HTMLDivElement>(null);
  const cyRef = useRef<cytoscape.Core | null>(null);

  useEffect(() => {
    if (!containerRef.current) return;

    const nodeElements = nodes.map(node => ({
      data: { id: node.id, label: node.label, type: node.type },
      classes: node.type,
    }));

    const edgeElements = edges.map(edge => ({
      data: {
        id: `${edge.source}-${edge.target}`,
        source: edge.source,
        target: edge.target,
        label: edge.label || '',
      },
    }));

    const cy = cytoscape({
      container: containerRef.current,
      elements: [...nodeElements, ...edgeElements],
      style: [
        {
          selector: 'node',
          style: {
            'content': 'data(label)',
            'text-valign': 'center',
            'text-halign': 'center',
            'width': '60px',
            'height': '60px',
            'font-size': '12px',
            'color': '#0a0e27',
          } as any,
        },
        {
          selector: 'node.firewall',
          style: {
            'background-color': '#ffa500',
            'border-width': '3px',
            'border-color': '#ff8c00',
          } as any,
        },
        {
          selector: 'node.server',
          style: {
            'background-color': '#00d4ff',
            'border-width': '2px',
            'border-color': '#0a0e27',
          } as any,
        },
        {
          selector: 'node.client',
          style: {
            'background-color': '#00ff88',
            'border-width': '2px',
            'border-color': '#0a0e27',
          } as any,
        },
        {
          selector: 'node.threat',
          style: {
            'background-color': '#ff1744',
            'border-width': '3px',
            'border-color': '#ff0040',
            'shape': 'triangle',
          } as any,
        },
        {
          selector: 'node.router',
          style: {
            'background-color': '#7c3aed',
            'border-width': '2px',
            'border-color': '#0a0e27',
            'shape': 'diamond',
          } as any,
        },
        {
          selector: 'node.infected',
          style: {
            'background-color': '#ff1744',
            'border-width': '3px',
            'border-color': '#ff0040',
          } as any,
        },
        {
          selector: 'node.healthy',
          style: {
            'background-color': '#00ff88',
            'border-width': '2px',
            'border-color': '#00d4ff',
          } as any,
        },
        {
          selector: 'edge',
          style: {
            'stroke-width': 2,
            'stroke': '#00d4ff',
            'target-arrow-color': '#00d4ff',
            'target-arrow-shape': 'triangle',
            'curve-style': 'bezier',
            'text-background-color': '#0a0e27',
            'text-background-opacity': 0.8,
            'text-background-padding': '2px',
          } as any,
        },
      ],
      layout: {
        name: 'cose',
        animate: true,
        animationDuration: 500,
        avoidOverlap: true,
        nodeSpacing: 10,
      } as any,
    });

    cyRef.current = cy;

    // Handle responsive resizing
    const handleResize = () => {
      if (cy && containerRef.current) {
        (cy as any).resize();
        (cy as any).fit();
      }
    };

    window.addEventListener('resize', handleResize);

    // Initial fit
    (cy as any).fit();

    return () => {
      window.removeEventListener('resize', handleResize);
      cy.destroy();
    };
  }, [nodes, edges]);

  return (
    <div className="w-full h-full flex flex-col">
      <div className="p-4 border-b border-cyber-blue/30">
        <h2 className="text-xl font-semibold text-cyber-blue">{title}</h2>
      </div>
      <div
        ref={containerRef}
        className="flex-1 bg-cyber-darker"
        style={{ minHeight: '400px' }}
      />
    </div>
  );
};
