/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html",
    "./static/src/**/"],
  theme: {
    extend: {
      colors: {
        primary: '#21A4D8',
        darkPrimary: '#030F27',
      },
      fontSize: {
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
      },
      scale: {
        '108': '1.08',
      }
    },
  },
  plugins: [],
}

