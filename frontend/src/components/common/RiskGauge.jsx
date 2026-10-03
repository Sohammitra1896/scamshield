import React from 'react';

function getRiskColor(level) {
  const value = (level || '').toUpperCase();

  if (value === 'HIGH RISK') {
    return 'text-rose-400 border-rose-500/30 bg-rose-500/10';
  }

  if (value === 'SUSPICIOUS') {
    return 'text-amber-400 border-amber-500/30 bg-amber-500/10';
  }

  if (value === 'LOW RISK') {
    return 'text-yellow-300 border-yellow-500/30 bg-yellow-500/10';
  }

  return 'text-emerald-400 border-emerald-500/30 bg-emerald-500/10';
}

function getGaugeColor(level) {
  const value = (level || '').toUpperCase();

  if (value === 'HIGH RISK') {
    return '#fb7185';
  }

  if (value === 'SUSPICIOUS') {
    return '#fbbf24';
  }

  if (value === 'LOW RISK') {
    return '#fde047';
  }

  return '#34d399';
}

export default function RiskGauge({ score = 0, riskLevel = 'SAFE' }) {
  const safeScore = Math.max(0, Math.min(100, Number(score) || 0));
  const color = getGaugeColor(riskLevel);

  return (
    <div className="flex flex-col items-center">
      <div
        className="relative w-44 h-44 rounded-full flex items-center justify-center"
        style={{
          background: `conic-gradient(${color} ${safeScore}%, rgba(51,65,85,0.35) ${safeScore}% 100%)`,
        }}
      >
        <div className="w-36 h-36 rounded-full bg-[#0A0F1D] border border-slate-800 flex flex-col items-center justify-center">
          <span className="text-4xl font-black text-white font-mono">
            {safeScore.toFixed(1)}
          </span>

          <span className="text-[10px] text-slate-500 uppercase tracking-widest mt-1">
            Risk Score
          </span>
        </div>
      </div>

      <div
        className={`mt-4 px-3 py-1.5 rounded-full border text-xs font-bold font-mono ${getRiskColor(
          riskLevel,
        )}`}
      >
        {(riskLevel || 'SAFE').toUpperCase()}
      </div>
    </div>
  );
}
