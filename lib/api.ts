export type ScanType = 'message' | 'url' | 'screenshot'

export type ScanResult = {
  scan_id?: string
  prediction?: string
  risk_level?: string
  risk_score?: number
  scam_probability?: number
  model_scam_probability?: number
  threat_category?: string
  evidence?: Array<{ label?: string; text?: string; severity?: string; description?: string }>
  positive_drivers?: string[]
  negative_drivers?: string[]
  recommended_actions?: string[]
  url_analysis?: Array<{ label?: string; value?: string; status?: string }>
  processing_time_ms?: number
  created_at?: string
  input_preview?: string
  type?: ScanType
  [key: string]: unknown
}

const API_BASE = process.env.NEXT_PUBLIC_API_BASE_URL ?? process.env.VITE_API_BASE_URL ?? ''

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  try {
    const response = await fetch(`${API_BASE}${path}`, {
      ...options,
      headers: { 'Content-Type': 'application/json', ...(options?.headers ?? {}) },
    })
    if (!response.ok) {
      throw new Error(response.status >= 500 ? 'ScamShield API is unavailable. Check the backend connection.' : 'Unable to analyze this input. Please try again.')
    }
    return response.json()
  } catch (error) {
    if (error instanceof TypeError) throw new Error('ScamShield API is unavailable. Check the backend connection.')
    throw error
  }
}

export const api = {
  health: () => request<{ status: string }>('/api/v1/health'),
  analyzeMessage: (message: string) => request<ScanResult>('/api/v1/message/analyze', { method: 'POST', body: JSON.stringify({ message }) }),
  analyzeUrl: (url: string) => request<ScanResult>('/api/v1/url/analyze', { method: 'POST', body: JSON.stringify({ url }) }),
  analyzeScreenshot: (file: File) => { const body = new FormData(); body.append('file', file); return fetch(`${API_BASE}/api/v1/screenshot/analyze`, { method: 'POST', body }).then(async (r) => { if (!r.ok) throw new Error(`Request failed with status ${r.status}`); return r.json() as Promise<ScanResult> }) },
  history: () => request<ScanResult[]>('/api/v1/history'),
  detail: (scanId: string) => request<ScanResult>(`/api/v1/history/${encodeURIComponent(scanId)}`),
  stats: () => request<Record<string, unknown>>('/api/v1/stats'),
}

type AnyResult = ScanResult | null | undefined
export const resultValue = (result: AnyResult, key: keyof ScanResult, fallback = '—') => {
  const value = result?.[key]
  return value === undefined || value === null || value === '' ? fallback : String(value)
}

export const resultScore = (result: AnyResult) => Number(result?.risk_score ?? result?.scam_probability ?? result?.model_scam_probability ?? 0)

export const riskTone = (level?: string) => {
  const value = (level ?? '').toLowerCase()
  if (value.includes('high') || value.includes('critical')) return 'high'
  if (value.includes('suspicious') || value.includes('medium')) return 'medium'
  if (value.includes('low')) return 'low'
  return 'safe'
}
