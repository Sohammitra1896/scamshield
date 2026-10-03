import React from 'react';
import {
  Activity,
  ArrowRight,
  CheckCircle2,
  Cpu,
  Eye,
  FileSearch,
  LockKeyhole,
  Search,
  Shield,
  Terminal,
} from 'lucide-react';

export default function Home({ onNavigate, backendData }) {
  const threatCategories = [
    {
      title: 'Fake Internship',
      desc: 'Unrealistic offers combined with registration fees, deposits or other upfront payments.',
    },
    {
      title: 'Task & Recruitment',
      desc: 'Task-based earning schemes and suspicious recruitment requests.',
    },
    {
      title: 'Scholarship Fraud',
      desc: 'Fake approvals, processing fees and payment requests.',
    },
    {
      title: 'Phishing',
      desc: 'Lookalike domains and suspicious credential or login requests.',
    },
    {
      title: 'Payment & UPI Fraud',
      desc: 'Payment manipulation, PIN requests and transaction scams.',
    },
    {
      title: 'Impersonation',
      desc: 'Messages pretending to come from officials, organisations or trusted entities.',
    },
    {
      title: 'Institutional Clones',
      desc: 'Fake university notices, emergency fee messages and portal links.',
    },
    {
      title: 'KYC & Account Scams',
      desc: 'Threats involving account suspension, KYC updates or urgent verification.',
    },
  ];

  const connected = backendData?.status === 'healthy';

  return (
    <div className="space-y-16 py-8">
      <section className="relative overflow-hidden rounded-3xl border border-slate-800 bg-gradient-to-b from-slate-900/90 via-[#0D1527] to-[#0A0F1D] p-8 md:p-12">
        <div className="absolute right-0 top-0 w-96 h-96 rounded-full bg-cyan-500/10 blur-3xl pointer-events-none" />

        <div className="relative max-w-4xl">
          <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-cyan-500/10 border border-cyan-500/20 text-cyan-400 text-[11px] font-mono">
            <Shield className="w-3.5 h-3.5" />
            INNOV12 • CYBER & DIGITAL TRUST
          </div>

          <h1 className="text-4xl md:text-6xl font-black text-white leading-tight mt-6">
            Scam detection that
            <span className="block text-cyan-400">
              shows its evidence.
            </span>
          </h1>

          <p className="text-base md:text-lg text-slate-400 max-w-3xl mt-6 leading-relaxed">
            ScamShield combines a lightweight machine-learning pipeline,
            deterministic security rules and grounded explanations to
            help students inspect suspicious digital messages and links.
          </p>

          <div className="flex flex-wrap gap-3 mt-8">
            <button
              type="button"
              onClick={() => onNavigate('analyzer')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-xl bg-cyan-500 text-slate-950 font-bold text-sm hover:bg-cyan-400 transition"
            >
              <Search className="w-4 h-4" />
              Open Threat Analyzer
              <ArrowRight className="w-4 h-4" />
            </button>

            <button
              type="button"
              onClick={() => onNavigate('awareness')}
              className="inline-flex items-center gap-2 px-5 py-3 rounded-xl border border-slate-700 bg-slate-900 text-slate-200 font-semibold text-sm hover:bg-slate-800 transition"
            >
              <FileSearch className="w-4 h-4" />
              Threat Intelligence
            </button>
          </div>
        </div>

        <div className="relative mt-12 pt-8 border-t border-slate-800 grid grid-cols-1 md:grid-cols-3 gap-6">
          <div className="flex gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 h-fit">
              <Eye className="w-5 h-5" />
            </div>

            <div>
              <h3 className="text-sm font-bold text-white font-mono">
                DETECT
              </h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Message and URL analysis using the trained ScamShield models.
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 h-fit">
              <Terminal className="w-5 h-5" />
            </div>

            <div>
              <h3 className="text-sm font-bold text-white font-mono">
                EXPLAIN
              </h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Exact rule evidence and model feature contributions.
              </p>
            </div>
          </div>

          <div className="flex gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 h-fit">
              <LockKeyhole className="w-5 h-5" />
            </div>

            <div>
              <h3 className="text-sm font-bold text-white font-mono">
                PROTECT
              </h3>
              <p className="text-xs text-slate-500 mt-1 leading-relaxed">
                Defensive recommendations based on detected evidence.
              </p>
            </div>
          </div>
        </div>
      </section>

      <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="flex items-center justify-between">
            <span className="text-[10px] uppercase tracking-widest font-mono text-slate-600">
              API Status
            </span>

            <Activity
              className={`w-4 h-4 ${
                connected
                  ? 'text-emerald-400'
                  : 'text-amber-400'
              }`}
            />
          </div>

          <div className="text-lg font-bold text-white mt-3">
            {connected ? 'Connected' : 'Waiting for backend'}
          </div>

          <p className="text-xs text-slate-500 mt-1">
            FastAPI analysis service
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="text-[10px] uppercase tracking-widest font-mono text-slate-600">
            Architecture
          </div>

          <div className="text-lg font-bold text-white mt-3">
            Explainable ML
          </div>

          <p className="text-xs text-slate-500 mt-1">
            ML probability + deterministic rules
          </p>
        </div>

        <div className="rounded-2xl border border-slate-800 bg-slate-900/60 p-5">
          <div className="text-[10px] uppercase tracking-widest font-mono text-slate-600">
            Current Build
          </div>

          <div className="text-lg font-bold text-cyan-400 mt-3">
            Phase 7
          </div>

          <p className="text-xs text-slate-500 mt-1">
            Live cybersecurity frontend
          </p>
        </div>
      </section>

      <section>
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-3 mb-6">
          <div>
            <h2 className="text-2xl font-bold text-white">
              Student Threat Families
            </h2>

            <p className="text-sm text-slate-500 mt-1">
              ScamShield's targeted analysis and awareness categories.
            </p>
          </div>

          <span className="text-[11px] font-mono text-cyan-400 border border-cyan-500/20 bg-cyan-500/5 px-3 py-1.5 rounded-lg">
            8 CORE FAMILIES
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {threatCategories.map((item, index) => (
            <div
              key={item.title}
              className="rounded-xl border border-slate-800 bg-slate-900/50 p-5 hover:border-slate-700 transition"
            >
              <div className="flex items-center justify-between">
                <span className="text-[10px] font-mono text-cyan-400">
                  0{index + 1}
                </span>

                <CheckCircle2 className="w-4 h-4 text-slate-700" />
              </div>

              <h3 className="text-sm font-bold text-white mt-4">
                {item.title}
              </h3>

              <p className="text-xs text-slate-500 mt-2 leading-relaxed">
                {item.desc}
              </p>
            </div>
          ))}
        </div>
      </section>

      <section className="rounded-2xl border border-slate-800 bg-[#0E1526] p-7">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
            <Cpu className="w-5 h-5 text-cyan-400" />
          </div>

          <div>
            <h2 className="text-lg font-bold text-white">
              Engineering Integrity
            </h2>

            <p className="text-xs text-slate-500">
              Built around reproducible analysis rather than decorative output.
            </p>
          </div>
        </div>

        <div className="grid md:grid-cols-3 gap-4 mt-6">
          {[
            'Real trained model artifacts',
            'Grounded deterministic evidence',
            'No fabricated scan results',
          ].map((item) => (
            <div
              key={item}
              className="rounded-xl border border-slate-800 bg-slate-950/40 p-4"
            >
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />

              <p className="text-sm font-semibold text-slate-200 mt-3">
                {item}
              </p>
            </div>
          ))}
        </div>
      </section>
    </div>
  );
}
