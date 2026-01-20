import React from 'react';

interface StatCardProps {
  title: string;
  value: string | number;
  unit?: string;
  color?: 'blue' | 'red' | 'green' | 'yellow' | 'purple';
}

export const StatCard: React.FC<StatCardProps> = ({
  title,
  value,
  unit,
  color = 'blue',
}) => {
  const colorMap = {
    blue: 'text-cyber-blue border-cyber-blue/20',
    red: 'text-cyber-red border-cyber-red/20',
    green: 'text-cyber-green border-cyber-green/20',
    yellow: 'text-cyber-yellow border-cyber-yellow/20',
    purple: 'text-cyber-purple border-cyber-purple/20',
  };

  return (
    <div className={`p-4 bg-black/40 backdrop-blur-md border ${colorMap[color]} rounded-xl shadow-inner group hover:bg-black/60 transition-all duration-300`}>
      <div className="text-[9px] font-black uppercase tracking-[0.2em] opacity-50 group-hover:opacity-100 transition-opacity mb-2">
        {title}
      </div>
      <div className="flex items-baseline gap-1">
        <span className="text-2xl font-black tracking-tighter text-white">
          {value}
        </span>
        {unit && (
          <span className="text-[9px] font-bold opacity-40 uppercase tracking-widest">
            {unit}
          </span>
        )}
      </div>
      <div className="mt-4 h-1 w-full bg-white/5 rounded-full overflow-hidden">
        <div 
          className={`h-full ${color === 'blue' ? 'bg-cyber-blue' : color === 'red' ? 'bg-cyber-red' : color === 'green' ? 'bg-cyber-green' : color === 'purple' ? 'bg-cyber-purple' : 'bg-cyber-yellow'} shadow-[0_0_10px_currentColor] transition-all duration-1000`}
          style={{ width: title === 'Infection %' ? `${value}%` : '66%' }}
        ></div>
      </div>
    </div>
  );
};
