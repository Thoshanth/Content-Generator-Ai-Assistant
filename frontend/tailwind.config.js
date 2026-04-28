/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        bg:           '#000000',
        surface:      '#0A0A0A',
        'surface-raised': '#141414',
        border:       '#222222',
        peach:        '#F9A8A8',
        'peach-hover':'#E59595',
        'peach-subtle':'#4A2020',
        'text-primary': '#FFFFFF',
        'text-secondary': '#A0A0A0',
        'text-muted': '#555555',
        success:      '#4CAF50',
        error:        '#FF5252',
      },
      fontFamily: {
        heading: ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
        body:    ['-apple-system', 'BlinkMacSystemFont', '"Segoe UI"', 'Roboto', 'Helvetica', 'Arial', 'sans-serif'],
        code:    ['JetBrains Mono', 'monospace'],
      },
    },
  },
  plugins: [],
}
