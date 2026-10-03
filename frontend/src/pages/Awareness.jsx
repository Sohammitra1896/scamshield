import React from 'react';
import {
  AlertTriangle,
  BookOpen,
  CheckCircle2,
  ShieldAlert,
} from 'lucide-react';

const scenarios = [
  {
    title: 'Fake Internship Offers',
    warning:
      'Unexpected internship offers paired with registration fees, deposits or equipment charges.',
    action:
      'Verify the organisation through its independently accessed official recruitment channel before paying or sharing information.',
    indicators: [
      'registration fee',
      'security deposit',
      'remote internship',
      'Telegram HR',
    ],
  },
  {
    title: 'Task & Recruitment Scams',
    warning:
      'Easy-money tasks followed by requests for deposits, recharges or account payments.',
    action:
      'Do not continue a payment chain merely because an earlier task produced a small reward.',
    indicators: [
      'task code',
      'merchant recharge',
      'daily earnings',
      'prepaid task',
    ],
  },
  {
    title: 'Scholarship Fraud',
    warning:
      'Messages claiming guaranteed scholarship approval and requesting urgent payment.',
    action:
      'Verify scholarship status through the official portal or institution rather than a message link.',
    indicators: [
      'processing fee',
      'scholarship approved',
      'claim deadline',
      'UPI payment',
    ],
  },
  {
    title: 'Credential Phishing',
    warning:
      'Lookalike domains, unusual URLs and requests to sign in or verify credentials.',
    action:
      'Inspect the exact domain and independently navigate to the official website.',
    indicators: [
      '.xyz',
      'verify login',
      'account update',
      'KYC',
    ],
  },
  {
    title: 'UPI & Payment Fraud',
    warning:
      'Requests involving UPI PINs, QR codes or payment actions framed as receiving money.',
    action:
      'Do not enter a UPI PIN to receive money and verify unexpected payment requests.',
    indicators: [
      'UPI PIN',
      'scan QR',
      'refund',
      'receive money',
    ],
  },
  {
    title: 'Impersonation',
    warning:
      'Messages or calls claiming to represent trusted officials, institutions or agencies.',
    action:
      'End the interaction and independently verify the identity using a trusted contact channel.',
    indicators: [
      'urgent call',
      'official notice',
      'police',
      'account officer',
    ],
  },
  {
    title: 'Fake Institutional Notices',
    warning:
      'Emergency notices about examinations, fees or account access arriving through unusual channels.',
    action:
      'Cross-check with the institution website, portal or known administrative contact.',
    indicators: [
      'urgent notice',
      'fee deadline',
      'exam cancelled',
      'verify now',
    ],
  },
  {
    title: 'KYC & Account Scams',
    warning:
      'Threats of immediate suspension combined with links or requests for sensitive information.',
    action:
      'Do not use the supplied link. Open the official service independently and verify the account state.',
    indicators: [
      'KYC update',
      'account suspended',
      'verify immediately',
      'SIM blocked',
    ],
  },
];

export default function Awareness() {
  return (
    <div className="space-y-8 py-8">
      <div className="border-b border-slate-800 pb-6">
        <div className="flex items-center gap-2 text-cyan-400 font-mono text-xs">
          <BookOpen className="w-3.5 h-3.5" />
          STUDENT THREAT INTELLIGENCE
        </div>

        <h1 className="text-3xl font-bold text-white mt-2">
          Scam Awareness
        </h1>

        <p className="text-sm text-slate-500 mt-2 max-w-2xl">
          Practical warning signals and defensive actions for common
          student-facing digital scams.
        </p>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {scenarios.map((item) => (
          <article
            key={item.title}
            className="rounded-2xl border border-slate-800 bg-slate-900/60 p-6"
          >
            <div className="flex items-start gap-3">
              <div className="p-2 rounded-lg bg-cyan-500/10 border border-cyan-500/20">
                <ShieldAlert className="w-5 h-5 text-cyan-400" />
              </div>

              <div>
                <h2 className="text-base font-bold text-white">
                  {item.title}
                </h2>

                <p className="text-xs text-slate-500 mt-1">
                  Common warning pattern
                </p>
              </div>
            </div>

            <div className="mt-5 rounded-xl border border-rose-500/20 bg-rose-500/5 p-4">
              <div className="flex gap-2">
                <AlertTriangle className="w-4 h-4 text-rose-400 mt-0.5" />

                <div>
                  <p className="text-[10px] font-mono uppercase tracking-widest text-rose-400">
                    Warning signal
                  </p>

                  <p className="text-xs text-rose-200/80 mt-1 leading-relaxed">
                    {item.warning}
                  </p>
                </div>
              </div>
            </div>

            <div className="mt-3 rounded-xl border border-emerald-500/20 bg-emerald-500/5 p-4">
              <div className="flex gap-2">
                <CheckCircle2 className="w-4 h-4 text-emerald-400 mt-0.5" />

                <div>
                  <p className="text-[10px] font-mono uppercase tracking-widest text-emerald-400">
                    Defensive action
                  </p>

                  <p className="text-xs text-emerald-200/80 mt-1 leading-relaxed">
                    {item.action}
                  </p>
                </div>
              </div>
            </div>

            <div className="flex flex-wrap gap-2 mt-4 pt-4 border-t border-slate-800">
              {item.indicators.map((indicator) => (
                <span
                  key={indicator}
                  className="px-2 py-1 rounded-md bg-slate-950 border border-slate-800 text-[10px] text-slate-400 font-mono"
                >
                  {indicator}
                </span>
              ))}
            </div>
          </article>
        ))}
      </div>
    </div>
  );
}
