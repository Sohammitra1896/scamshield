import React, { useState } from 'react';
import {
  Image,
  Upload,
  ScanSearch,
  AlertCircle,
  FileImage,
} from 'lucide-react';

import { analyzeScreenshot } from '../../api/client';

export default function ScreenshotScanner({ onResult, onError }) {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!file) {
      onError?.('Please select an image first.');
      return;
    }

    setLoading(true);

    try {
      const result = await analyzeScreenshot(file);
      onResult?.(result);
    } catch (error) {
      const detail =
        error?.response?.data?.detail ||
        'Screenshot analysis is currently unavailable.';

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
            <Image className="w-5 h-5 text-cyan-400" />
          </div>

          <div>
            <h2 className="text-base font-bold text-white">
              Screenshot Analysis
            </h2>

            <p className="text-xs text-slate-500 mt-0.5">
              Upload a chat screenshot for OCR-based analysis
            </p>
          </div>
        </div>
      </div>

      <div className="p-6 space-y-5">
        <label className="block cursor-pointer">
          <input
            type="file"
            accept="image/png,image/jpeg,image/webp"
            className="hidden"
            onChange={(event) => {
              const selected = event.target.files?.[0] || null;
              setFile(selected);
              onError?.('');
            }}
          />

          <div className="rounded-2xl border-2 border-dashed border-slate-800 hover:border-cyan-500/40 bg-[#0A0F1D] p-10 text-center transition">
            <div className="w-14 h-14 mx-auto rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center">
              {file ? (
                <FileImage className="w-7 h-7 text-cyan-400" />
              ) : (
                <Upload className="w-7 h-7 text-slate-500" />
              )}
            </div>

            <h3 className="text-sm font-semibold text-slate-200 mt-4">
              {file ? file.name : 'Select a screenshot'}
            </h3>

            <p className="text-xs text-slate-500 mt-1">
              PNG, JPG or WebP
            </p>
          </div>
        </label>

        <div className="rounded-xl border border-amber-500/20 bg-amber-500/5 p-4 flex gap-3">
          <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />

          <div>
            <p className="text-xs font-semibold text-amber-200">
              OCR pipeline status
            </p>

            <p className="text-xs text-amber-300/70 mt-1 leading-relaxed">
              Screenshot OCR is scheduled for Phase 9. This frontend
              is wired to the real endpoint but will not fabricate an
              analysis while OCR is unavailable.
            </p>
          </div>
        </div>

        <button
          type="button"
          onClick={handleAnalyze}
          disabled={loading || !file}
          className="w-full flex items-center justify-center gap-2 px-5 py-3 rounded-xl bg-slate-800 text-slate-300 font-bold text-sm hover:bg-slate-700 disabled:opacity-40 disabled:cursor-not-allowed transition"
        >
          <ScanSearch className="w-4 h-4" />

          {loading ? 'Uploading...' : 'Analyze Screenshot'}
        </button>
      </div>
    </div>
  );
}
