/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    "./src/**/*.{html,js}",
    "./templates/**/*.{html,js}",
    "./node_modules/flowbite/**/*.js",
    "./src/**/form.py",
  ],
  theme: {
    extend: {},
  },
  plugins: [
      require('flowbite/plugin')
  ]
}


