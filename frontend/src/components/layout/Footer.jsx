import React from 'react';
import { Shield, Lock, Terminal, Cpu } from 'lucide-react';

export default function Footer() {
  return (
    <footer className="border-t border-slate-800 bg-[#0A0F1D] text-slate-400 py-10 mt-auto">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8 mb-8">
          {/* Col 1: Platform */}
          <div className="space-y-3 md:col-span-1">
            <div className="flex items-center gap-2">
              <Shield className="w-5 h-5 text-cyan-400" />
              <span className="text-base font-bold text-white tracking-tight">ScamShield</span>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Explainable AI-powered digital safety platform designed to protect students and young digital users against sophisticated online fraud.
            </p>
            <div className="flex items-center gap-1.5 text-xs text-cyan-400/90 font-mono">
              <Terminal className="w-3.5 h-3.5" />
              <span>DETECT → EXPLAIN → PROTECT</span>
            </div>
          </div>

          {/* Col 2: Team Obsidian */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-slate-200 tracking-wider uppercase font-mono">
              Team OBSIDIAN
            </h4>
            <ul className="text-xs space-y-1.5 text-slate-400">
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                <span className="text-slate-300 font-medium">Soham Mitra</span>
                <span className="text-slate-500">— CSE, 3rd Yr</span>
              </li>
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                <span className="text-slate-300 font-medium">Khyati K Doshi</span>
                <span className="text-slate-500">— CSE (IOTCSBT), 3rd Yr</span>
              </li>
              <li className="flex items-center gap-1.5">
                <span className="w-1.5 h-1.5 rounded-full bg-cyan-400"></span>
                <span className="text-slate-300 font-medium">Srinistha Biswas</span>
                <span className="text-slate-500">— CSE (IOTCSBT), 3rd Yr</span>
              </li>
            </ul>
          </div>

          {/* Col 3: Tracks & Competition */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-slate-200 tracking-wider uppercase font-mono">
              INNOV12 Competition
            </h4>
            <div className="space-y-1.5 text-xs">
              <div>
                <span className="text-slate-500 block">Primary Track:</span>
                <span className="text-slate-300 font-medium">Cyber & Digital Trust</span>
              </div>
              <div>
                <span className="text-slate-500 block">Supporting Track:</span>
                <span className="text-slate-300 font-medium">AI & GenAI</span>
              </div>
            </div>
          </div>

          {/* Col 4: Architecture Status */}
          <div className="space-y-2">
            <h4 className="text-xs font-semibold text-slate-200 tracking-wider uppercase font-mono">
              System Architecture
            </h4>
            <div className="space-y-1.5 text-xs">
              <div className="flex items-center justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">Current Phase:</span>
                <span className="text-cyan-400 font-mono font-medium">Phase 1 Foundation</span>
              </div>
              <div className="flex items-center justify-between py-1 border-b border-slate-800">
                <span className="text-slate-400">ML Backend:</span>
                <span className="text-slate-300 font-mono">FastAPI + Python 3.12</span>
              </div>
              <div className="flex items-center justify-between py-1">
                <span className="text-slate-400">Database:</span>
                <span className="text-slate-300 font-mono">PostgreSQL (SQLite Fallback)</span>
              </div>
            </div>
          </div>
        </div>

        <div className="border-t border-slate-800/80 pt-6 flex flex-col sm:flex-row items-center justify-between text-xs text-slate-500">
          <p>© 2026 Team OBSIDIAN — INNOV12 Competition. Developed as a real, explainable cybersecurity working prototype.</p>
          <div className="flex items-center gap-4 mt-2 sm:mt-0">
            <span className="flex items-center gap-1">
              <Lock className="w-3.5 h-3.5 text-emerald-400" />
              <span>Grounded Evidence Architecture</span>
            </span>
          </div>
        </div>
      </div>
    </footer>
  );
}
