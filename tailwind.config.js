/** @type {import('tailwindcss').Config} */
module.exports = {
  mode: 'jit', // Habilita el modo JIT
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


