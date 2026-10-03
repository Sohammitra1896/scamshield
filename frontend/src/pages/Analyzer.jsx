import React, { useState } from 'react';
import {
  AlertCircle,
  CheckCircle2,
  FileSearch,
  Info,
  Link2,
  MessageSquare,
  Shield,
  Sparkles,
  Terminal,
  XCircle,
} from 'lucide-react';

import MessageScanner from '../components/analysis/MessageScanner';
import URLScanner from '../components/analysis/URLScanner';
import ScreenshotScanner from '../components/analysis/ScreenshotScanner';

import RiskGauge from '../components/common/RiskGauge';
import IndicatorList from '../components/common/IndicatorList';
import TopFeaturesChart from '../components/common/TopFeaturesChart';
import ActionSteps from '../components/common/ActionSteps';

function ResultHeader({ result }) {
  const isScam = result.prediction === 'scam';
  const probability =
    result?.model_estimated_probabilities?.scam ?? 0;

  const category = result?.category?.category;

  return (
    <div className="rounded-2xl border border-slate-800 bg-slate-900/60 overflow-hidden">
      <div className="p-6 border-b border-slate-800">
        <div className="flex items-center justify-between gap-4">
          <div className="flex items-center gap-3">
            <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
              <Terminal className="w-5 h-5 text-cyan-400" />
            </div>

            <div>
              <h2 className="text-base font-bold text-white">
                Explainable Analysis Report
              </h2>

              <p className="text-xs text-slate-500 mt-0.5">
                Real result from the ScamShield analysis API
              </p>
            </div>
          </div>

          {isScam ? (
            <XCircle className="w-5 h-5 text-rose-400" />
          ) : (
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
          )}
        </div>
      </div>

      <div className="p-6">
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8 items-center">
          <RiskGauge
            score={result?.risk?.risk_score}
            riskLevel={result?.risk?.risk_level}
          />

          <div className="space-y-4">
            <div>
              <div className="text-[10px] font-mono uppercase tracking-widest text-slate-600">
                Prediction
              </div>

              <div
                className={`text-3xl font-black mt-1 uppercase ${
                  isScam
                    ? 'text-rose-400'
                    : 'text-emerald-400'
                }`}
              >
                {result.prediction}
              </div>
            </div>

            <div className="grid grid-cols-2 gap-3">
              <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-4">
                <div className="text-[10px] text-slate-600 uppercase font-mono">
                  Model scam probability
                </div>

                <div className="text-xl font-bold text-white font-mono mt-1">
                  {(probability * 100).toFixed(2)}%
                </div>
              </div>

              <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-4">
                <div className="text-[10px] text-slate-600 uppercase font-mono">
                  Category
                </div>

                <div className="text-sm font-semibold text-cyan-400 mt-2">
                  {category || 'No category assigned'}
                </div>
              </div>
            </div>

            <div className="rounded-xl border border-slate-800 bg-slate-950/50 p-4">
              <div className="text-[10px] text-slate-600 uppercase font-mono">
                Score construction
              </div>

              <div className="text-xs text-slate-400 mt-2 leading-relaxed">
                Base score: {Number(result?.risk?.base_score || 0).toFixed(2)}
                {' '}• Rule bonus: {Number(result?.risk?.rule_bonus || 0).toFixed(2)}
                {' '}• Final application score: {Number(result?.risk?.risk_score || 0).toFixed(2)}
              </div>

              <div className="text-[10px] text-slate-600 mt-2">
                The application risk score is separate from the model-estimated probability.
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

function ResultSections({ result }) {
  const isScam = result.prediction === 'scam';

  return (
    <div className="space-y-6">
      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
        <div className="flex items-center gap-2 mb-4">
          <FileSearch className="w-4 h-4 text-cyan-400" />

          <h3 className="text-sm font-bold text-white font-mono">
            01 — DETECT
          </h3>
        </div>

        <IndicatorList indicators={result.indicators} />
      </div>

      <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6">
        <div className="flex items-center gap-2 mb-4">
          <Sparkles className="w-4 h-4 text-cyan-400" />

          <h3 className="text-sm font-bold text-white font-mono">
            02 — EXPLAIN
          </h3>
        </div>

        <p className="text-xs text-slate-500 mb-4">
          {isScam
            ? 'Positive model contributions associated with the scam prediction.'
            : 'Model contributions associated with the legitimate prediction.'}
        </p>

        <TopFeaturesChart
          prediction={result.prediction}
          riskDrivers={result.ml_risk_drivers}
          legitimacyDrivers={result.ml_legitimacy_drivers}
        />
      </div>

      <ActionSteps
        recommendations={result.recommendations}
      />
    </div>
  );
}

function ErrorBox({ message }) {
  if (!message) {
    return null;
  }

  return (
    <div className="rounded-xl border border-rose-500/20 bg-rose-500/5 p-4 flex gap-3">
      <AlertCircle className="w-4 h-4 text-rose-400 shrink-0 mt-0.5" />

      <div>
        <p className="text-sm font-semibold text-rose-300">
          Analysis request failed
        </p>

        <p className="text-xs text-rose-300/70 mt-1 leading-relaxed">
          {message}
        </p>
      </div>
    </div>
  );
}

export default function Analyzer({ backendStatus }) {
  const [activeTab, setActiveTab] = useState('message');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');

  const handleResult = (data) => {
    setResult(data);
    setError('');
  };

  const tabs = [
    {
      id: 'message',
      label: 'Message',
      icon: MessageSquare,
    },
    {
      id: 'url',
      label: 'URL',
      icon: Link2,
    },
    {
      id: 'screenshot',
      label: 'Screenshot',
      icon: Shield,
    },
  ];

  return (
    <div className="space-y-8 py-8">
      <div className="flex flex-col lg:flex-row lg:items-end justify-between gap-5 border-b border-slate-800 pb-6">
        <div>
          <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs mb-2">
            <Shield className="w-3.5 h-3.5" />
            ANALYSIS CONSOLE
          </div>

          <h1 className="text-3xl font-bold text-white tracking-tight">
            Threat Detection Workbench
          </h1>

          <p className="text-sm text-slate-400 mt-2 max-w-2xl">
            Submit a suspicious message or URL and inspect the real
            model probability, deterministic evidence, risk score,
            model drivers and defensive recommendations.
          </p>
        </div>

        <div className="flex items-center gap-2 px-3 py-2 rounded-xl border border-slate-800 bg-slate-900 text-xs">
          <span
            className={`w-2 h-2 rounded-full ${
              backendStatus === 'healthy'
                ? 'bg-emerald-400 animate-pulse'
                : backendStatus === 'connecting'
                  ? 'bg-amber-400 animate-pulse'
                  : 'bg-rose-400'
            }`}
          />

          <span className="font-mono text-slate-400">
            API:{' '}
            {backendStatus === 'healthy'
              ? 'CONNECTED'
              : backendStatus.toUpperCase()}
          </span>
        </div>
      </div>

      <div className="flex flex-wrap border-b border-slate-800 gap-1">
        {tabs.map((tab) => {
          const Icon = tab.icon;
          const active = activeTab === tab.id;

          return (
            <button
              key={tab.id}
              type="button"
              onClick={() => {
                setActiveTab(tab.id);
                setError('');
              }}
              className={`flex items-center gap-2 px-5 py-3 text-sm font-semibold border-b-2 transition ${
                active
                  ? 'border-cyan-400 text-cyan-400 bg-cyan-500/5'
                  : 'border-transparent text-slate-500 hover:text-slate-200'
              }`}
            >
              <Icon className="w-4 h-4" />
              {tab.label}
            </button>
          );
        })}
      </div>

      <div className="grid grid-cols-1 xl:grid-cols-12 gap-8">
        <div className="xl:col-span-5 space-y-5">
          {activeTab === 'message' && (
            <MessageScanner
              onResult={handleResult}
              onError={setError}
            />
          )}

          {activeTab === 'url' && (
            <URLScanner
              onResult={handleResult}
              onError={setError}
            />
          )}

          {activeTab === 'screenshot' && (
            <ScreenshotScanner
              onResult={handleResult}
              onError={setError}
            />
          )}

          <div className="rounded-xl border border-cyan-500/10 bg-cyan-500/5 p-4 flex gap-3">
            <Info className="w-4 h-4 text-cyan-400 mt-0.5 shrink-0" />

            <div>
              <p className="text-xs font-semibold text-cyan-200">
                DETECT → EXPLAIN → PROTECT
              </p>

              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Results are populated from the backend analysis pipeline.
                The frontend does not generate or invent model findings.
              </p>
            </div>
          </div>

          <ErrorBox message={error} />
        </div>

        <div className="xl:col-span-7">
          {!result ? (
            <div className="h-full min-h-[520px] rounded-2xl border border-slate-800 bg-slate-900/40 flex items-center justify-center p-8">
              <div className="max-w-sm text-center">
                <div className="w-16 h-16 mx-auto rounded-2xl bg-slate-900 border border-slate-800 flex items-center justify-center">
                  <Sparkles className="w-7 h-7 text-cyan-400" />
                </div>

                <h2 className="text-lg font-bold text-white mt-5">
                  Awaiting analysis
                </h2>

                <p className="text-sm text-slate-500 mt-2 leading-relaxed">
                  Submit a message or URL to populate the explainable
                  report with live backend results.
                </p>
              </div>
            </div>
          ) : (
            <div className="space-y-6">
              <ResultHeader result={result} />
              <ResultSections result={result} />
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
