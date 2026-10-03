import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  CheckCircle2,
  Clock3,
  Database,
  Eye,
  RefreshCw,
  Search,
  Shield,
  X,
} from 'lucide-react';

import {
  fetchHistory,
  fetchHistoryRecord,
  fetchStats,
} from '../api/client';


function formatRiskLevel(value) {
  return String(value || 'SAFE')
    .replaceAll('_', ' ');
}


function riskClasses(level) {
  const value = String(level || '').toUpperCase();

  if (value === 'HIGH_RISK') {
    return {
      badge: 'border-rose-500/30 bg-rose-500/10 text-rose-400',
      icon: 'text-rose-400',
    };
  }

  if (value === 'SUSPICIOUS') {
    return {
      badge: 'border-amber-500/30 bg-amber-500/10 text-amber-400',
      icon: 'text-amber-400',
    };
  }

  if (value === 'LOW_RISK') {
    return {
      badge: 'border-yellow-500/30 bg-yellow-500/10 text-yellow-300',
      icon: 'text-yellow-300',
    };
  }

  return {
    badge: 'border-emerald-500/30 bg-emerald-500/10 text-emerald-400',
    icon: 'text-emerald-400',
  };
}


function formatDate(value) {
  if (!value) {
    return 'Unknown time';
  }

  const date = new Date(value);

  if (Number.isNaN(date.getTime())) {
    return value;
  }

  return date.toLocaleString();
}


function StatCard({
  label,
  value,
  icon,
}) {
  const Icon = icon;

  return (
    <div className="rounded-xl border border-slate-800 bg-slate-900/60 p-5">
      <div className="flex items-center justify-between">
        <span className="text-[10px] uppercase tracking-widest font-mono text-slate-600">
          {label}
        </span>

        <Icon className="w-4 h-4 text-cyan-400" />
      </div>

      <div className="text-2xl font-black text-white mt-3 font-mono">
        {value}
      </div>
    </div>
  );
}


export default function History({ backendData }) {
  const [records, setRecords] = useState([]);
  const [stats, setStats] = useState(null);

  const [search, setSearch] = useState('');
  const [riskLevel, setRiskLevel] = useState('');

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  const [selectedRecord, setSelectedRecord] =
    useState(null);

  const dbStatus = backendData?.database;

  const loadHistory = async () => {
    setLoading(true);
    setError('');

    try {
      const [historyData, statsData] =
        await Promise.all([
          fetchHistory({
            search,
            riskLevel,
            skip: 0,
            limit: 50,
          }),
          fetchStats(),
        ]);

      setRecords(historyData.items || []);
      setStats(statsData);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          'Unable to load scan history.',
      );
    } finally {
      setLoading(false);
    }
  };


  useEffect(() => {
    loadHistory();
  }, [search, riskLevel]);


  const openRecord = async (id) => {
    try {
      const record = await fetchHistoryRecord(id);
      setSelectedRecord(record);
    } catch (err) {
      setError(
        err?.response?.data?.detail ||
          'Unable to load scan details.',
      );
    }
  };


  return (
    <div className="space-y-8 py-8">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-5 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs">
            <Clock3 className="w-3.5 h-3.5" />
            AUDIT TRAIL
          </div>

          <h1 className="text-3xl font-bold text-white mt-2">
            Analysis History
          </h1>

          <p className="text-sm text-slate-500 mt-2 max-w-2xl">
            Real persisted message and URL scans with stored
            risk information and evidence.
          </p>
        </div>

        <div className="flex items-center gap-3">
          <div className="px-4 py-2 rounded-xl border border-slate-800 bg-slate-900">
            <div className="text-[9px] uppercase font-mono tracking-widest text-slate-600">
              Database
            </div>

            <div className="text-xs text-cyan-400 font-mono mt-1">
              {dbStatus?.active_engine || 'unknown'}
            </div>
          </div>

          <button
            type="button"
            onClick={loadHistory}
            className="p-2.5 rounded-xl border border-slate-800 bg-slate-900 text-slate-400 hover:text-white transition"
            title="Refresh history"
          >
            <RefreshCw
              className={`w-4 h-4 ${
                loading ? 'animate-spin' : ''
              }`}
            />
          </button>
        </div>
      </div>


      {stats && (
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <StatCard
            label="Total Scans"
            value={stats.total_scans}
            icon={Database}
          />

          <StatCard
            label="Safe"
            value={stats.safe_scans}
            icon={CheckCircle2}
          />

          <StatCard
            label="Suspicious"
            value={
              stats.suspicious_scans +
              stats.high_risk_scans
            }
            icon={AlertTriangle}
          />

          <StatCard
            label="Avg Risk"
            value={stats.average_risk_score}
            icon={Shield}
          />
        </div>
      )}


      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-4">
        <div className="grid grid-cols-1 md:grid-cols-[1fr_auto] gap-3">
          <div className="relative">
            <Search className="absolute left-3.5 top-3 w-4 h-4 text-slate-600" />

            <input
              type="text"
              value={search}
              onChange={(event) =>
                setSearch(event.target.value)
              }
              placeholder="Search scans, categories or input..."
              className="w-full rounded-xl bg-[#0A0F1D] border border-slate-800 py-3 pl-10 pr-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <select
            value={riskLevel}
            onChange={(event) =>
              setRiskLevel(event.target.value)
            }
            className="rounded-xl bg-[#0A0F1D] border border-slate-800 px-4 py-3 text-sm text-slate-300 focus:outline-none focus:border-cyan-500"
          >
            <option value="">All risk levels</option>
            <option value="SAFE">Safe</option>
            <option value="LOW_RISK">Low Risk</option>
            <option value="SUSPICIOUS">
              Suspicious
            </option>
            <option value="HIGH_RISK">High Risk</option>
          </select>
        </div>
      </div>


      {error && (
        <div className="rounded-xl border border-rose-500/20 bg-rose-500/5 p-4 text-sm text-rose-300">
          {error}
        </div>
      )}


      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden">
        <div className="p-5 border-b border-slate-800 flex items-center justify-between">
          <div>
            <h2 className="text-sm font-bold text-white font-mono">
              STORED SCANS
            </h2>

            <p className="text-xs text-slate-600 mt-1">
              {records.length} records displayed
            </p>
          </div>
        </div>


        {loading ? (
          <div className="p-12 text-center text-sm text-slate-500">
            Loading persisted scans...
          </div>
        ) : records.length === 0 ? (
          <div className="p-12 text-center">
            <Clock3 className="w-8 h-8 mx-auto text-slate-700" />

            <h3 className="text-base font-semibold text-white mt-4">
              No matching scans
            </h3>

            <p className="text-xs text-slate-500 mt-2">
              Analyze a message or URL to create the first
              persistent history record.
            </p>
          </div>
        ) : (
          <div className="divide-y divide-slate-800">
            {records.map((record) => {
              const classes =
                riskClasses(record.risk_level);

              return (
                <div
                  key={record.id}
                  className="p-5 hover:bg-slate-950/40 transition"
                >
                  <div className="flex flex-col lg:flex-row lg:items-center gap-4">
                    <div className="flex-1 min-w-0">
                      <div className="flex flex-wrap items-center gap-2">
                        <span className="text-[10px] font-mono uppercase text-cyan-400">
                          {record.scan_type}
                        </span>

                        <span
                          className={`px-2 py-1 rounded-md border text-[10px] font-mono ${classes.badge}`}
                        >
                          {formatRiskLevel(
                            record.risk_level,
                          )}
                        </span>

                        {record.threat_category && (
                          <span className="text-[10px] text-slate-500">
                            {record.threat_category}
                          </span>
                        )}
                      </div>

                      <p className="text-sm text-slate-300 mt-3 truncate">
                        {record.input_preview}
                      </p>

                      <div className="flex flex-wrap gap-4 mt-2 text-[10px] text-slate-600 font-mono">
                        <span>
                          #{record.id}
                        </span>

                        <span>
                          {formatDate(record.created_at)}
                        </span>

                        <span>
                          {record.processing_time_ms != null
                            ? `${record.processing_time_ms.toFixed(2)} ms`
                            : 'n/a'}
                        </span>

                        <span>
                          {record.evidence?.length || 0}{' '}
                          evidence items
                        </span>
                      </div>
                    </div>

                    <div className="flex items-center gap-4">
                      <div className="text-right">
                        <div className="text-[9px] uppercase font-mono text-slate-600">
                          Risk Score
                        </div>

                        <div
                          className={`text-xl font-black font-mono mt-1 ${classes.icon}`}
                        >
                          {Number(
                            record.risk_score,
                          ).toFixed(1)}
                        </div>
                      </div>

                      <button
                        type="button"
                        onClick={() =>
                          openRecord(record.id)
                        }
                        className="p-2.5 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 hover:text-cyan-400 transition"
                        title="View scan details"
                      >
                        <Eye className="w-4 h-4" />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>


      {selectedRecord && (
        <div className="fixed inset-0 z-[100] bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-3xl max-h-[90vh] overflow-y-auto rounded-2xl border border-slate-700 bg-[#0A0F1D] shadow-2xl">
            <div className="sticky top-0 bg-[#0A0F1D] border-b border-slate-800 p-5 flex items-center justify-between">
              <div>
                <h2 className="text-base font-bold text-white">
                  Scan #{selectedRecord.id}
                </h2>

                <p className="text-xs text-slate-600 mt-1">
                  {formatDate(
                    selectedRecord.created_at,
                  )}
                </p>
              </div>

              <button
                type="button"
                onClick={() =>
                  setSelectedRecord(null)
                }
                className="p-2 rounded-lg border border-slate-800 text-slate-500 hover:text-white"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="p-5 space-y-5">
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-3">
                  <div className="text-[9px] uppercase font-mono text-slate-600">
                    Type
                  </div>

                  <div className="text-sm text-cyan-400 mt-1">
                    {selectedRecord.scan_type}
                  </div>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-3">
                  <div className="text-[9px] uppercase font-mono text-slate-600">
                    Risk
                  </div>

                  <div className="text-sm text-white mt-1">
                    {formatRiskLevel(
                      selectedRecord.risk_level,
                    )}
                  </div>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-3">
                  <div className="text-[9px] uppercase font-mono text-slate-600">
                    Score
                  </div>

                  <div className="text-sm text-white mt-1 font-mono">
                    {Number(
                      selectedRecord.risk_score,
                    ).toFixed(2)}
                  </div>
                </div>

                <div className="rounded-xl border border-slate-800 bg-slate-900/50 p-3">
                  <div className="text-[9px] uppercase font-mono text-slate-600">
                    Category
                  </div>

                  <div className="text-xs text-cyan-400 mt-1">
                    {selectedRecord.threat_category ||
                      'None'}
                  </div>
                </div>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-4">
                <div className="text-[9px] uppercase font-mono tracking-widest text-slate-600">
                  Input Preview
                </div>

                <p className="text-sm text-slate-300 mt-2 leading-relaxed break-words">
                  {selectedRecord.input_preview}
                </p>
              </div>

              <div>
                <h3 className="text-xs font-bold text-white font-mono mb-3">
                  STORED EVIDENCE
                </h3>

                {selectedRecord.evidence?.length ? (
                  <div className="space-y-3">
                    {selectedRecord.evidence.map(
                      (item) => (
                        <div
                          key={item.id}
                          className="rounded-xl border border-slate-800 bg-slate-900/50 p-4"
                        >
                          <div className="flex flex-wrap items-center gap-2">
                            <span className="text-xs font-semibold text-cyan-400">
                              {item.signal_name}
                            </span>

                            <span className="text-[9px] font-mono text-slate-600 uppercase">
                              {item.evidence_type}
                            </span>

                            {item.severity && (
                              <span className="text-[9px] text-rose-400 uppercase">
                                {item.severity}
                              </span>
                            )}
                          </div>

                          {item.verbatim_quote && (
                            <blockquote className="text-xs text-slate-300 font-mono mt-2">
                              "{item.verbatim_quote}"
                            </blockquote>
                          )}

                          {item.feature_weight != null && (
                            <div className="text-[10px] text-slate-500 font-mono mt-2">
                              contribution:{' '}
                              {Number(
                                item.feature_weight,
                              ).toFixed(6)}
                            </div>
                          )}

                          {item.character_offset_start != null &&
                            item.character_offset_end != null && (
                              <div className="text-[10px] text-slate-600 font-mono mt-1">
                                offsets{' '}
                                {item.character_offset_start}
                                –
                                {item.character_offset_end}
                              </div>
                            )}
                        </div>
                      ),
                    )}
                  </div>
                ) : (
                  <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-5 text-center text-xs text-slate-600">
                    No stored evidence items.
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
