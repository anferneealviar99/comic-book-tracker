/** @type {import('tailwindcss').Config} */
module.exports = {
  future: {
    removeDeprecatedGapUtilities: true,
    purgeLayersByDefault: true,
  },
  darkMode: 'media',
  content: [
      '../comics/templates/**/*.html',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

