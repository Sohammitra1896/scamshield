import React from 'react';
import {
  Activity,
  BookOpen,
  Clock3,
  Shield,
} from 'lucide-react';

export default function Navbar({
  activePage,
  setActivePage,
  backendStatus,
}) {
  const navItems = [
    {
      id: 'home',
      label: 'Overview',
      icon: Activity,
    },
    {
      id: 'analyzer',
      label: 'Threat Analyzer',
      icon: Shield,
    },
    {
      id: 'history',
      label: 'Scan History',
      icon: Clock3,
    },
    {
      id: 'awareness',
      label: 'Awareness',
      icon: BookOpen,
    },
  ];

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800 bg-[#0A0F1D]/90 backdrop-blur-xl">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="h-16 flex items-center justify-between gap-4">

          {/* Logo */}
          <button
            type="button"
            onClick={() => setActivePage('home')}
            className="flex items-center gap-3 min-w-0"
          >
            <div className="w-10 h-10 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center shrink-0">
              <Shield className="w-5 h-5 text-cyan-400" />
            </div>

            <div className="text-left min-w-0">
              <div className="flex items-center gap-2">
                <span className="text-lg font-black text-white">
                  ScamShield
                </span>

                <span className="px-1.5 py-0.5 rounded bg-cyan-500/10 border border-cyan-500/20 text-[9px] text-cyan-400 font-mono">
                  INNOV12
                </span>
              </div>

              <div className="text-[10px] text-slate-600 font-mono hidden sm:block">
                TEAM OBSIDIAN • DETECT → EXPLAIN → PROTECT
              </div>
            </div>
          </button>

          {/* Desktop Navigation */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const active = activePage === item.id;

              return (
                <button
                  key={item.id}
                  type="button"
                  onClick={() => setActivePage(item.id)}
                  className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-semibold transition ${
                    active
                      ? 'text-cyan-400 bg-cyan-500/10 border border-cyan-500/20'
                      : 'text-slate-500 hover:text-slate-200 hover:bg-slate-900'
                  }`}
                >
                  <Icon className="w-4 h-4" />
                  {item.label}
                </button>
              );
            })}
          </nav>

          {/* Backend Status */}
          <div className="hidden sm:flex items-center gap-2 px-3 py-1.5 rounded-full border border-slate-800 bg-slate-900">
            <span
              className={`w-2 h-2 rounded-full ${
                backendStatus === 'healthy'
                  ? 'bg-emerald-400 animate-pulse'
                  : backendStatus === 'connecting'
                    ? 'bg-amber-400 animate-pulse'
                    : 'bg-rose-400'
              }`}
            />

            <span className="text-[10px] font-mono text-slate-500">
              {backendStatus === 'healthy'
                ? 'API CONNECTED'
                : backendStatus.toUpperCase()}
            </span>
          </div>
        </div>
      </div>

      {/* Mobile Navigation */}
      <div className="md:hidden border-t border-slate-800 px-2 py-2 flex justify-around bg-slate-950/90">
        {navItems.map((item) => {
          const Icon = item.icon;
          const active = activePage === item.id;

          return (
            <button
              key={item.id}
              type="button"
              onClick={() => setActivePage(item.id)}
              className={`flex flex-col items-center gap-1 px-3 py-1 ${
                active
                  ? 'text-cyan-400'
                  : 'text-slate-600'
              }`}
            >
              <Icon className="w-4 h-4" />

              <span className="text-[9px] font-medium">
                {item.label.split(' ')[0]}
              </span>
            </button>
          );
        })}
      </div>
    </header>
  );
}
