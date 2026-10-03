import React, { useState } from 'react';
import {
  Link2,
  ScanSearch,
  RotateCcw,
} from 'lucide-react';

import { analyzeURL } from '../../api/client';

const SAMPLE_SCAM =
  'http://internsha1a-stipend.xyz/verify?token=123';

const SAMPLE_LEGIT =
  'https://internshala.com/student/dashboard';

export default function URLScanner({ onResult, onError }) {
  const [url, setUrl] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!url.trim()) {
      onError?.('Please enter a URL to analyze.');
      return;
    }

    setLoading(true);

    try {
      const result = await analyzeURL(url.trim());
      onResult?.(result);
    } catch (error) {
      const detail =
        error?.response?.data?.detail ||
        'URL analysis failed. Check that the backend is running.';

      onError?.(detail);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
            <Link2 className="w-5 h-5 text-cyan-400" />
          </div>

          <div>
            <h2 className="text-base font-bold text-white">
              URL Analysis
            </h2>

            <p className="text-xs text-slate-500 mt-0.5">
              Inspect protocol, domain structure and suspicious indicators
            </p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-4">
        <div className="relative">
          <Link2 className="absolute left-4 top-3.5 w-4 h-4 text-slate-600" />

          <input
            type="text"
            value={url}
            onChange={(event) => setUrl(event.target.value)}
            placeholder="https://example.com/verify"
            className="w-full rounded-xl bg-[#0A0F1D] border border-slate-800 py-3 pl-11 pr-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 font-mono"
          />
        </div>

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setUrl(SAMPLE_SCAM)}
            className="px-3 py-2 rounded-lg border border-rose-500/20 bg-rose-500/5 text-rose-300 text-xs hover:bg-rose-500/10 transition"
          >
            Load suspicious URL
          </button>

          <button
            type="button"
            onClick={() => setUrl(SAMPLE_LEGIT)}
            className="px-3 py-2 rounded-lg border border-emerald-500/20 bg-emerald-500/5 text-emerald-300 text-xs hover:bg-emerald-500/10 transition"
          >
            Load legitimate URL
          </button>

          <button
            type="button"
            onClick={() => {
              setUrl('');
              onError?.('');
            }}
            className="px-3 py-2 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 text-xs hover:text-white transition"
          >
            <RotateCcw className="inline w-3 h-3 mr-1" />
            Clear
          </button>
        </div>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={loading || !url.trim()}
          className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold text-sm hover:bg-cyan-400 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <ScanSearch className="w-4 h-4" />

          {loading ? 'Analyzing...' : 'Analyze URL'}
        </button>
      </div>
    </div>
  );
}
