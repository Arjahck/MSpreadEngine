import React from 'react';
import Plot from 'react-plotly.js';

interface PlotlyChartProps {
  title?: string;
  data: any[];
  layout?: any;
  config?: any;
}

export const PlotlyChart: React.FC<PlotlyChartProps> = ({
  title,
  data,
  layout = {},
  config = {},
}) => {
  const defaultLayout = {
    title: title ? {
      text: title,
      font: { color: 'rgba(255,255,255,0.9)', size: 12, family: 'JetBrains Mono, monospace' },
      x: 0.05
    } : undefined,
    paper_bgcolor: 'rgba(0,0,0,0)',
    plot_bgcolor: 'rgba(0,0,0,0)',
    font: {
      color: 'rgba(255,255,255,0.7)',
      family: 'JetBrains Mono, monospace',
      size: 10
    },
    xaxis: {
      gridcolor: 'rgba(255,255,255,0.05)',
      linecolor: 'rgba(255,255,255,0.1)',
      zeroline: false
    },
    yaxis: {
      gridcolor: 'rgba(255,255,255,0.05)',
      linecolor: 'rgba(255,255,255,0.1)',
      zeroline: false
    },
    margin: { l: 40, r: 20, t: 40, b: 40 },
    hovermode: 'x unified',
    ...layout,
  };

  const defaultConfig = {
    responsive: true,
    displayModeBar: false,
    ...config,
  };

  return (
    <div className="w-full h-full">
      <Plot
        data={data}
        layout={defaultLayout}
        config={defaultConfig}
        style={{ width: '100%', height: '100%' }}
      />
    </div>
  );
};
