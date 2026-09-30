import React from 'react';
import { Clock, Database, Shield, Search, Filter, AlertTriangle, CheckCircle, ExternalLink } from 'lucide-react';

export default function History({ backendData }) {
  const dbStatus = backendData?.database || { active_engine: 'sqlite (fallback)', status: 'connected' };

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs mb-1">
            <Clock className="w-3.5 h-3.5" />
            <span>AUDIT TRAIL & PERSISTENCE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Analysis History & Forensics
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Persisted scans, threat category breakdown, and evidence audit trails.
          </p>
        </div>

        {/* Database Engine Status */}
        <div className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-slate-900 border border-slate-800 text-xs">
          <Database className="w-4 h-4 text-cyan-400" />
          <div>
            <span className="font-semibold text-slate-200 block font-mono">
              DATABASE: {dbStatus.active_engine?.toUpperCase() || 'POSTGRESQL'}
            </span>
            <span className="text-slate-400 text-[11px]">
              Status: {dbStatus.status === 'connected' ? 'Connected & Ready' : dbStatus.status}
            </span>
          </div>
        </div>
      </div>

      {/* History Structure Preview */}
      <div className="p-8 rounded-xl border border-slate-800 bg-slate-900/40 text-center space-y-4 max-w-2xl mx-auto">
        <div className="w-12 h-12 rounded-full bg-slate-800 flex items-center justify-center mx-auto text-cyan-400">
          <Clock className="w-6 h-6" />
        </div>
        <div className="space-y-1">
          <h3 className="text-lg font-bold text-white">Relational History Schema Established</h3>
          <p className="text-xs text-slate-400 leading-relaxed max-w-md mx-auto">
            SQLAlchemy data models (<code className="text-cyan-400">ScanRecord</code> and <code className="text-cyan-400">DetectedEvidence</code>) are configured. Live persistence and audit log filtering will be connected in Phase 8 after message and URL analysis engines are completed.
          </p>
        </div>
        <div className="inline-flex items-center gap-2 px-3 py-1 rounded bg-slate-800 text-slate-400 text-xs font-mono">
          <span>Target Database: PostgreSQL 18.6 (with SQLite Fallback)</span>
        </div>
      </div>
    </div>
  );
}
