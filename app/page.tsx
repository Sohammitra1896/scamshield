import ScamShieldApp from '@/components/scamshield'

export default function Page() {
  return <ScamShieldApp />
}

export const dynamic = 'force-dynamic'

export const metadata = {
  title: 'ScamShield — Intelligent Scam Detection',
  description: 'Explainable scam and fraud detection by Team OBSIDIAN.',
}

export const viewport = {
  themeColor: '#080b12',
  colorScheme: 'dark' as const,
}

// v0 Design System Showcase Page
export const runtime = 'nodejs'
