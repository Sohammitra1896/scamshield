export type ScanType = 'message' | 'url' | 'screenshot'

export type ScanResult = {
  scan_id?: string
  prediction?: string
  risk_level?: string
  risk_score?: number
  scam_probability?: number
  model_scam_probability?: number
  threat_category?: string

  evidence?: Array<{
    label?: string
    text?: string
    severity?: string
    description?: string
  }>

  positive_drivers?: string[]
  negative_drivers?: string[]
  recommended_actions?: string[]

  url_analysis?: Array<{
    label?: string
    value?: string
    status?: string
  }>

  processing_time_ms?: number
  created_at?: string
  input_preview?: string
  type?: ScanType

  [key: string]: unknown
}

const API_BASE =
  process.env.NEXT_PUBLIC_API_BASE_URL ||
  'http://127.0.0.1:8000'

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  try {
    const isFormData = options.body instanceof FormData

    const response = await fetch(
      `${API_BASE}${path}`,
      {
        ...options,
        headers: {
          ...(isFormData
            ? {}
            : {
                'Content-Type': 'application/json',
              }),
          ...(options.headers ?? {}),
        },
      }
    )

    const text = await response.text()

    let data: unknown = null

    try {
      data = text ? JSON.parse(text) : null
    } catch {
      data = text
    }

    if (!response.ok) {
      let message =
        `Request failed with status ${response.status}`

      if (
        typeof data === 'object' &&
        data !== null &&
        'detail' in data
      ) {
        const detail =
          (data as { detail?: unknown }).detail

        if (typeof detail === 'string') {
          message = detail
        }
      }

      throw new Error(message)
    }

    return data as T

  } catch (error) {
    if (error instanceof TypeError) {
      throw new Error(
        'ScamShield API is unavailable. Make sure the FastAPI backend is running.'
      )
    }

    throw error
  }
}

function normalizeHistory(
  data: unknown
): ScanResult[] {
  if (Array.isArray(data)) {
    return data as ScanResult[]
  }

  if (
    data &&
    typeof data === 'object'
  ) {
    const obj =
      data as Record<string, unknown>

    const possibleKeys = [
      'items',
      'history',
      'scans',
      'results',
      'data',
    ]

    for (const key of possibleKeys) {
      if (Array.isArray(obj[key])) {
        return obj[key] as ScanResult[]
      }
    }
  }

  return []
}

export const api = {
  health: () =>
    request<{ status: string }>(
      '/api/v1/health'
    ),

  analyzeMessage: (message: string) =>
    request<ScanResult>(
      '/api/v1/analyze/message',
      {
        method: 'POST',
        body: JSON.stringify({
          message,
        }),
      }
    ),

  analyzeUrl: (url: string) =>
    request<ScanResult>(
      '/api/v1/analyze/url',
      {
        method: 'POST',
        body: JSON.stringify({
          url,
        }),
      }
    ),

  analyzeScreenshot: (file: File) => {
    const body = new FormData()

    body.append('file', file)

    return request<ScanResult>(
      '/api/v1/analyze/screenshot',
      {
        method: 'POST',
        body,
      }
    )
  },

  history: async (): Promise<ScanResult[]> => {
    const data = await request<unknown>(
      '/api/v1/history'
    )

    return normalizeHistory(data)
  },

  detail: (scanId: string) =>
    request<ScanResult>(
      `/api/v1/history/${encodeURIComponent(scanId)}`
    ),

  deleteHistory: (scanId: string | number) =>
    request<{
      success: boolean
      scan_id: number
    }>(
      `/api/v1/history/${encodeURIComponent(String(scanId))}`,
      {
        method: 'DELETE',
      }
    ),

  clearHistory: () =>
    request<{
      success: boolean
      deleted_count: number
    }>(
      '/api/v1/history',
      {
        method: 'DELETE',
      }
    ),

  stats: () =>
    request<Record<string, unknown>>(
      '/api/v1/stats'
    ),
}

type AnyResult =
  | ScanResult
  | null
  | undefined

export const resultValue = (
  result: AnyResult,
  key: keyof ScanResult,
  fallback = '—'
) => {
  const value = result?.[key]

  return value === undefined ||
    value === null ||
    value === ''
    ? fallback
    : String(value)
}

export const resultScore = (
  result: AnyResult
) =>
  Number(
    result?.risk_score ??
      result?.scam_probability ??
      result?.model_scam_probability ??
      0
  )

export const riskTone = (
  level?: string
) => {
  const value =
    (level ?? '').toLowerCase()

  if (
    value.includes('high') ||
    value.includes('critical')
  ) {
    return 'high'
  }

  if (
    value.includes('suspicious') ||
    value.includes('medium')
  ) {
    return 'medium'
  }

  if (value.includes('low')) {
    return 'low'
  }

  return 'safe'
}
