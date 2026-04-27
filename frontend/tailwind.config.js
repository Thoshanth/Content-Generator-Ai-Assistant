/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#1D6CF2',
          dark: '#0F4DC9',
          light: '#E8F0FE',
          accent: '#4A90F5',
        },
        surface: {
          DEFAULT: '#F7F9FC',
          dark: '#0D1117',
        },
        text: {
          primary: '#1A1A2E',
          secondary: '#5F6B7A',
        },
        border: '#E2E8F0',
      },
      fontFamily: {
        sans: ['-apple-system', 'BlinkMacSystemFont', '"SF Pro Display"', '"SF Pro Text"', 'sans-serif'],
      },
    },
  },
  plugins: [],
}
