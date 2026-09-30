import React from 'react';
import { 
  Shield, 
  Search, 
  Link as LinkIcon, 
  Image as ImageIcon, 
  CheckCircle, 
  AlertTriangle, 
  Terminal, 
  ArrowRight, 
  Cpu, 
  Lock, 
  Eye, 
  FileText 
} from 'lucide-react';

export default function Home({ onNavigate, backendData }) {
  const threatCategories = [
    { title: "Fake Internship Offers", desc: "Unrealistic stipends, no interview, laptop security deposits." },
    { title: "Task & Part-Time Scams", desc: "Telegram/WhatsApp task scams paying ₹50 to like YouTube videos." },
    { title: "Scholarship & Grant Fraud", desc: "Phony registration fees for guaranteed government scholarships." },
    { title: "Credential Harvesters & Phishing", desc: "Typosquatted university fee portals and lookalike domains." },
    { title: "UPI PIN & Payment Fraud", desc: "Overpayment tricks, refund fraud, and UPI collect requests." },
    { title: "Digital Impersonation", desc: "Impersonation of college officials, bank admins, or courier delivery." },
    { title: "Institutional Notice Clones", desc: "Fake exam postponements and emergency fee circulars." },
    { title: "KYC & Account Suspension", desc: "Threats of SIM blocking or power disconnection within hours." },
  ];

  return (
    <div className="space-y-16 py-8">
      {/* Hero Section */}
      <section className="relative overflow-hidden rounded-2xl border border-slate-800 bg-gradient-to-b from-slate-900/80 via-[#0D1527] to-[#0A0F1D] p-8 md:p-12 shadow-2xl">
        <div className="absolute top-0 right-0 w-96 h-96 bg-cyan-500/10 rounded-full blur-3xl -z-10 pointer-events-none"></div>
        <div className="max-w-3xl space-y-6">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-500/10 border border-cyan-500/30 text-cyan-400 text-xs font-mono font-medium">
            <Shield className="w-3.5 h-3.5" />
            <span>INNOV12 COMPETITION ENTRY • TRACK: CYBER & DIGITAL TRUST</span>
          </div>

          <h1 className="text-3xl sm:text-5xl font-extrabold tracking-tight text-white leading-tight">
            Explainable AI Protection <br />
            <span className="text-transparent bg-clip-text bg-gradient-to-r from-cyan-400 to-blue-500">
              Against Student Scams
            </span>
          </h1>

          <p className="text-base sm:text-lg text-slate-300 leading-relaxed">
            ScamShield safeguards students and young digital users by dissecting suspicious text messages, malicious URLs, and chat screenshots. We deliver verifiable risk assessments backed by mathematical token attributions and grounded heuristic evidence.
          </p>

          <div className="flex flex-wrap items-center gap-4 pt-2">
            <button
              onClick={() => onNavigate('analyzer')}
              className="inline-flex items-center gap-2 px-6 py-3 rounded-lg bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-sm transition-all duration-200 shadow-lg shadow-cyan-500/20"
            >
              <Search className="w-4 h-4" />
              Open Threat Analyzer
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={() => onNavigate('awareness')}
              className="inline-flex items-center gap-2 px-5 py-3 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 font-medium text-sm border border-slate-700 transition-all duration-200"
            >
              <FileText className="w-4 h-4" />
              Threat Intelligence Hub
            </button>
          </div>
        </div>

        {/* Core Principles Ribbon */}
        <div className="mt-12 pt-8 border-t border-slate-800/80 grid grid-cols-1 sm:grid-cols-3 gap-6">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Eye className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white font-mono">1. DETECT</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Calibrated TF-IDF + Logistic Regression coupled with lexical URL analyzers.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Terminal className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white font-mono">2. EXPLAIN</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Verbatim matched rule quotes and linear model coefficient weights. Zero fabrication.
              </p>
            </div>
          </div>

          <div className="flex items-start gap-3">
            <div className="p-2 rounded-lg bg-cyan-500/10 text-cyan-400 border border-cyan-500/20">
              <Lock className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-semibold text-white font-mono">3. PROTECT</h3>
              <p className="text-xs text-slate-400 mt-0.5">
                Immediate, actionable defensive protocols tailored to the verified threat category.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Target Scam Scenarios */}
      <section className="space-y-6">
        <div className="flex flex-col sm:flex-row sm:items-end justify-between gap-4">
          <div>
            <h2 className="text-xl sm:text-2xl font-bold text-white tracking-tight">
              Targeted Student Threat Scenarios
            </h2>
            <p className="text-xs sm:text-sm text-slate-400 mt-1">
              Common cyber fraud tactics engineered specifically to exploit students and campus communities.
            </p>
          </div>
          <span className="text-xs font-mono text-cyan-400 bg-cyan-500/10 px-3 py-1 rounded border border-cyan-500/20 w-fit">
            8 Specialized Threat Families
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
          {threatCategories.map((item, idx) => (
            <div
              key={idx}
              className="p-5 rounded-xl border border-slate-800 bg-slate-900/60 hover:bg-slate-900 hover:border-slate-700 transition-all duration-200 space-y-2 group"
            >
              <div className="flex items-center justify-between">
                <span className="text-xs font-mono text-cyan-400/80">0{idx + 1}</span>
                <AlertTriangle className="w-4 h-4 text-slate-600 group-hover:text-amber-400 transition-colors" />
              </div>
              <h4 className="text-sm font-semibold text-slate-100">{item.title}</h4>
              <p className="text-xs text-slate-400 leading-relaxed">{item.desc}</p>
            </div>
          ))}
        </div>
      </section>

      {/* Architecture & Engineering Integrity Card */}
      <section className="p-8 rounded-xl border border-slate-800 bg-[#0E1526] space-y-6">
        <div className="flex items-center gap-3">
          <div className="p-2.5 rounded-lg bg-cyan-500/10 border border-cyan-500/30 text-cyan-400">
            <Cpu className="w-5 h-5" />
          </div>
          <div>
            <h3 className="text-lg font-bold text-white">Competition Prototype Architecture</h3>
            <p className="text-xs text-slate-400">Team OBSIDIAN engineering standards for INNOV12</p>
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 text-xs text-slate-300">
          <div className="space-y-2 p-4 rounded-lg bg-slate-900/80 border border-slate-800/80">
            <h5 className="font-semibold text-white font-mono flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-cyan-400" />
              Explainable ML Pipeline
            </h5>
            <p className="text-slate-400 leading-relaxed">
              Logistic Regression with TF-IDF provides exact coefficient-based attribution for text, combined with structural URL lexical feature extraction.
            </p>
          </div>

          <div className="space-y-2 p-4 rounded-lg bg-slate-900/80 border border-slate-800/80">
            <h5 className="font-semibold text-white font-mono flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-cyan-400" />
              Deterministic Rule Safety Floor
            </h5>
            <p className="text-slate-400 leading-relaxed">
              High-risk patterns (urgent fee demands, UPI PIN requests) trigger verifiable quotes with token offsets, preventing model evasion.
            </p>
          </div>

          <div className="space-y-2 p-4 rounded-lg bg-slate-900/80 border border-slate-800/80">
            <h5 className="font-semibold text-white font-mono flex items-center gap-1.5">
              <CheckCircle className="w-3.5 h-3.5 text-cyan-400" />
              Reliable Relational Storage
            </h5>
            <p className="text-slate-400 leading-relaxed">
              PostgreSQL primary persistence with automatic SQLite fallback for zero-friction local development and demonstrations.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
}
