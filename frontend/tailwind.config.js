/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        cyber: {
          bg: "#0A0F1D",
          surface: "#0F172A",
          card: "#1E293B",
          cardHover: "#283548",
          border: "#334155",
          accent: "#06B6D4",
          accentHover: "#0891B2",
          cyanGlow: "rgba(6, 182, 212, 0.15)",
          textPrimary: "#F8FAFC",
          textSecondary: "#94A3B8",
          textMuted: "#64748B",
        },
        risk: {
          safe: "#10B981",
          safeBg: "rgba(16, 185, 129, 0.1)",
          warning: "#F59E0B",
          warningBg: "rgba(245, 158, 11, 0.1)",
          danger: "#F43F5E",
          dangerBg: "rgba(244, 63, 94, 0.1)",
        }
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [],
}
