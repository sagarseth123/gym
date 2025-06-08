// frontend/tailwind.config.js
/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{js,jsx,ts,tsx}", // Scan all relevant files in src
  ],
  theme: {
    extend: {
      // We can extend the default theme here later
      // e.g., colors: { 'instagram-blue': '#3897f0', ... }
    },
  },
  plugins: [],
}
