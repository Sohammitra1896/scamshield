import React from 'react';
import { Shield, Cpu, Activity, Clock, BookOpen } from 'lucide-react';

export default function Navbar({ activePage, setActivePage, backendStatus }) {
  const navItems = [
    { id: 'home', label: 'Overview', icon: Activity },
    { id: 'analyzer', label: 'Threat Analyzer', icon: Shield },
    { id: 'history', label: 'Scan Audit Log', icon: Clock },
    { id: 'awareness', label: 'Threat Intelligence', icon: BookOpen },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-[#0A0F1D]/80 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo & Platform Info */}
          <div className="flex items-center gap-3 cursor-pointer" onClick={() => setActivePage('home')}>
            <div className="relative flex items-center justify-center w-10 h-10 rounded-lg bg-gradient-to-br from-cyan-500/20 to-blue-600/20 border border-cyan-500/30 text-cyan-400 shadow-sm shadow-cyan-500/10">
              <Shield className="w-5 h-5 text-cyan-400" />
              <span className="absolute -top-1 -right-1 flex h-2.5 w-2.5">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-cyan-400 opacity-75"></span>
                <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-cyan-500"></span>
              </span>
            </div>
            <div>
              <div className="flex items-center gap-2">
                <span className="text-lg font-bold tracking-tight text-white">ScamShield</span>
                <span className="px-1.5 py-0.5 text-[10px] font-semibold tracking-wide uppercase rounded bg-cyan-500/10 text-cyan-400 border border-cyan-500/30">
                  INNOV12
                </span>
              </div>
              <div className="text-[11px] font-medium text-slate-400 tracking-wide flex items-center gap-1.5">
                <span>Team OBSIDIAN</span>
                <span>•</span>
                <span className="text-slate-500">Detect → Explain → Protect</span>
              </div>
            </div>
          </div>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive = activePage === item.id;
              return (
                <button
                  key={item.id}
                  onClick={() => setActivePage(item.id)}
                  className={`flex items-center gap-2 px-3.5 py-2 rounded-lg text-sm font-medium transition-all duration-150 ${
                    isActive
                      ? 'bg-cyan-500/15 text-cyan-400 border border-cyan-500/30 shadow-sm shadow-cyan-500/10'
                      : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Backend Status Badge */}
          <div className="flex items-center gap-3">
            <div className="hidden sm:flex items-center gap-2 px-2.5 py-1 rounded-full bg-slate-900 border border-slate-800 text-xs">
              <span
                className={`w-2 h-2 rounded-full ${
                  backendStatus === 'healthy'
                    ? 'bg-emerald-400 animate-pulse'
                    : backendStatus === 'connecting'
                    ? 'bg-amber-400 animate-ping'
                    : 'bg-rose-500'
                }`}
              />
              <span className="text-slate-400 font-mono text-[11px]">
                API: {backendStatus === 'healthy' ? 'CONNECTED' : backendStatus.toUpperCase()}
              </span>
            </div>
          </div>
        </div>
      </div>
      {/* Mobile nav bar */}
      <div className="md:hidden flex items-center justify-around border-t border-slate-800/80 px-2 py-2 bg-slate-950/90">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = activePage === item.id;
          return (
            <button
              key={item.id}
              onClick={() => setActivePage(item.id)}
              className={`flex flex-col items-center gap-1 px-3 py-1 rounded text-xs font-medium ${
                isActive ? 'text-cyan-400' : 'text-slate-400'
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.label.split(' ')[0]}</span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
