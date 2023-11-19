/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./templates/**/*.html",
    "./static/src/**/"],
  theme: {
    extend: {
      colors: {
        primary: '#21A4D8',
        darkPrimary: '#0D313D',
      },
      fontSize: {
        '2xl': '1.5rem',
        '3xl': '1.875rem',
        '4xl': '2.25rem',
      },
    },
  },
  plugins: [],
}

