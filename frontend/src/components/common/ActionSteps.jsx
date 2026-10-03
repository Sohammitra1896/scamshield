import React from 'react';
import {
  LockKeyhole,
  ShieldCheck,
  ArrowRight,
} from 'lucide-react';

export default function ActionSteps({ recommendations = [] }) {
  const items = Array.isArray(recommendations)
    ? recommendations
    : [];

  return (
    <div className="rounded-xl border border-cyan-500/20 bg-cyan-500/5 p-5">
      <div className="flex items-center gap-3 mb-4">
        <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
          <LockKeyhole className="w-5 h-5 text-cyan-400" />
        </div>

        <div>
          <h3 className="text-sm font-bold text-white">
            Protect
          </h3>

          <p className="text-xs text-slate-500">
            Defensive actions returned by the analysis engine
          </p>
        </div>
      </div>

      {!items.length ? (
        <p className="text-sm text-slate-400">
          Verify important or unexpected requests before
          paying, clicking, or sharing sensitive information.
        </p>
      ) : (
        <div className="space-y-2">
          {items.map((item, index) => (
            <div
              key={`${item}-${index}`}
              className="flex items-start gap-3 rounded-lg border border-slate-800 bg-slate-950/50 p-3"
            >
              <ShieldCheck className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />

              <div className="flex-1 text-xs text-slate-300 leading-relaxed">
                {item}
              </div>

              <ArrowRight className="w-3.5 h-3.5 text-slate-600 mt-0.5 shrink-0" />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
