import React, { useState } from 'react';
import {
  MessageSquare,
  ScanSearch,
  RotateCcw,
} from 'lucide-react';

import { analyzeMessage } from '../../api/client';

const SAMPLE_SCAM =
  'Congratulations! You have been selected for a remote internship. Pay Rs. 1999 registration fee immediately to confirm your position.';

const SAMPLE_LEGIT =
  'Reminder: Database Systems lecture slides and assignment 3 are available on Classroom. Submit before Tuesday.';

export default function MessageScanner({ onResult, onError }) {
  const [message, setMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!message.trim()) {
      onError?.('Please enter a message to analyze.');
      return;
    }

    setLoading(true);

    try {
      const result = await analyzeMessage(message.trim());
      onResult?.(result);
    } catch (error) {
      const detail =
        error?.response?.data?.detail ||
        'Message analysis failed. Check that the backend is running.';

      onError?.(detail);
    } finally {
      setLoading(false);
    }
  };

  const clearInput = () => {
    setMessage('');
    onError?.('');
  };

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
            <MessageSquare className="w-5 h-5 text-cyan-400" />
          </div>

          <div>
            <h2 className="text-base font-bold text-white">
              Message Analysis
            </h2>

            <p className="text-xs text-slate-500 mt-0.5">
              Analyze SMS, WhatsApp, Telegram, email and other text
            </p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-4">
        <textarea
          value={message}
          onChange={(event) => setMessage(event.target.value)}
          rows={9}
          placeholder="Paste a suspicious message here..."
          className="w-full rounded-xl bg-[#0A0F1D] border border-slate-800 p-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 resize-y"
        />

        <div className="flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => setMessage(SAMPLE_SCAM)}
            className="px-3 py-2 rounded-lg border border-rose-500/20 bg-rose-500/5 text-rose-300 text-xs hover:bg-rose-500/10 transition"
          >
            Load scam example
          </button>

          <button
            type="button"
            onClick={() => setMessage(SAMPLE_LEGIT)}
            className="px-3 py-2 rounded-lg border border-emerald-500/20 bg-emerald-500/5 text-emerald-300 text-xs hover:bg-emerald-500/10 transition"
          >
            Load legitimate example
          </button>

          <button
            type="button"
            onClick={clearInput}
            className="px-3 py-2 rounded-lg border border-slate-800 bg-slate-950 text-slate-400 text-xs hover:text-white transition"
          >
            <RotateCcw className="inline w-3 h-3 mr-1" />
            Clear
          </button>
        </div>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={loading || !message.trim()}
          className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold text-sm hover:bg-cyan-400 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <ScanSearch className="w-4 h-4" />

          {loading ? 'Analyzing...' : 'Analyze Message'}
        </button>
      </div>
    </div>
  );
}
