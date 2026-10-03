'use client'

import { useMemo, useState } from 'react'
import { ArrowRight, Eye, EyeOff, LockKeyhole, ShieldCheck } from 'lucide-react'

export function SecurityVisual() {
  return <div className="auth-visual" aria-hidden="true"><div className="auth-grid" /><div className="auth-line line-one" /><div className="auth-line line-two" /><div className="auth-core"><ShieldCheck size={34} /><span>TRUST<br /><b>CORE</b></span></div>{['MESSAGE', 'URL', 'THREAT', 'EVIDENCE', 'RISK'].map((label, index) => <span className={`auth-node auth-node-${index + 1}`} key={label}>{label}</span>)}</div>
}

export function AuthPage({ mode }: { mode: 'login' | 'register' }) {
  const isRegister = mode === 'register'
  const [showPassword, setShowPassword] = useState(false)
  const [name, setName] = useState('')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [confirm, setConfirm] = useState('')
  const strength = useMemo(() => password.length >= 12 ? 'Strong' : password.length >= 8 ? 'Good' : password ? 'Build a stronger password' : 'Use 8+ characters', [password])
  return <main className="auth-page"><section className="auth-visual-pane"><SecurityVisual /><div className="auth-visual-copy"><div className="eyebrow">SCAMSHIELD INTELLIGENCE</div><h1>Detect the signal.<br /><em>Protect the person.</em></h1><p>Explainable threat analysis for every message, URL and digital interaction.</p></div></section><section className="auth-panel"><a href="/" className="auth-brand"><span className="logo-mark"><ShieldCheck size={18} /></span><span>SCAM<span>SHIELD</span><small>by OBSIDIAN</small></span></a><div className="auth-form-wrap"><div className="eyebrow">SECURE ACCESS</div><h2>{isRegister ? 'Create your shield.' : 'Welcome back.'}</h2><p> {isRegister ? 'Start protecting your digital trust.' : 'Continue protecting your digital trust.'}</p><form onSubmit={e => e.preventDefault()}>{isRegister && <label>Full name<input value={name} onChange={e => setName(e.target.value)} placeholder="Your name" autoComplete="name" /></label>}<label>Email<input value={email} onChange={e => setEmail(e.target.value)} placeholder="you@company.com" type="email" autoComplete="email" required /></label><label>Password<div className="password-field"><input value={password} onChange={e => setPassword(e.target.value)} placeholder="Enter your password" type={showPassword ? 'text' : 'password'} autoComplete={isRegister ? 'new-password' : 'current-password'} required /><button type="button" onClick={() => setShowPassword(!showPassword)} aria-label={showPassword ? 'Hide password' : 'Show password'}>{showPassword ? <EyeOff size={16} /> : <Eye size={16} />}</button></div>{isRegister && <span className={`password-strength ${strength === 'Strong' ? 'strong' : ''}`}>{strength}</span>}</label>{isRegister && <label>Confirm password<input value={confirm} onChange={e => setConfirm(e.target.value)} placeholder="Repeat your password" type="password" autoComplete="new-password" /></label>}{!isRegister && <div className="auth-options"><label className="remember"><input type="checkbox" /> Remember me</label><a href="/register">Create an account</a></div>}<button className="button primary auth-submit" type="submit">{isRegister ? 'Create account' : 'Sign in'} <ArrowRight size={16} /></button></form>{isRegister ? <p className="auth-switch">Already have an account? <a href="/login">Sign in</a></p> : <button className="demo-button" type="button"><LockKeyhole size={14} /> Try Demo</button>}</div></section></main>
}
