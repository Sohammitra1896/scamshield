import React from 'react';
import { Activity, TrendingDown, TrendingUp } from 'lucide-react';

export default function TopFeaturesChart({
  riskDrivers = [],
  legitimacyDrivers = [],
  prediction = 'scam',
}) {
  const drivers =
    prediction === 'scam' ? riskDrivers : legitimacyDrivers;

  if (!drivers.length) {
    return (
      <div className="rounded-xl border border-slate-800 bg-[#0A0F1D] p-5 text-center">
        <Activity className="w-5 h-5 mx-auto text-slate-600 mb-2" />
        <p className="text-sm text-slate-500">
          No model drivers were returned.
        </p>
      </div>
    );
  }

  const visibleDrivers = [...drivers]
    .sort(
      (a, b) =>
        Math.abs(Number(b.contribution)) -
        Math.abs(Number(a.contribution)),
    )
    .slice(0, 8);

  const maxValue = Math.max(
    ...visibleDrivers.map((item) =>
      Math.abs(Number(item.contribution) || 0),
    ),
    0.0001,
  );

  return (
    <div className="space-y-3">
      {visibleDrivers.map((item, index) => {
        const contribution = Number(item.contribution) || 0;
        const width =
          (Math.abs(contribution) / maxValue) * 100;

        const positive = contribution >= 0;

        return (
          <div
            key={`${item.feature}-${index}`}
            className="rounded-lg border border-slate-800 bg-slate-950/50 p-3"
          >
            <div className="flex items-center justify-between gap-3 mb-2">
              <div className="flex items-center gap-2 min-w-0">
                {positive ? (
                  <TrendingUp className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                ) : (
                  <TrendingDown className="w-3.5 h-3.5 text-emerald-400 shrink-0" />
                )}

                <span className="text-xs text-slate-300 font-mono truncate">
                  {item.feature}
                </span>
              </div>

              <span
                className={`text-[11px] font-mono ${
                  positive
                    ? 'text-rose-400'
                    : 'text-emerald-400'
                }`}
              >
                {contribution >= 0 ? '+' : ''}
                {contribution.toFixed(4)}
              </span>
            </div>

            <div className="h-1.5 rounded-full bg-slate-800 overflow-hidden">
              <div
                className="h-full rounded-full"
                style={{
                  width: `${width}%`,
                  backgroundColor: positive
                    ? '#fb7185'
                    : '#34d399',
                }}
              />
            </div>
          </div>
        );
      })}
    </div>
  );
}
