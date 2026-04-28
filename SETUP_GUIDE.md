# Creo Frontend Setup Guide

## 🚀 Quick Start

### Prerequisites
- Node.js 16+ installed
- npm or yarn package manager
- Backend service running (see backend README)

### Installation

1. **Navigate to frontend directory**
```bash
cd frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Configure environment variables**
Create a `.env` file in the `frontend` directory:
```env
VITE_API_BASE_URL=http://localhost:8080/api
```

4. **Start development server**
```bash
npm run dev
```

The application will be available at `http://localhost:5173`

## 📦 Dependencies

All required dependencies are already in `package.json`:

### Core
- **React 18.2.0** - UI framework
- **React Router DOM 6.21.1** - Routing
- **Axios 1.6.5** - HTTP client

### UI & Animations
- **Framer Motion 12.38.0** ✨ - Animation library
- **Lucide React 0.303.0** - Icon library
- **Tailwind CSS 3.4.0** - Utility-first CSS

### Utilities
- **Date-fns 3.0.6** - Date manipulation
- **React Hot Toast 2.4.1** - Toast notifications
- **React Markdown 9.0.1** - Markdown rendering

## 🎨 New Features Overview

### 1. Chat History Sidebar with Date Grouping
- Conversations organized by: Today, Yesterday, This Week, This Month, Older
- Real-time search across all history
- Animated list transitions
- Session count badges

### 2. Daily Reset Indicator
- Live countdown to midnight (12:00 AM)
- Visual progress bar (0-10 messages)
- Color-coded warnings
- Automatic updates every second

### 3. Enhanced Animations
- Smooth page transitions
- Hover effects on all interactive elements
- Staggered list animations
- Micro-interactions throughout

### 4. Branding: "Creo"
- Consistent naming across all pages
- Professional, memorable brand identity
- No generic "AI" suffix

## 🔧 Configuration

### Tailwind CSS
The project uses a custom Tailwind configuration with:
- Custom color palette (peach theme)
- Extended animations
- Custom utilities
- Dark theme optimized

### Vite
Fast build tool with:
- Hot Module Replacement (HMR)
- Optimized production builds
- React Fast Refresh

## 📁 Project Structure

```
frontend/
├── src/
│   ├── components/
│   │   ├── chat/
│   │   │   ├── Sidebar.jsx (✨ Updated)
│   │   │   ├── ChatWindow.jsx (✨ Updated)
│   │   │   ├── InputBar.jsx (✨ Updated)
│   │   │   ├── DailyResetIndicator.jsx (🆕 New)
│   │   │   ├── MessageBubble.jsx
│   │   │   ├── ContentTypeSelector.jsx
│   │   │   ├── ToneSelector.jsx
│   │   │   ├── LengthSelector.jsx
│   │   │   └── LanguageSelector.jsx
│   │   └── ProtectedRoute.jsx
│   ├── context/
│   │   ├── AuthContext.jsx
│   │   └── ChatContext.jsx
│   ├── pages/
│   │   ├── ChatPage.jsx (✨ Updated)
│   │   ├── LandingPage.jsx
│   │   ├── LoginPage.jsx
│   │   ├── RegisterPage.jsx
│   │   └── ProfilePage.jsx
│   ├── services/
│   │   ├── api.js
│   │   ├── authService.js
│   │   ├── chatService.js
│   │   └── userService.js
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css (✨ Updated)
├── public/
├── .env
├── package.json
├── tailwind.config.js
├── vite.config.js
└── README.md
```

## 🎯 Key Components

### DailyResetIndicator
**Location**: `src/components/chat/DailyResetIndicator.jsx`

Shows daily message usage and countdown to reset:
```jsx
<DailyResetIndicator 
  dailyMessageCount={user?.dailyMessageCount || 0} 
  maxMessages={10} 
/>
```

**Features:**
- Real-time countdown (updates every second)
- Progress bar visualization
- Color-coded warnings (red at 80%+)
- Smooth animations

### Enhanced Sidebar
**Location**: `src/components/chat/Sidebar.jsx`

**New Features:**
- Date-based grouping (Today, Yesterday, etc.)
- Animated session lists
- Search functionality
- Refresh button with loading state
- Smooth slide-in animation

**Date Groups:**
```javascript
{
  today: [],      // Today's chats
  yesterday: [],  // Yesterday's chats
  thisWeek: [],   // Last 7 days
  thisMonth: [],  // Current month
  older: []       // Everything else
}
```

### Animated Chat Window
**Location**: `src/components/chat/ChatWindow.jsx`

**Enhancements:**
- Welcome screen with floating bot icon
- Pulsing glow effects
- Staggered message animations
- Smooth scroll behavior

### Enhanced Input Bar
**Location**: `src/components/chat/InputBar.jsx`

**Improvements:**
- Focus scale animation
- Rotating gradient on send button
- Sparkle indicators
- Better placeholder text

## 🎨 Styling System

### Custom CSS Classes

**Animations:**
```css
.animate-blink        /* Cursor blink effect */
.animate-gradient     /* Gradient animation */
.animate-float        /* Floating effect */
.animate-pulse-slow   /* Slow pulse */
```

**Buttons:**
```css
.btn-primary    /* Primary action button */
.btn-secondary  /* Secondary button */
.btn-ghost      /* Ghost button */
.btn-danger     /* Danger/delete button */
.btn-icon       /* Icon-only button */
```

**Utilities:**
```css
.input-field       /* Styled input field */
.card              /* Card container */
.custom-scrollbar  /* Custom scrollbar styling */
```

### Color Palette
```javascript
{
  bg: '#000000',              // Pure black background
  surface: '#0A0A0A',         // Dark surface
  'surface-raised': '#141414', // Elevated surface
  border: '#222222',          // Border color
  peach: '#F9A8A8',          // Primary accent
  'peach-hover': '#E59595',   // Hover state
  'peach-subtle': '#4A2020',  // Subtle accent
  'text-primary': '#FFFFFF',  // Primary text
  'text-secondary': '#A0A0A0', // Secondary text
  'text-muted': '#555555',    // Muted text
  success: '#4CAF50',         // Success state
  error: '#FF5252'            // Error state
}
```

## 🔄 Backend Integration

### API Endpoints Used

**Authentication:**
- `POST /api/auth/login` - User login
- `POST /api/auth/register` - User registration
- `POST /api/auth/refresh` - Token refresh

**Chat:**
- `POST /api/chat/message` - Send message
- `POST /api/chat/message/stream` - Stream response
- `GET /api/chat/sessions` - Get all sessions
- `GET /api/chat/sessions/:id` - Get specific session
- `POST /api/chat/sessions` - Create session
- `DELETE /api/chat/sessions/:id` - Delete session
- `DELETE /api/chat/sessions` - Delete all sessions

**User:**
- `GET /api/users/profile` - Get user profile
- `GET /api/users/stats` - Get user statistics

### Daily Reset Logic

**Backend (Java):**
```java
// Automatic reset at midnight
if (lastMessageDate == null || !lastMessageDate.equals(today)) {
    user.setDailyMessageCount(0);
    user.setLastMessageDate(Timestamp.now());
}
```

**Frontend (React):**
```javascript
// Real-time countdown display
const calculateTimeUntilMidnight = () => {
  const now = new Date()
  const midnight = new Date()
  midnight.setHours(24, 0, 0, 0)
  const diff = midnight - now
  // Calculate hours, minutes, seconds
}
```

## 🧪 Testing

### Manual Testing Checklist

**Chat History:**
- [ ] Sessions group correctly by date
- [ ] Search filters work across all groups
- [ ] Delete individual session works
- [ ] Clear all history works
- [ ] Refresh updates the list
- [ ] Active session highlighted

**Daily Reset:**
- [ ] Countdown displays correctly
- [ ] Progress bar shows accurate usage
- [ ] Color changes at 80% usage
- [ ] Timer updates every second
- [ ] Resets at midnight (backend)

**Animations:**
- [ ] Sidebar slides in smoothly
- [ ] Messages fade in with stagger
- [ ] Buttons have hover effects
- [ ] Transitions are smooth (60fps)
- [ ] No janky animations

**Responsive:**
- [ ] Works on mobile (320px+)
- [ ] Works on tablet (768px+)
- [ ] Works on desktop (1024px+)
- [ ] Touch interactions work
- [ ] Sidebar toggles properly

## 🐛 Troubleshooting

### Common Issues

**1. Animations not working**
- Ensure Framer Motion is installed: `npm install framer-motion`
- Check browser compatibility (modern browsers only)
- Clear cache and rebuild

**2. Date grouping incorrect**
- Check system timezone settings
- Verify backend timestamp format
- Ensure date-fns is installed

**3. Daily reset not showing**
- Verify user is authenticated
- Check API response includes `dailyMessageCount`
- Inspect browser console for errors

**4. Styles not applying**
- Run `npm run build` to rebuild Tailwind
- Check for CSS conflicts
- Verify Tailwind config is correct

### Debug Mode

Enable React DevTools:
```bash
npm install -g react-devtools
react-devtools
```

Check Framer Motion animations:
```javascript
// Add to component for debugging
<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  onAnimationStart={() => console.log('Animation started')}
  onAnimationComplete={() => console.log('Animation complete')}
>
```

## 📊 Performance

### Optimization Tips

1. **Lazy Loading**
```javascript
const ChatPage = lazy(() => import('./pages/ChatPage'))
```

2. **Memoization**
```javascript
const groupedSessions = useMemo(() => {
  // Expensive calculation
}, [dependencies])
```

3. **Debouncing**
```javascript
const debouncedSearch = useMemo(
  () => debounce(handleSearch, 300),
  []
)
```

### Metrics to Monitor
- First Contentful Paint (FCP)
- Time to Interactive (TTI)
- Cumulative Layout Shift (CLS)
- Animation frame rate (target: 60fps)

## 🚀 Deployment

### Build for Production
```bash
npm run build
```

Output will be in `dist/` directory.

### Environment Variables
```env
# Production
VITE_API_BASE_URL=https://api.creo.com/api

# Staging
VITE_API_BASE_URL=https://staging-api.creo.com/api

# Development
VITE_API_BASE_URL=http://localhost:8080/api
```

### Deploy to Vercel
```bash
npm install -g vercel
vercel --prod
```

### Deploy to Netlify
```bash
npm run build
netlify deploy --prod --dir=dist
```

## 📚 Additional Resources

- [React Documentation](https://react.dev)
- [Framer Motion Docs](https://www.framer.com/motion/)
- [Tailwind CSS Docs](https://tailwindcss.com)
- [Vite Documentation](https://vitejs.dev)
- [Date-fns Documentation](https://date-fns.org)

## 🎓 Learning Resources

### Framer Motion Tutorials
- [Official Examples](https://www.framer.com/motion/examples/)
- [Animation Patterns](https://www.framer.com/motion/animation/)
- [Gestures & Interactions](https://www.framer.com/motion/gestures/)

### React Best Practices
- [React Patterns](https://reactpatterns.com)
- [Performance Optimization](https://react.dev/learn/render-and-commit)
- [Hooks Guide](https://react.dev/reference/react)

## 🤝 Contributing

When adding new features:
1. Follow existing code style
2. Add animations for interactive elements
3. Ensure responsive design
4. Test on multiple devices
5. Update documentation

## 📝 License

This project is part of the Creo AI platform.

---

**Need Help?** Check the troubleshooting section or review the component documentation in the code.

**Version:** 2.0.0  
**Last Updated:** 2026-04-28
