/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./app/views/**/*.html",
    "./app/static/js/**/*.js"
  ],
  theme: {
    extend: {
      colors: {
        primary: { DEFAULT: "#1e3a5f", light: "#2d5282", dark: "#152b47" },
        secondary: { DEFAULT: "#c9a84c", light: "#e2c072", dark: "#a07830" },
        danger: "#dc2626",
        success: "#16a34a",
        warning: "#d97706"
      },
      fontFamily: {
        sans: ["Be Vietnam Pro", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"]
      }
    }
  },
  plugins: [
    require("@tailwindcss/forms"),
    require("@tailwindcss/typography")
  ]
};

