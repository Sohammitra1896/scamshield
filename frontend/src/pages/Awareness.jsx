import React from 'react';
import { BookOpen, ShieldAlert, Check, AlertOctagon, HelpCircle, ExternalLink } from 'lucide-react';

export default function Awareness() {
  const guideScenarios = [
    {
      category: "Fake Internship & Job Scams",
      warningSign: "Offered a high stipend (e.g. ₹35,000/mo) without an interview or portfolio check; asked to pay a 'refundable laptop courier/registration fee'.",
      action: "Never pay upfront money for an internship. Legitimate companies dispatch equipment or provide stipends directly without deposits.",
      keywords: ["security deposit", "laptop fee", "telegram hr", "offer letter pdf"],
    },
    {
      category: "Task & Part-Time Earnings",
      warningSign: "Invited to Telegram groups to 'like YouTube videos' or 'review hotels' for ₹50–₹100 per task, followed by demanding a 'prepaid merchant recharge'.",
      action: "Stop communication immediately. This is a Ponzi-style task scam. No legitimate brand pays for random video likes.",
      keywords: ["merchant task", "daily 2000-5000", "task code", "telegram admin"],
    },
    {
      category: "Scholarship & Grant Frauds",
      warningSign: "SMS claiming your national/state scholarship is approved, requiring an immediate 'processing fee' via UPI.",
      action: "Government and legitimate scholarship portals (e.g. NSP) never collect approval fees via private UPI IDs or WhatsApp.",
      keywords: ["scholarship approved", "sanction fee", "claim deadline", "upi transfer"],
    },
    {
      category: "Credential Phishing & Typosquatting",
      warningSign: "Links mimicking college portals, banking apps, or courier services (e.g., 'internsha1a.xyz', 'sbi-kyc-update.online').",
      action: "Inspect the exact domain name and TLD before entering credentials. Never click SMS links claiming emergency portal logins.",
      keywords: [".xyz", ".top", "login-verify", "update-kyc"],
    },
    {
      category: "UPI PIN & Payment Fraud",
      warningSign: "Buyer on OLX or stranger claiming to send you money and asking you to enter your UPI PIN or scan a QR code.",
      action: "RULE: UPI PIN is ONLY entered to SEND money, never to RECEIVE money. Scanning a QR code authorizes a debit, not a credit.",
      keywords: ["scan qr to receive", "enter pin to accept", "refund pending"],
    },
    {
      category: "Digital Impersonation & Arrest",
      warningSign: "Caller pretending to be Police/CBI/FedEx claiming your parcel contains illegal items and demanding you remain on video call ('Digital Arrest').",
      action: "Indian law does not recognize 'Digital Arrest'. Real law enforcement agencies never conduct interrogations or demand fund transfers over video calls.",
      keywords: ["digital arrest", "customs seized", "cbi officer", "fedex parcel"],
    },
  ];

  return (
    <div className="space-y-8 py-6">
      {/* Header */}
      <div className="border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs mb-1">
          <BookOpen className="w-3.5 h-3.5" />
          <span>STUDENT THREAT INTELLIGENCE</span>
        </div>
        <h1 className="text-2xl sm:text-3xl font-bold text-white tracking-tight">
          Scam Awareness & Defensive Playbook
        </h1>
        <p className="text-xs sm:text-sm text-slate-400 mt-1">
          Tactical threat breakdowns designed specifically for students, young developers, and campus job seekers.
        </p>
      </div>

      {/* Guide Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        {guideScenarios.map((item, idx) => (
          <div
            key={idx}
            className="p-6 rounded-xl border border-slate-800 bg-slate-900/60 space-y-4 hover:border-slate-700 transition-colors"
          >
            <div className="flex items-start justify-between">
              <h3 className="text-base font-bold text-white flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-cyan-400"></span>
                {item.category}
              </h3>
            </div>

            <div className="space-y-2 text-xs">
              <div className="p-3 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300">
                <span className="font-semibold block text-rose-200 mb-0.5">Warning Signal:</span>
                {item.warningSign}
              </div>

              <div className="p-3 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300">
                <span className="font-semibold block text-emerald-200 mb-0.5">Defensive Action:</span>
                {item.action}
              </div>
            </div>

            <div className="pt-2 border-t border-slate-800 flex items-center gap-2 flex-wrap">
              <span className="text-[11px] font-mono text-slate-500">Typical Indicators:</span>
              {item.keywords.map((kw, kIdx) => (
                <span
                  key={kIdx}
                  className="px-2 py-0.5 rounded bg-slate-800 text-slate-300 text-[10px] font-mono"
                >
                  {kw}
                </span>
              ))}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
