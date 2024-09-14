/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  darkMode: 'media',
  content: [
      '../templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

