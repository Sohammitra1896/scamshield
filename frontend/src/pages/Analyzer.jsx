import React, { useState } from 'react';
import { 
  Shield, 
  MessageSquare, 
  Link as LinkIcon, 
  Image as ImageIcon, 
  AlertCircle, 
  CheckCircle, 
  Info, 
  Terminal, 
  ArrowRight,
  Clock,
  Sparkles
} from 'lucide-react';

export default function Analyzer({ backendStatus }) {
  const [activeTab, setActiveTab] = useState('message');
  const [inputMessage, setInputMessage] = useState('');
  const [inputUrl, setInputUrl] = useState('');

  return (
    <div className="space-y-8 py-6">
      {/* Page Title & Context */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs mb-1">
            <Shield className="w-3.5 h-3.5" />
            <span>ANALYSIS CONSOLE</span>
          </div>
          <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
            Threat & Scam Detection Workbench
          </h1>
          <p className="text-xs sm:text-sm text-slate-400 mt-1">
            Analyze suspicious messages, phishing links, and chat screenshots with explainable AI evidence.
          </p>
        </div>

        {/* Phase 1 Status Alert */}
        <div className="flex items-center gap-3 px-4 py-2.5 rounded-xl bg-slate-900 border border-cyan-500/30 text-xs">
          <div className="w-2.5 h-2.5 rounded-full bg-cyan-400 animate-pulse"></div>
          <div>
            <span className="font-semibold text-slate-200 block font-mono">PHASE 1 FOUNDATION</span>
            <span className="text-slate-400 text-[11px]">ML models & rules connect in Phase 2 & 3</span>
          </div>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 gap-2">
        <button
          onClick={() => setActiveTab('message')}
          className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-all ${
            activeTab === 'message'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <MessageSquare className="w-4 h-4" />
          Message Analysis
        </button>
        <button
          onClick={() => setActiveTab('url')}
          className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-all ${
            activeTab === 'url'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <LinkIcon className="w-4 h-4" />
          URL Scanner
        </button>
        <button
          onClick={() => setActiveTab('screenshot')}
          className={`flex items-center gap-2 px-5 py-3 text-sm font-medium border-b-2 transition-all ${
            activeTab === 'screenshot'
              ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
              : 'border-transparent text-slate-400 hover:text-slate-200'
          }`}
        >
          <ImageIcon className="w-4 h-4" />
          Screenshot OCR
        </button>
      </div>

      {/* Main Analyzer Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
        {/* Left Column: Input Form (7 cols) */}
        <div className="lg:col-span-7 space-y-6">
          <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/60 space-y-4">
            {activeTab === 'message' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider font-mono">
                    Suspicious Message / Email Text
                  </label>
                  <span className="text-[11px] text-slate-500">
                    Supports SMS, WhatsApp, Telegram, emails
                  </span>
                </div>
                <textarea
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  placeholder="Paste suspicious text here (e.g. 'Congratulations! You have been selected for an internship with ₹35,000 stipend. Deposit ₹1500 refundable security fee...')"
                  rows={7}
                  className="w-full rounded-lg bg-[#0A0F1D] border border-slate-800 p-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 font-sans"
                />
              </div>
            )}

            {activeTab === 'url' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider font-mono">
                    Target URL / Web Address
                  </label>
                  <span className="text-[11px] text-slate-500">
                    Domain structure & brand spoofing
                  </span>
                </div>
                <div className="relative">
                  <LinkIcon className="absolute left-4 top-3.5 w-4 h-4 text-slate-500" />
                  <input
                    type="url"
                    value={inputUrl}
                    onChange={(e) => setInputUrl(e.target.value)}
                    placeholder="https://example-university-portal.xyz/fees/pay"
                    className="w-full rounded-lg bg-[#0A0F1D] border border-slate-800 py-3 pl-11 pr-4 text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-cyan-500 focus:ring-1 focus:ring-cyan-500 font-mono"
                  />
                </div>
              </div>
            )}

            {activeTab === 'screenshot' && (
              <div className="space-y-4">
                <div className="flex items-center justify-between">
                  <label className="text-xs font-semibold text-slate-300 uppercase tracking-wider font-mono">
                    Message Screenshot
                  </label>
                  <span className="text-[11px] text-slate-500">
                    PNG, JPG, WebP supported
                  </span>
                </div>
                <div className="border-2 border-dashed border-slate-800 hover:border-cyan-500/50 rounded-xl p-8 text-center bg-[#0A0F1D] space-y-3 cursor-pointer transition-colors">
                  <div className="w-12 h-12 rounded-full bg-slate-900 border border-slate-800 flex items-center justify-center mx-auto text-cyan-400">
                    <ImageIcon className="w-6 h-6" />
                  </div>
                  <div>
                    <span className="text-sm font-medium text-slate-300">
                      Drag and drop chat screenshot or click to browse
                    </span>
                    <p className="text-xs text-slate-500 mt-1">
                      OCR pipeline extracts message body and parses embedded URLs automatically
                    </p>
                  </div>
                </div>
              </div>
            )}

            {/* Action Bar */}
            <div className="pt-2 flex items-center justify-between border-t border-slate-800/80">
              <div className="flex items-center gap-2 text-xs text-slate-500">
                <Info className="w-3.5 h-3.5 text-cyan-400" />
                <span>Zero fabricated outputs: Real ML pipeline will evaluate inputs</span>
              </div>
              <button
                disabled
                className="px-5 py-2.5 rounded-lg bg-slate-800 text-slate-500 font-semibold text-xs tracking-wider uppercase font-mono cursor-not-allowed flex items-center gap-2"
              >
                <span>Pipeline Locked (Phase 1)</span>
              </button>
            </div>
          </div>

          {/* Development Status Notice */}
          <div className="p-4 rounded-xl border border-amber-500/20 bg-amber-500/5 text-amber-300 text-xs flex items-start gap-3">
            <AlertCircle className="w-4 h-4 text-amber-400 shrink-0 mt-0.5" />
            <div className="space-y-1">
              <span className="font-semibold block text-amber-200">
                Phase 1 Development Mode Notice
              </span>
              <p className="text-amber-300/80 leading-relaxed">
                The frontend shell has been constructed to the final cybersecurity specification. Model weights (TF-IDF + Logistic Regression) and deterministic heuristic rules will be trained and linked during Phase 2 and Phase 3 without any fake hardcoded results.
              </p>
            </div>
          </div>
        </div>

        {/* Right Column: Visual Layout Prototype of Results (5 cols) */}
        <div className="lg:col-span-5 space-y-6">
          <div className="p-6 rounded-xl border border-slate-800 bg-slate-900/60 space-y-6">
            <div className="flex items-center justify-between border-b border-slate-800 pb-4">
              <h3 className="text-sm font-bold text-white font-mono flex items-center gap-2">
                <Terminal className="w-4 h-4 text-cyan-400" />
                EXPLAINABLE REPORT BLUEPRINT
              </h3>
              <span className="text-[10px] font-mono uppercase bg-slate-800 text-slate-400 px-2 py-0.5 rounded">
                Structure Preview
              </span>
            </div>

            {/* Risk Gauge Blueprint */}
            <div className="p-4 rounded-lg bg-[#0A0F1D] border border-slate-800 space-y-3">
              <span className="text-xs font-mono text-slate-400 block">1. DETECTED RISK TIER</span>
              <div className="flex items-center justify-between">
                <div>
                  <span className="text-2xl font-black text-slate-400 font-mono">-- / 100</span>
                  <span className="text-xs text-slate-500 block">Calibrated Risk Score</span>
                </div>
                <div className="px-3 py-1 rounded border border-slate-800 bg-slate-900 text-xs font-mono text-slate-400">
                  AWAITING INFERENCE
                </div>
              </div>
            </div>

            {/* Evidence Indicators Blueprint */}
            <div className="p-4 rounded-lg bg-[#0A0F1D] border border-slate-800 space-y-3">
              <span className="text-xs font-mono text-slate-400 block">2. GROUNDED EVIDENCE INDICATORS</span>
              <p className="text-xs text-slate-500 leading-relaxed">
                Each warning will cite verbatim text snippets and character offsets from the input (e.g. upfront fee demands, off-platform Telegram jump, fake urgency).
              </p>
            </div>

            {/* Algorithmic Drivers Blueprint */}
            <div className="p-4 rounded-lg bg-[#0A0F1D] border border-slate-800 space-y-3">
              <span className="text-xs font-mono text-slate-400 block">3. ALGORITHMIC RISK DRIVERS</span>
              <p className="text-xs text-slate-500 leading-relaxed">
                Exact positive token weights from the calibrated Logistic Regression model will highlight specific scam keywords.
              </p>
            </div>

            {/* Action Steps Blueprint */}
            <div className="p-4 rounded-lg bg-[#0A0F1D] border border-slate-800 space-y-3">
              <span className="text-xs font-mono text-slate-400 block">4. PROTECT GUIDANCE</span>
              <p className="text-xs text-slate-500 leading-relaxed">
                Tailored defensive steps matching the verified threat family.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
