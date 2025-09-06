/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.{html,js}',
    './theme/**/*.{html,js}',
  ],
  theme: {
    extend: {
      colors: {
        darkblue: '#1e1f25',
        brand: {
          DEFAULT: '#1e1f25',
          light: '#2b2c33',
        }
      },
    },
  },
  plugins: [],
}