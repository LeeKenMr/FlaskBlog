/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/*.html"],  //npx tailwindcss -i ./tailwind.css -o ./static/main.css
  // content: ["./vue/src/**/*.{css,js,vue}"], //npx tailwindcss -i ./tailwind.css -o ./vue/public/static/admin.css
  theme: {
    extend: {},
  },
  plugins: [
    require('@tailwindcss/forms'),
  ],
}

