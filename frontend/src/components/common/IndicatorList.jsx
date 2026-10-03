import React from 'react';
import {
  AlertTriangle,
  ShieldAlert,
  FileSearch,
} from 'lucide-react';

function severityClass(severity) {
  const value = (severity || '').toLowerCase();

  if (value === 'high') {
    return 'border-rose-500/30 bg-rose-500/5';
  }

  if (value === 'medium') {
    return 'border-amber-500/30 bg-amber-500/5';
  }

  return 'border-cyan-500/20 bg-cyan-500/5';
}

function severityText(severity) {
  const value = (severity || '').toLowerCase();

  if (value === 'high') {
    return 'text-rose-400';
  }

  if (value === 'medium') {
    return 'text-amber-400';
  }

  return 'text-cyan-400';
}

export default function IndicatorList({ indicators = [] }) {
  if (!indicators.length) {
    return (
      <div className="rounded-xl border border-slate-800 bg-[#0A0F1D] p-5 text-center">
        <FileSearch className="w-6 h-6 mx-auto text-slate-600 mb-2" />

        <p className="text-sm text-slate-400">
          No deterministic rule indicators were matched.
        </p>

        <p className="text-xs text-slate-600 mt-1">
          The result may still contain model-derived evidence.
        </p>
      </div>
    );
  }

  return (
    <div className="space-y-3">
      {indicators.map((item, index) => (
        <div
          key={`${item.signal}-${index}`}
          className={`rounded-xl border p-4 ${severityClass(item.severity)}`}
        >
          <div className="flex items-start gap-3">
            <div className="mt-0.5">
              {item.severity?.toLowerCase() === 'high' ? (
                <ShieldAlert className="w-4 h-4 text-rose-400" />
              ) : (
                <AlertTriangle
                  className={`w-4 h-4 ${severityText(item.severity)}`}
                />
              )}
            </div>

            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-sm font-semibold text-white">
                  {item.signal}
                </span>

                <span
                  className={`text-[10px] uppercase font-mono ${severityText(
                    item.severity,
                  )}`}
                >
                  {item.severity}
                </span>

                <span className="text-[10px] uppercase font-mono text-slate-600">
                  {item.source}
                </span>
              </div>

              <p className="text-xs text-slate-400 mt-1 leading-relaxed">
                {item.description}
              </p>

              {item.matched_text && (
                <div className="mt-3 rounded-lg border border-slate-800 bg-slate-950/70 p-3">
                  <div className="text-[10px] uppercase tracking-wider font-mono text-slate-600 mb-1">
                    Matched Evidence
                  </div>

                  <blockquote className="text-sm text-slate-200 font-mono break-words">
                    "{item.matched_text}"
                  </blockquote>

                  {(item.start !== null && item.start !== undefined) &&
                    (item.end !== null && item.end !== undefined) && (
                      <div className="text-[10px] text-slate-600 font-mono mt-2">
                        offsets {item.start}–{item.end}
                      </div>
                    )}
                </div>
              )}
            </div>
          </div>
        </div>
      ))}
    </div>
  );
}
