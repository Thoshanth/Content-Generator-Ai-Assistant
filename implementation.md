const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  HeadingLevel, AlignmentType, BorderStyle, WidthType, ShadingType,
  LevelFormat, PageNumber, Header, Footer, TabStopType, TabStopPosition
} = require('docx');
const fs = require('fs');

const PEACH = "FFBE9D";
const PEACH_DARK = "E8A07A";
const BLACK = "0D0D0D";
const WHITE = "FFFFFF";
const GRAY = "A0A0A0";
const DARK_SURFACE = "1A1A1A";
const ACCENT = "FFBE9D";

const border = { style: BorderStyle.SINGLE, size: 1, color: "333333" };
const borders = { top: border, bottom: border, left: border, right: border };
const noBorder = { style: BorderStyle.NONE, size: 0, color: "FFFFFF" };
const noBorders = { top: noBorder, bottom: noBorder, left: noBorder, right: noBorder };

function h1(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_1,
    spacing: { before: 400, after: 160 },
    children: [new TextRun({ text, font: "Georgia", size: 36, bold: true, color: PEACH })]
  });
}

function h2(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_2,
    spacing: { before: 320, after: 120 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: PEACH, space: 4 } },
    children: [new TextRun({ text, font: "Georgia", size: 26, bold: true, color: WHITE })]
  });
}

function h3(text) {
  return new Paragraph({
    heading: HeadingLevel.HEADING_3,
    spacing: { before: 240, after: 80 },
    children: [new TextRun({ text, font: "Montserrat", size: 22, bold: true, color: PEACH })]
  });
}

function body(text, color = "CCCCCC") {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    children: [new TextRun({ text, font: "Montserrat", size: 20, color })]
  });
}

function note(text) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    indent: { left: 360 },
    children: [
      new TextRun({ text: "💡 ", size: 20 }),
      new TextRun({ text, font: "Montserrat", size: 20, color: PEACH, italics: true })
    ]
  });
}

function warn(text) {
  return new Paragraph({
    spacing: { before: 80, after: 80 },
    indent: { left: 360 },
    children: [
      new TextRun({ text: "⚠️  ", size: 20 }),
      new TextRun({ text, font: "Montserrat", size: 20, color: "FF9966", bold: true })
    ]
  });
}

function bullet(text, sub = false) {
  return new Paragraph({
    numbering: { reference: "bullets", level: sub ? 1 : 0 },
    spacing: { before: 40, after: 40 },
    children: [new TextRun({ text, font: "Montserrat", size: 20, color: "CCCCCC" })]
  });
}

function divider() {
  return new Paragraph({
    spacing: { before: 240, after: 240 },
    border: { bottom: { style: BorderStyle.SINGLE, size: 2, color: "333333", space: 1 } },
    children: []
  });
}

function space(n = 1) {
  return new Paragraph({ spacing: { before: 60 * n, after: 60 * n }, children: [] });
}

function colorRow(cells, bg = DARK_SURFACE) {
  return new TableRow({
    children: cells.map((c, i) => new TableCell({
      borders,
      width: { size: Math.floor(9360 / cells.length), type: WidthType.DXA },
      shading: { fill: bg, type: ShadingType.CLEAR },
      margins: { top: 80, bottom: 80, left: 160, right: 160 },
      children: [new Paragraph({
        children: [new TextRun({ text: c.text || c, font: "Montserrat", size: 18,
          bold: c.bold || false, color: c.color || "CCCCCC" })]
      })]
    }))
  });
}

function makeTable(headers, rows) {
  const colW = Math.floor(9360 / headers.length);
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: headers.map(() => colW),
    rows: [
      new TableRow({
        tableHeader: true,
        children: headers.map(h => new TableCell({
          borders,
          width: { size: colW, type: WidthType.DXA },
          shading: { fill: "2A1A0D", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 160, right: 160 },
          children: [new Paragraph({
            children: [new TextRun({ text: h, font: "Montserrat", size: 18, bold: true, color: PEACH })]
          })]
        }))
      }),
      ...rows.map((row, ri) => new TableRow({
        children: row.map(cell => new TableCell({
          borders,
          width: { size: colW, type: WidthType.DXA },
          shading: { fill: ri % 2 === 0 ? "1A1A1A" : "0D0D0D", type: ShadingType.CLEAR },
          margins: { top: 80, bottom: 80, left: 160, right: 160 },
          children: [new Paragraph({
            children: [new TextRun({ text: cell, font: "Montserrat", size: 18, color: "CCCCCC" })]
          })]
        }))
      }))
    ]
  });
}

function codeBlock(lines) {
  return new Table({
    width: { size: 9360, type: WidthType.DXA },
    columnWidths: [9360],
    rows: [
      new TableRow({
        children: [new TableCell({
          borders: { top: border, bottom: border, left: { style: BorderStyle.SINGLE, size: 12, color: PEACH }, right: border },
          width: { size: 9360, type: WidthType.DXA },
          shading: { fill: "111111", type: ShadingType.CLEAR },
          margins: { top: 120, bottom: 120, left: 240, right: 240 },
          children: lines.map(l => new Paragraph({
            spacing: { before: 20, after: 20 },
            children: [new TextRun({ text: l, font: "Courier New", size: 18, color: "E8E8E8" })]
          }))
        })]
      })
    ]
  });
}

// ─────────────────────────────────────────────
// DOCUMENT CONTENT
// ─────────────────────────────────────────────

const doc = new Document({
  numbering: {
    config: [
      {
        reference: "bullets",
        levels: [
          { level: 0, format: LevelFormat.BULLET, text: "▸", alignment: AlignmentType.LEFT,
            style: { run: { color: PEACH, font: "Montserrat" }, paragraph: { indent: { left: 480, hanging: 240 } } } },
          { level: 1, format: LevelFormat.BULLET, text: "–", alignment: AlignmentType.LEFT,
            style: { run: { color: GRAY, font: "Montserrat" }, paragraph: { indent: { left: 960, hanging: 240 } } } }
        ]
      }
    ]
  },
  styles: {
    default: {
      document: { run: { font: "Montserrat", size: 20, color: "CCCCCC" } }
    },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 36, bold: true, font: "Georgia", color: PEACH },
        paragraph: { spacing: { before: 400, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: "Georgia", color: WHITE },
        paragraph: { spacing: { before: 320, after: 120 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 22, bold: true, font: "Montserrat", color: PEACH },
        paragraph: { spacing: { before: 240, after: 80 }, outlineLevel: 2 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [
          new Paragraph({
            border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: PEACH, space: 4 } },
            children: [
              new TextRun({ text: "AI Content Generator — ", font: "Georgia", size: 18, color: PEACH, bold: true }),
              new TextRun({ text: "Frontend Design & Implementation Specification", font: "Montserrat", size: 18, color: GRAY })
            ]
          })
        ]
      })
    },
    footers: {
      default: new Footer({
        children: [
          new Paragraph({
            border: { top: { style: BorderStyle.SINGLE, size: 2, color: "333333", space: 4 } },
            alignment: AlignmentType.CENTER,
            children: [
              new TextRun({ text: "Version 2.0 — Peach & Black Theme  |  Page ", font: "Montserrat", size: 16, color: GRAY }),
              new TextRun({ children: [PageNumber.CURRENT], font: "Montserrat", size: 16, color: PEACH }),
            ]
          })
        ]
      })
    },
    children: [

      // ══════════════════════════════════════════
      // COVER / TITLE
      // ══════════════════════════════════════════
      space(4),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
        children: [new TextRun({ text: "✦  AI CONTENT GENERATOR  ✦", font: "Georgia", size: 52, bold: true, color: PEACH })]
      }),
      space(1),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
        children: [new TextRun({ text: "Frontend Design & Implementation Specification", font: "Montserrat", size: 24, color: "AAAAAA" })]
      }),
      space(1),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        spacing: { before: 0, after: 0 },
        children: [new TextRun({ text: "Theme: Peach on Black  |  Stack: React + TailwindCSS  |  Version 2.0", font: "Montserrat", size: 18, color: "666666", italics: true })]
      }),
      space(6),
      divider(),

      // ══════════════════════════════════════════
      // SECTION 1 — DESIGN SYSTEM
      // ══════════════════════════════════════════
      h1("1. Design System"),
      body("This section replaces the blue & white SF Pro theme from the original implementation plan. All frontend components must be rebuilt against the specifications below."),
      space(),

      h2("1.1 Color Palette"),
      space(),
      makeTable(
        ["Token", "Hex Value", "Usage"],
        [
          ["--color-bg", "#000000", "Root page background"],
          ["--color-surface", "#0D0D0D", "Cards, sidebars, modals"],
          ["--color-surface-raised", "#1A1A1A", "Input fields, message bubbles, dropdowns"],
          ["--color-border", "#2A2A2A", "Dividers, input borders, card edges"],
          ["--color-peach", "#FFBE9D", "Primary buttons, active states, icons, links"],
          ["--color-peach-hover", "#E8A07A", "Hover state for all peach elements"],
          ["--color-peach-subtle", "#3A2010", "Peach-tinted backgrounds (e.g., selected items)"],
          ["--color-text-primary", "#FFFFFF", "Headings, important labels"],
          ["--color-text-secondary", "#A0A0A0", "Descriptions, timestamps, placeholders"],
          ["--color-text-muted", "#555555", "Disabled states, helper text"],
          ["--color-success", "#4CAF50", "Success toasts, positive states"],
          ["--color-error", "#FF5252", "Error messages, destructive actions"],
        ]
      ),
      space(),
      note("Add these as CSS custom properties in your global :root {} block in index.css or tailwind.config.js. Use Tailwind's extend.colors to map them for class-based usage."),
      space(),

      h2("1.2 Typography"),
      space(),
      makeTable(
        ["Element", "Font Family", "Weight", "Size", "Color"],
        [
          ["Page Title (H1)", "Georgia, serif", "Bold (700)", "2.5rem", "--color-peach"],
          ["Section Title (H2)", "Georgia, serif", "Bold (700)", "1.75rem", "--color-text-primary"],
          ["Sub-heading (H3)", "Georgia, serif", "SemiBold (600)", "1.25rem", "--color-text-primary"],
          ["Body text", "Montserrat, sans-serif", "Regular (400)", "1rem", "--color-text-secondary"],
          ["Button labels", "Montserrat, sans-serif", "Bold (700)", "0.875rem", "#000000 on peach / #fff on dark"],
          ["Input text", "Montserrat, sans-serif", "Regular (400)", "1rem", "--color-text-primary"],
          ["Code / AI output", "JetBrains Mono, monospace", "Regular (400)", "0.875rem", "--color-text-primary"],
          ["Timestamps / meta", "Montserrat, sans-serif", "Regular (400)", "0.75rem", "--color-text-muted"],
          ["Navigation links", "Montserrat, sans-serif", "Medium (500)", "0.9rem", "--color-text-secondary"],
        ]
      ),
      space(),
      warn("Remove SF Pro / system-ui from all font declarations. Montserrat must be loaded via Google Fonts. Add these two imports to index.html:"),
      space(),
      codeBlock([
        '<link rel="preconnect" href="https://fonts.googleapis.com">',
        '<link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">',
      ]),
      space(),
      note("Georgia is a web-safe font — no import needed. It is already available in all browsers."),
      space(),

      h2("1.3 Tailwind Configuration"),
      body("Replace the contents of tailwind.config.js with the following to register the design tokens:"),
      space(),
      codeBlock([
        "// tailwind.config.js",
        "export default {",
        "  content: ['./index.html', './src/**/*.{js,jsx}'],",
        "  theme: {",
        "    extend: {",
        "      colors: {",
        "        bg:           '#000000',",
        "        surface:      '#0D0D0D',",
        "        'surface-raised': '#1A1A1A',",
        "        border:       '#2A2A2A',",
        "        peach:        '#FFBE9D',",
        "        'peach-hover':'#E8A07A',",
        "        'peach-subtle':'#3A2010',",
        "      },",
        "      fontFamily: {",
        "        heading: ['Georgia', 'serif'],",
        "        body:    ['Montserrat', 'sans-serif'],",
        "        code:    ['JetBrains Mono', 'monospace'],",
        "      },",
        "    },",
        "  },",
        "  plugins: [],",
        "};",
      ]),
      space(),

      h2("1.4 Component Design Tokens — Buttons"),
      body("All button variants below are based on Montserrat Bold. Rounded corners: rounded-xl (12px). Transition: 150ms ease."),
      space(),
      makeTable(
        ["Variant", "Background", "Text Color", "Hover BG", "Usage"],
        [
          ["Primary", "#FFBE9D (peach)", "#000000", "#E8A07A", "Main CTAs: Send, Login, Register, Get Started"],
          ["Secondary", "transparent", "#FFBE9D", "rgba(255,190,157,0.1)", "Cancel, secondary actions"],
          ["Ghost", "transparent", "#A0A0A0", "rgba(255,255,255,0.05)", "Nav links, subtle actions"],
          ["Danger", "transparent", "#FF5252", "rgba(255,82,82,0.1)", "Delete account, delete session"],
          ["Icon Button", "#1A1A1A", "#A0A0A0", "#2A2A2A + peach icon", "Copy, Regenerate, Like on AI messages"],
        ]
      ),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 2 — LOGO
      // ══════════════════════════════════════════
      h1("2. Logo"),
      body("The app logo must be generated using the following exact prompt and integrated as an SVG or PNG in the Navbar and Login/Register pages."),
      space(),

      h2("2.1 Logo Generation Prompt"),
      codeBlock([
        '"Minimal AI logo with neural nodes forming a spark, peach accent on black,',
        ' modern SaaS style, clean and geometric"',
      ]),
      space(),
      body("Recommended generation tools: Midjourney, DALL-E 3, Adobe Firefly, or Ideogram. Export as SVG if possible, PNG @2x (400x400px) as fallback."),
      space(),

      h2("2.2 Logo Usage Rules"),
      bullet("In Navbar: 32px height, left-aligned, paired with app name in Georgia Bold, peach color"),
      bullet("In Login/Register pages: 64px height, centered above the form card"),
      bullet("Favicon: Use the spark/node icon only (no text), 32x32px ICO/SVG"),
      bullet("Dark background only — never place logo on light backgrounds"),
      bullet("Minimum clear space: 16px on all sides"),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 3 — LAYOUT & NAVIGATION
      // ══════════════════════════════════════════
      h1("3. Layout & Navigation"),
      space(),

      h2("3.1 Navbar (Navbar.jsx)"),
      body("The Navbar is present on the Landing Page and Chat Page. It is hidden on Login and Register pages (those use centered card layouts without nav)."),
      space(),
      makeTable(
        ["Property", "Value"],
        [
          ["Background", "#000000 with a bottom border of 1px solid #2A2A2A"],
          ["Height", "56px"],
          ["Position", "sticky top-0, z-index: 50"],
          ["Left content", "Logo SVG + App name in Georgia Bold, peach, 18px"],
          ["Right content", "Navigation links + Login/Logout button"],
          ["Font", "Montserrat Medium, 0.9rem"],
          ["Active link indicator", "Underline in peach, 2px"],
          ["Mobile", "Hamburger menu — collapses to drawer sliding in from right"],
        ]
      ),
      space(),

      h3("Navbar Links"),
      bullet("Home  → navigates to /"),
      bullet("Chat  → navigates to /chat  (always visible)"),
      bullet("Login → navigates to /login  (visible only when NOT logged in)"),
      bullet("Logout → calls logout(), clears JWT, redirects to /  (visible only when logged in)"),
      bullet("Profile → navigates to /profile  (visible only when logged in)"),
      space(),
      warn("Replace the existing Navbar design that includes Image Generator, Video, Music, Voice Chat, Photo Editor tabs. Those features are out of scope. The new Navbar is minimal with only the links listed above."),
      space(),

      h2("3.2 Sidebar (Sidebar.jsx) — Chat Page Only"),
      makeTable(
        ["Property", "Value"],
        [
          ["Width", "260px on desktop, full-screen drawer on mobile"],
          ["Background", "#0D0D0D"],
          ["Border", "1px solid #2A2A2A on right edge"],
          ["Position", "Fixed left, full height"],
          ["Top section", "New Chat button (full-width, peach primary)"],
          ["Middle section", "Scrollable list of chat sessions"],
          ["Bottom section", "User avatar + display name + Settings icon"],
        ]
      ),
      space(),

      h3("Session List Item"),
      bullet("Session title truncated with ellipsis after ~30 chars"),
      bullet("Timestamp in muted text (e.g., '2 hours ago' using date-fns)"),
      bullet("Active session: peach-subtle background (#3A2010), left border 2px peach"),
      bullet("Hover: #1A1A1A background"),
      bullet("Delete icon (Trash2 from lucide-react) appears on hover, right-aligned, red on hover"),
      space(),

      h2("3.3 Footer"),
      body("A simple, minimal footer displayed on the Landing Page only. Not shown inside the Chat Page or auth pages."),
      space(),
      makeTable(
        ["Element", "Detail"],
        [
          ["Background", "#000000, border-top: 1px solid #2A2A2A"],
          ["Padding", "32px vertical"],
          ["Left: App Name", "Georgia Bold, 16px, peach — 'AI Content Generator'"],
          ["Left: Tagline", "Montserrat, 14px, muted — 'Generate smarter content, faster.'"],
          ["Right: Links", "Home · Chat · Login — Montserrat Medium, 14px, gray, peach on hover"],
          ["Link behavior", "React Router <Link> — no page reload. Active link gets peach color."],
          ["Copyright", "Centered bottom line: '© 2025 AI Content Generator. All rights reserved.' — muted, 12px"],
        ]
      ),
      space(),
      warn("All footer links must use React Router's <Link to='...'> — not <a href='...'>. Using anchor tags will cause full page reloads."),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 4 — PAGES
      // ══════════════════════════════════════════
      h1("4. Pages — Detailed Specifications"),
      space(),

      // ── Landing Page ──
      h2("4.1 Landing Page (/)"),
      body("The Landing Page is the first impression. It must be visually striking — dark, premium, focused on conversion. The primary CTA is 'Get Started'."),
      space(),

      h3("Hero Section"),
      bullet("Full viewport height (min-h-screen), black background"),
      bullet("Centered vertically and horizontally"),
      bullet("Large headline: 'Generate Content with AI' — Georgia Bold, 3.5rem, white, with 'AI' in peach"),
      bullet("Subheading (1 line): Montserrat, 1.1rem, gray — 'Blog posts, emails, social media, and more. In seconds.'"),
      bullet("Spacing between headline and subheading: 16px"),
      bullet("CTA Button: 'Get Started' — peach primary button, large (px-8 py-4), Montserrat Bold"),
      bullet("Below CTA: small muted text — 'No credit card required. Free forever.'"),
      space(),

      h3("'Get Started' Button Behavior"),
      bullet("On click: navigate to /chat using React Router's useNavigate()"),
      bullet("Do NOT use window.location.href — use programmatic navigation"),
      bullet("No auth check at this stage — the auth check happens inside the Chat Page"),
      space(),

      h3("Features Section (below hero, optional)"),
      bullet("3-column grid on desktop, 1-column on mobile"),
      bullet("Each card: #0D0D0D background, 1px border #2A2A2A, rounded-xl, padding 24px"),
      bullet("Icon (lucide-react): peach, 28px"),
      bullet("Title: Georgia SemiBold, white, 1.1rem"),
      bullet("Description: Montserrat Regular, gray, 0.9rem"),
      bullet("Suggested features: Blog Posts, Email Copy, Social Media — matching the app's content types"),
      space(),

      // ── Chat Page ──
      h2("4.2 Chat Page (/chat)"),
      body("The Chat Page is the core app experience. It is protected — unauthenticated users are redirected to /login."),
      space(),

      h3("Auth Guard"),
      bullet("Wrap <ChatPage /> with a ProtectedRoute component"),
      bullet("ProtectedRoute checks AuthContext for a valid JWT token"),
      bullet("If no token: redirect to /login, preserving the attempted URL via location.state so the user is redirected back after login"),
      space(),

      h3("Layout"),
      bullet("Left: Sidebar (260px fixed) — session list, new chat, user info"),
      bullet("Right: Main area — takes remaining width, flex column"),
      bullet("Main area: header bar + message area (scrollable) + input bar (sticky bottom)"),
      space(),

      h3("Header Bar (inside main area)"),
      bullet("Shows current session title or 'New Chat' as placeholder"),
      bullet("Content type selector dropdown on the right (Blog Post / Email / Social Media / Ad Copy / General)"),
      bullet("Dropdown style: #1A1A1A bg, peach border on focus, Montserrat text, white chevron icon"),
      space(),

      h3("Message Bubbles"),
      makeTable(
        ["Property", "User Message", "AI Message"],
        [
          ["Alignment", "Right-aligned", "Left-aligned"],
          ["Background", "#1A1A1A (surface-raised)", "#0D0D0D (surface)"],
          ["Border", "none", "1px solid #2A2A2A"],
          ["Border Radius", "rounded-2xl rounded-br-sm", "rounded-2xl rounded-bl-sm"],
          ["Text color", "White", "White / rendered as Markdown"],
          ["Font", "Montserrat Regular, 1rem", "JetBrains Mono for code blocks, Montserrat for prose"],
          ["Max width", "70% of container", "80% of container"],
          ["Padding", "12px 16px", "16px 20px"],
          ["Timestamp", "Bottom-right, muted 0.7rem", "Bottom-left, muted 0.7rem"],
        ]
      ),
      space(),

      h3("AI Message Action Buttons"),
      bullet("Appear below each AI message on hover"),
      bullet("Copy (Copy icon from lucide): copies raw text to clipboard. Shows green checkmark for 1.5s on success."),
      bullet("Regenerate (RefreshCw icon): resends the same user prompt, appends new AI response"),
      bullet("Like (ThumbsUp icon): local state toggle — filled peach when active"),
      bullet("All three are Icon Button variant (see Section 1.4)"),
      space(),

      h3("Typing Indicator"),
      bullet("Show three animated dots when awaiting AI response"),
      bullet("Left-aligned, same position as AI message"),
      bullet("CSS animation: scale pulse, 0.4s stagger between dots, peach color"),
      space(),

      h3("Input Bar"),
      bullet("Sticky to bottom of main area"),
      bullet("Black background with top border 1px #2A2A2A"),
      bullet("Textarea (auto-resize, max 5 rows): #1A1A1A bg, no outline, peach border on focus, Montserrat"),
      bullet("Send button: peach primary, icon (Send from lucide), right of textarea"),
      bullet("Send disabled state: opacity-40, not-allowed cursor when textarea is empty or request in-flight"),
      bullet("Enter key: submits (Shift+Enter for newline)"),
      space(),

      h3("Auth Intercept on Send"),
      bullet("Before calling the API: check AuthContext.isAuthenticated"),
      bullet("If NOT authenticated: do NOT submit. Instead, navigate to /login with state: { from: '/chat' }"),
      bullet("After login, redirect back to /chat automatically (read location.state.from in LoginPage)"),
      space(),

      // ── Login Page ──
      h2("4.3 Login Page (/login)"),
      body("Centered card layout. Navbar and Footer are hidden on this page."),
      space(),
      makeTable(
        ["Element", "Specification"],
        [
          ["Page background", "Black (#000000) with subtle radial gradient: peach at 5% opacity in center"],
          ["Card", "#0D0D0D, border 1px solid #2A2A2A, rounded-2xl, padding 40px, max-width 440px, centered"],
          ["Logo", "Centered, 56px height, above heading"],
          ["Heading", "'Welcome back' — Georgia Bold, 1.75rem, white"],
          ["Subheading", "'Sign in to your account' — Montserrat, 0.9rem, gray"],
          ["Email input", "Full width, #1A1A1A bg, 1px border #2A2A2A, peach focus ring, Montserrat, white text"],
          ["Password input", "Same as email, with eye toggle icon (Eye/EyeOff from lucide) for show/hide"],
          ["Remember me", "Checkbox with 'Remember me' label — peach checkbox accent, Montserrat 0.875rem, gray"],
          ["Login button", "Full width, peach primary, 'Sign In', Montserrat Bold — submit on click and Enter key"],
          ["Error state", "Red inline error below input (invalid credentials, etc.) — FF5252, 0.8rem"],
          ["Footer link", "'Don\u2019t have an account? Register \u2192' — gray with peach hover, navigates to /register"],
        ]
      ),
      space(),

      // ── Register Page ──
      h2("4.4 Register Page (/register)"),
      body("Same card layout as Login. Navbar and Footer hidden."),
      space(),
      makeTable(
        ["Field", "Validation"],
        [
          ["Full Name", "Required, 2-100 characters"],
          ["Username", "Required, 3-30 chars, alphanumeric + underscores only, lowercase"],
          ["Email", "Required, valid email format"],
          ["Password", "Required, min 8 chars, at least 1 uppercase + 1 number"],
          ["Confirm Password", "Must match Password field exactly"],
          ["Terms checkbox", "Must be checked to enable Register button"],
        ]
      ),
      space(),
      bullet("Show inline validation errors beneath each field on blur (not on type)"),
      bullet("Password strength indicator: thin bar below password field — red/orange/green based on strength"),
      bullet("Register button: disabled until all fields valid and terms checked"),
      bullet("On success: show toast 'Account created!', redirect to /chat"),
      bullet("Footer link: 'Already have an account? Sign In' — navigates to /login"),
      space(),

      // ── Profile Page ──
      h2("4.5 Profile Page (/profile)"),
      body("Protected route. Split into three visual sections: Profile Info, Change Password, Danger Zone."),
      space(),

      h3("Profile Info Section"),
      bullet("Avatar: circular, 80px, upload on click (pencil overlay icon) — accepts JPG/PNG, max 2MB"),
      bullet("Full Name: editable text input"),
      bullet("Username: editable, same validation as register"),
      bullet("Email: read-only input (grayed out) — labeled 'Email cannot be changed'"),
      bullet("'Save Changes' button: peach primary, only enabled when a field has been modified"),
      bullet("Success toast on save: 'Profile updated successfully'"),
      space(),

      h3("Usage Stats"),
      bullet("Two stat cards side by side: 'Total Sessions' and 'Messages Sent'"),
      bullet("Card style: #0D0D0D, 1px border, rounded-xl, peach number in Georgia Bold, gray label in Montserrat"),
      space(),

      h3("Change Password Section"),
      bullet("Three fields: Current Password, New Password, Confirm New Password"),
      bullet("Same validation as register password field"),
      bullet("'Update Password' peach primary button"),
      bullet("Error: 'Current password is incorrect' — shown inline"),
      space(),

      h3("Danger Zone"),
      bullet("Visually separated with a red dashed border section"),
      bullet("Heading: 'Danger Zone' — Montserrat Bold, red (#FF5252)"),
      bullet("Text: 'Permanently delete your account and all chat history. This cannot be undone.'"),
      bullet("'Delete Account' button: Danger variant (see Section 1.4)"),
      bullet("On click: open a confirmation modal requiring the user to type their username to confirm"),
      bullet("Modal confirm button is disabled until typed username matches exactly"),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 5 — AUTH FLOW
      // ══════════════════════════════════════════
      h1("5. Authentication Flow"),
      space(),

      h2("5.1 JWT Storage & AuthContext"),
      bullet("Store JWT in localStorage under key: 'auth_token'"),
      bullet("Store user info (id, email, username) in localStorage under key: 'auth_user'"),
      bullet("AuthContext exposes: { user, token, isAuthenticated, login(), logout() }"),
      bullet("On app mount: read localStorage and hydrate AuthContext state"),
      bullet("login(token, user): writes to localStorage + sets context state"),
      bullet("logout(): clears localStorage + resets context + navigates to /"),
      space(),

      h2("5.2 Axios Interceptor"),
      bullet("In services/api.js: attach Authorization: Bearer <token> header to every request"),
      bullet("Response interceptor: on 401 response, call logout() and redirect to /login"),
      bullet("This handles token expiry automatically without manual checks"),
      space(),

      h2("5.3 Protected Route Component"),
      codeBlock([
        "// components/ProtectedRoute.jsx",
        "const ProtectedRoute = ({ children }) => {",
        "  const { isAuthenticated } = useAuth();",
        "  const location = useLocation();",
        "  if (!isAuthenticated) {",
        "    return <Navigate to='/login' state={{ from: location.pathname }} replace />;",
        "  }",
        "  return children;",
        "};",
      ]),
      space(),
      body("Wrap all protected pages in App.jsx using this component:"),
      codeBlock([
        "<Route path='/chat'    element={<ProtectedRoute><ChatPage /></ProtectedRoute>} />",
        "<Route path='/profile' element={<ProtectedRoute><ProfilePage /></ProtectedRoute>} />",
      ]),
      space(),

      h2("5.4 Post-Login Redirect"),
      codeBlock([
        "// In LoginPage.jsx after successful login:",
        "const location = useLocation();",
        "const from = location.state?.from || '/chat';",
        "navigate(from, { replace: true });",
      ]),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 6 — COMPONENT BREAKDOWN
      // ══════════════════════════════════════════
      h1("6. Component Breakdown"),
      space(),

      h2("6.1 UI Primitives (src/components/ui/)"),
      makeTable(
        ["Component", "Props", "Notes"],
        [
          ["Button.jsx", "variant, size, loading, disabled, onClick", "All 5 variants from Section 1.4. Loading shows Spinner inline."],
          ["Input.jsx", "label, error, type, icon, ...rest", "Supports email, password (eye toggle), text. Peach focus ring."],
          ["Textarea.jsx", "placeholder, maxRows, onChange, value", "Auto-resizes. Max 5 rows before scroll."],
          ["Modal.jsx", "isOpen, onClose, title, children", "Overlay: rgba(0,0,0,0.8). Card: #0D0D0D, centered."],
          ["Spinner.jsx", "size, color", "CSS border animation. Default: peach 20px."],
          ["Toast.jsx", "Handled by react-hot-toast", "Configure toaster: dark bg, peach accent in _app or main.jsx."],
          ["Avatar.jsx", "src, fallback (initials), size", "Circular. Peach border. Shows initials on missing image."],
        ]
      ),
      space(),

      h2("6.2 Chat Components (src/components/chat/)"),
      makeTable(
        ["Component", "Responsibility"],
        [
          ["ChatWindow.jsx", "Renders list of MessageBubble. Auto-scrolls to bottom on new message. Manages scroll ref."],
          ["MessageBubble.jsx", "Renders single message (user or AI). Handles markdown rendering for AI messages. Shows action buttons on hover."],
          ["InputBar.jsx", "Textarea + Send button + auth intercept logic. Emits onSend(text) to parent."],
          ["ContentTypeSelector.jsx", "Dropdown for content type. Options: General, Blog Post, Email, Social Media Post, Ad Copy."],
          ["TypingIndicator.jsx", "3-dot animated indicator. Shown when isLoading=true."],
          ["SessionList.jsx", "Renders list of sessions in sidebar. Handles select + delete per session."],
        ]
      ),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 7 — ROUTING
      // ══════════════════════════════════════════
      h1("7. Routing (App.jsx)"),
      space(),
      codeBlock([
        "// App.jsx route structure",
        "<Routes>",
        "  <Route path='/'         element={<LandingPage />} />",
        "  <Route path='/login'    element={<LoginPage />} />",
        "  <Route path='/register' element={<RegisterPage />} />",
        "  <Route path='/chat'     element={",
        "    <ProtectedRoute><ChatPage /></ProtectedRoute>",
        "  } />",
        "  <Route path='/profile'  element={",
        "    <ProtectedRoute><ProfilePage /></ProtectedRoute>",
        "  } />",
        "  <Route path='*'         element={<Navigate to='/' replace />} />",
        "</Routes>",
      ]),
      space(),
      bullet("LandingPage, LoginPage, RegisterPage render without Sidebar"),
      bullet("ChatPage renders with Sidebar + no Footer"),
      bullet("LandingPage renders with Navbar + Footer"),
      bullet("LoginPage and RegisterPage render without Navbar and without Footer"),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 8 — RESPONSIVENESS
      // ══════════════════════════════════════════
      h1("8. Responsive Design"),
      space(),
      makeTable(
        ["Breakpoint", "Tailwind Prefix", "Sidebar Behavior", "Navbar Behavior", "Chat Layout"],
        [
          ["< 640px (mobile)", "default", "Hidden. Toggle via hamburger button.", "Hamburger menu icon. Drawer from right.", "Full width. Input bar stacked."],
          ["640–1024px (tablet)", "sm / md", "Hidden by default. Slide-in on toggle.", "Partial links + hamburger.", "Full width main area."],
          ["> 1024px (desktop)", "lg", "Always visible (260px fixed left).", "All links visible horizontally.", "Sidebar + main area side by side."],
        ]
      ),
      space(),
      bullet("Mobile sidebar toggle: add a HamburgerMenuIcon button in Navbar top-left on mobile"),
      bullet("Sidebar overlay on mobile: add a translucent black overlay behind the open sidebar, click to close"),
      bullet("Input bar on mobile: full width, Send button below textarea (stacked) if viewport < 400px"),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 9 — ANIMATIONS & MICRO-INTERACTIONS
      // ══════════════════════════════════════════
      h1("9. Animations & Micro-interactions"),
      space(),
      makeTable(
        ["Interaction", "Animation", "Implementation"],
        [
          ["Page load (Landing)", "Hero text fades in + slides up", "CSS: opacity 0→1, translateY 20px→0, 0.6s ease, 0.1s delay"],
          ["Button hover (Primary)", "Slight scale + darker peach", "Tailwind: hover:scale-[1.02] hover:bg-peach-hover transition-all duration-150"],
          ["Message appear", "Fade in from bottom", "CSS: opacity 0→1, translateY 8px→0, 0.25s ease"],
          ["Typing indicator", "3 dots pulse sequentially", "CSS animation with animation-delay: 0s, 0.15s, 0.3s"],
          ["Sidebar session hover", "Background transition", "transition-colors duration-150"],
          ["Copy button feedback", "Icon swaps to CheckCircle for 1.5s", "useState for copied state + setTimeout reset"],
          ["Input focus", "Peach ring appears", "Tailwind: focus:ring-2 focus:ring-peach focus:ring-opacity-50"],
          ["Toast notifications", "Slide in from top-right", "react-hot-toast default — customize with dark toastOptions"],
        ]
      ),
      space(),
      note("Keep animations subtle and purposeful. Do not add gratuitous motion — the dark theme and typography carry the visual weight. Animations should feel fast (< 300ms) and reinforce actions."),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 10 — SUGGESTIONS
      // ══════════════════════════════════════════
      h1("10. Design Suggestions & Recommendations"),
      body("The following suggestions go beyond the stated requirements and are offered to elevate the overall product quality. These are optional but highly recommended."),
      space(),

      h2("10.1 Color Suggestions"),
      bullet("Consider adding a very subtle grain texture overlay on the black background (5% opacity SVG noise filter) — this prevents the pure black from feeling flat on OLED screens and gives a premium feel."),
      bullet("For the peach (#FFBE9D), ensure WCAG AA contrast on black. Run it through a contrast checker — the combination passes at large text sizes. For small body text, use white (#FFFFFF) instead of peach to maintain legibility."),
      bullet("Add a peach-to-transparent gradient as a top glow on the Landing Page hero — place it as a radial gradient behind the headline only. This creates depth without distracting from the content."),
      space(),

      h2("10.2 UX Suggestions"),
      bullet("Auto-generate session titles: after the first AI response, silently call a short API prompt to summarize the session in 4-5 words and use it as the session title in the sidebar. This is far better than 'New Chat #1, #2...'"),
      bullet("Add a content type badge on each session in the sidebar (e.g., a small 'Blog' or 'Email' chip). This helps users quickly find past work."),
      bullet("Consider an empty state illustration for the Chat Page when there are no sessions yet. A minimal SVG of a spark/node (matching the logo motif) with text 'Start your first session' works well."),
      bullet("Add keyboard shortcut Cmd/Ctrl + K to open a session search modal — this is a power-user feature that makes the app feel polished and professional."),
      bullet("Show a word/character count in the bottom-right of the input textarea. Useful for users generating content with length constraints."),
      space(),

      h2("10.3 Typography Suggestions"),
      bullet("The Georgia + Montserrat pairing is excellent — Georgia gives editorial authority to headings while Montserrat provides clean readability in UI contexts. Stick to this pairing consistently."),
      bullet("For AI-generated content in chat bubbles, render it with react-markdown and style the output carefully: peach for H1-H3 headings inside the bubble, subtle horizontal rules, code blocks in JetBrains Mono with a slightly lighter surface background."),
      bullet("Use letter-spacing: 0.05em on the Navbar app name ('AI CONTENT GENERATOR' in uppercase tracking) — it adds a premium SaaS feel."),
      space(),

      h2("10.4 Performance Suggestions"),
      bullet("Lazy-load all page components using React.lazy() and Suspense. This reduces initial bundle size significantly."),
      bullet("Memoize SessionList items with React.memo to prevent unnecessary re-renders as new messages come in."),
      bullet("Use IntersectionObserver for auto-scroll in ChatWindow rather than scrollIntoView() on every render — smoother on large message lists."),
      space(),

      divider(),

      // ══════════════════════════════════════════
      // SECTION 11 — CHANGE SUMMARY
      // ══════════════════════════════════════════
      h1("11. Changes from Original Implementation Plan (v1.0)"),
      body("The following is a complete diff summary of what changes from the original Phase 3 plan:"),
      space(),
      makeTable(
        ["Area", "Original (v1.0)", "New (v2.0)"],
        [
          ["Primary color", "Blue (#1D6CF2)", "Peach (#FFBE9D)"],
          ["Hover color", "Dark blue (#0F4DC9)", "Peach dark (#E8A07A)"],
          ["Background", "White / Light gray (#F7F9FC)", "Black (#000000)"],
          ["Surface color", "White (#FFFFFF)", "Near-black (#0D0D0D, #1A1A1A)"],
          ["Text primary", "Dark (#1A1A2E)", "White (#FFFFFF)"],
          ["Text secondary", "Medium gray (#5F6B7A)", "Gray (#A0A0A0)"],
          ["Font (headings)", "SF Pro / system-ui", "Georgia (serif)"],
          ["Font (body/UI)", "SF Pro / system-ui", "Montserrat (sans-serif)"],
          ["Font (code)", "Not specified", "JetBrains Mono (monospace)"],
          ["Navbar links", "7 tabs including Video, Music, etc.", "4 links: Home, Chat, Login/Logout, Profile"],
          ["Footer", "Not specified", "App name + tagline + 3 navigation links"],
          ["Landing CTA", "Not specified", "'Get Started' → navigates to /chat"],
          ["Auth intercept", "Not specified", "Chat send → redirect to /login if unauthenticated"],
          ["Logo", "Generic", "Neural spark logo, peach on black (specific prompt provided)"],
        ]
      ),
      space(),
      warn("The backend (Spring Boot), AI service (Python FastAPI), database schema (Supabase), and all API contracts are UNCHANGED. Only the React frontend layer is affected by this document."),
      space(),

      divider(),

      // Footer note
      space(2),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: "End of Frontend Specification — v2.0",
          font: "Georgia", size: 18, color: "555555", italics: true
        })]
      }),
      new Paragraph({
        alignment: AlignmentType.CENTER,
        children: [new TextRun({
          text: "AI Content Generator  ✦  Peach & Black Theme",
          font: "Montserrat", size: 16, color: "333333"
        })]
      }),

    ]
  }]
});

Packer.toBuffer(doc).then(buffer => {
  fs.writeFileSync('/home/claude/frontend-spec-v2.docx', buffer);
  console.log('Done.');
});