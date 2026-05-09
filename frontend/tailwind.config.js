/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ['./app/**/*.{js,jsx,ts,tsx}', './components/**/*.{js,jsx,ts,tsx}'],
  presets: [require('nativewind/preset')],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#FEF3E7',
          100: '#F9E4C8',
          500: '#D4A574',
          600: '#B8935F',
          900: '#6B5334',
        },
        neutral: {
          50: '#F5F3F0',
          100: '#E8E5E0',
          200: '#D1CCC4',
          300: '#9B9388',
          500: '#6B6358',
          700: '#3D3832',
          800: '#252118',
          900: '#0F0D0A',
        },
        success: {
          500: '#7C9885',
          600: '#5A7A65',
        },
        warning: {
          500: '#C9A961',
          600: '#A88B4F',
        },
        error: {
          500: '#A05A52',
          600: '#8B4A43',
        },
      },
    },
  },
  plugins: [],
};
