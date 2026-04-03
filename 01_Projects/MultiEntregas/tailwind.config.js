/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx}",
  ],
  theme: {
    extend: {
      colors: {
        navy: {
          900: '#050B14',
          800: '#0A121E',
          700: '#0F1B2D',
          600: '#15243C',
        },
        emerald: {
          DEFAULT: '#00A859',
          glow: 'rgba(0, 168, 89, 0.4)',
          dark: '#008C4A',
          light: '#33B97A',
        },
        'brand-red': {
          DEFAULT: '#E31E24',
          glow: 'rgba(227, 30, 36, 0.4)',
        },
        silver: '#8E9AAF',
        void: '#0B0E14',
      },
      fontFamily: {
        sans: ['Inter', 'Helvetica Neue', 'Arial', 'sans-serif'],
      },
      animation: {
        'fade-up': 'fadeUp 0.6s ease-out forwards',
      },
      keyframes: {
        fadeUp: {
          '0%': { opacity: '0', transform: 'translateY(24px)' },
          '100%': { opacity: '1', transform: 'translateY(0)' },
        },
      },
    },
  },
  plugins: [],
}
