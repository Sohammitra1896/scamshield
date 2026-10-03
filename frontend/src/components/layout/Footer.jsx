import React from 'react';
import {
  LockKeyhole,
  Shield,
  Terminal,
} from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-[#0A0F1D] mt-16">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-10">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          <div>
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-cyan-400" />

              <span className="font-black text-white">
                ScamShield
              </span>
            </div>

            <p className="text-xs text-slate-500 mt-3 leading-relaxed max-w-sm">
              Explainable scam detection platform for the INNOV12
              Cyber & Digital Trust track.
            </p>

            <div className="flex items-center gap-2 text-[10px] text-cyan-400 font-mono mt-4">
              <Terminal className="w-3 h-3" />
              DETECT → EXPLAIN → PROTECT
            </div>
          </div>

          <div>
            <h3 className="text-[10px] font-mono uppercase tracking-widest text-slate-600">
              Team OBSIDIAN
            </h3>

            <div className="space-y-2 mt-4 text-xs">
              <div className="text-slate-300">Soham Mitra — CSE</div>
              <div className="text-slate-300">
                Khyati K Doshi — CSE (IOTCSBT)
              </div>
              <div className="text-slate-300">
                Srinistha Biswas — CSE (IOTCSBT)
              </div>
            </div>
          </div>

          <div>
            <h3 className="text-[10px] font-mono uppercase tracking-widest text-slate-600">
              Architecture
            </h3>

            <div className="space-y-2 mt-4 text-xs text-slate-500">
              <div>Frontend: React + Vite</div>
              <div>Backend: FastAPI + Python</div>
              <div>Analysis: ML + Rules</div>
              <div>Persistence: Phase 8</div>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-800 mt-8 pt-5 flex flex-col sm:flex-row items-center justify-between gap-3">
          <p className="text-[10px] text-slate-700">
            Team OBSIDIAN • INNOV12 • 2026
          </p>

          <div className="flex items-center gap-2 text-[10px] text-slate-600">
            <LockKeyhole className="w-3 h-3 text-emerald-400" />
            Grounded Evidence Architecture
          </div>
        </div>
      </div>
    </footer>
  );
}
