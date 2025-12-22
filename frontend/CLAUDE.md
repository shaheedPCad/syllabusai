# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Clarity LMS Frontend** - A modern Learning Management System web application built with Next.js 16, React 19, and Tailwind CSS 4. The frontend provides an interactive interface for students and teachers to manage courses, upload documents, chat with an AI tutor, and engage with study materials through flashcards, quizzes, and notes.

## Technology Stack

### Core Framework
- **Next.js 16.0.7**: React framework with App Router and Turbopack
- **React 19.2.0**: UI library with latest concurrent features
- **TypeScript 5**: Type-safe development
- **Node.js**: Runtime environment

### Styling & UI
- **Tailwind CSS 4**: Utility-first CSS framework with modern CSS features
- **tw-animate-css**: Animation utilities for Tailwind
- **@tailwindcss/typography**: Typography plugin for prose content
- **Radix UI**: Accessible component primitives
  - Dialog, Label, Progress, Radio Group, Scroll Area, Select, Separator, Slot, Tabs, Tooltip
- **Framer Motion**: Animation library for React
- **GSAP**: Advanced animation library with React integration
- **class-variance-authority**: CVA for component variants
- **tailwind-merge**: Merge Tailwind classes intelligently

### 3D Graphics & Animation
- **Three.js**: 3D graphics library
- **@react-three/fiber**: React renderer for Three.js
- **@react-three/drei**: Useful helpers for React Three Fiber

### Forms & Validation
- **React Hook Form**: Performant form library
- **Zod**: TypeScript-first schema validation
- **@hookform/resolvers**: Validation resolvers for React Hook Form

### API & Data
- **Axios**: HTTP client for API requests
- **react-markdown**: Markdown renderer for chat messages and content

### Icons & UI Elements
- **Lucide React**: Modern icon library
- **date-fns**: Date utility library

## Project Structure

```
frontend/
├── app/                          # Next.js App Router
│   ├── layout.tsx               # Root layout with fonts and metadata
│   ├── page.tsx                 # Landing page
│   ├── globals.css              # Global styles and Tailwind imports
│   ├── dashboard/               # Dashboard route
│   │   └── page.tsx            # Course management dashboard
│   └── courses/[courseId]/      # Dynamic course routes
│       ├── layout.tsx          # Course layout with navigation
│       ├── page.tsx            # Course overview
│       ├── documents/          # Document management
│       │   └── page.tsx
│       ├── chat/               # AI tutor chat
│       │   └── page.tsx
│       └── study/              # Study tools (flashcards, quizzes, notes)
│           └── page.tsx
├── components/                   # React components
│   ├── landing/                # Landing page sections
│   │   ├── AboutSection.tsx
│   │   ├── CTA.tsx
│   │   ├── Features.tsx
│   │   ├── Footer.tsx
│   │   ├── HowItWorks.tsx
│   │   └── Pricing.tsx
│   ├── dashboard/              # Dashboard components
│   │   ├── CourseCard.tsx
│   │   ├── CreateCourseDialog.tsx
│   │   └── JoinCourse.tsx
│   ├── course/                 # Course feature components
│   │   ├── ChatInterface.tsx   # AI tutor chat UI
│   │   ├── ChatView.tsx
│   │   ├── DocumentList.tsx    # Document display
│   │   ├── DocumentsView.tsx
│   │   ├── UploadZone.tsx      # File upload UI
│   │   ├── StudyView.tsx       # Study tools navigation
│   │   ├── FlashcardSession.tsx
│   │   ├── QuizSession.tsx
│   │   └── NoteView.tsx
│   └── ui/                     # Shared UI components
│       ├── button.tsx
│       ├── hero.tsx            # Hero section with 3D canvas
│       ├── canvas.tsx          # Animated canvas background
│       └── [other shadcn components]
├── services/                     # API service layer
│   ├── courses.ts              # Course CRUD operations
│   ├── documents.ts            # Document upload and management
│   ├── chat.ts                 # Chat with AI tutor
│   └── study.ts                # Flashcards, quizzes, notes
├── lib/                         # Utilities and configurations
│   ├── api.ts                  # Axios instance with interceptors
│   └── utils.ts                # Utility functions (cn helper)
├── hooks/                       # Custom React hooks (if any)
├── public/                      # Static assets
├── .env.local                   # Environment variables
├── package.json                # Dependencies and scripts
├── tsconfig.json               # TypeScript configuration
├── next.config.ts              # Next.js configuration
├── postcss.config.mjs          # PostCSS configuration
├── eslint.config.mjs           # ESLint configuration
└── CLAUDE.md                   # This file
```

## Getting Started

### Prerequisites
- **Node.js**: v20 or higher recommended
- **npm**: Comes with Node.js
- **Backend running**: The FastAPI backend must be running on `http://localhost:8000`

### Installation

```bash
# Install dependencies
npm install
```

### Environment Variables

Create a `.env.local` file in the frontend directory:

```env
# API Configuration
# For local development, the browser connects to the backend via localhost:8000
# This matches the Docker port mapping in docker-compose.yml
NEXT_PUBLIC_API_URL=http://localhost:8000/api/v1
```

**Note**: `NEXT_PUBLIC_` prefix is required for environment variables that need to be exposed to the browser.

### Development Workflow

```bash
# Start development server
npm run dev
# Server runs on http://localhost:3000

# Build for production
npm run build

# Start production server (after build)
npm start

# Run linter
npm run lint
```

### Development Server Details
- **Port**: 3000 (default, will auto-increment if in use)
- **Turbopack**: Enabled by default for faster builds
- **Hot Reload**: Automatic on file changes
- **Type Checking**: Automatic in development

## API Integration

### API Client Setup

The application uses a configured Axios instance located at `lib/api.ts`:

```typescript
import { api } from '@/lib/api';

// GET request
const courses = await api.get('/courses');

// POST request
const newCourse = await api.post('/courses', { title: 'My Course' });
```

### Dev Auth System

The backend uses a development authentication system where users are identified by the `x-user-email` header. This is automatically injected by the API client.

**Default user**: `student@clarity.com`

**Change user for testing:**
```typescript
import { setUserEmail } from '@/lib/api';

// Switch to teacher
setUserEmail('teacher@clarity.com');

// Switch to different student
setUserEmail('alice@clarity.com');
```

**Get current user:**
```typescript
import { getUserEmail } from '@/lib/api';

const email = getUserEmail(); // Returns current user email
```

**Clear user:**
```typescript
import { clearUserEmail } from '@/lib/api';

clearUserEmail(); // Reverts to default user
```

### Service Layer

All API calls are organized in the `services/` directory:

**courses.ts**
- `getCourses()`: Get all courses for current user
- `getCourse(courseId)`: Get specific course details
- `createCourse(data)`: Create new course (teachers)
- `joinCourse(joinCode)`: Join course by code (students)

**documents.ts**
- `getDocuments(courseId)`: Get all documents for a course
- `uploadDocument(courseId, file, title?)`: Upload a document

**chat.ts**
- `sendMessage(courseId, message)`: Send message to AI tutor

**study.ts**
- `getFlashcards(courseId)`: Get flashcard deck
- `generateFlashcards(courseId)`: Generate new flashcards
- `getQuiz(courseId)`: Get quiz
- `generateQuiz(courseId)`: Generate new quiz
- `getNotes(courseId)`: Get study notes
- `generateNotes(courseId)`: Generate new notes

## Features & Routes

### Landing Page (`/`)
- Hero section with animated 3D canvas background
- Features overview
- How it works section
- About section
- Pricing information
- Call to action
- Footer

**Key Components:**
- `Hero`: Main hero with canvas animation (uses `renderCanvas()` from `canvas.tsx`)
- `Features`, `HowItWorks`, `AboutSection`, `Pricing`, `CTA`, `Footer`

### Dashboard (`/dashboard`)
- View all courses (teacher: created, student: enrolled)
- Create new course (teachers)
- Join course by code (students)
- Navigate to course details

**Key Components:**
- `CourseCard`: Display course information
- `CreateCourseDialog`: Modal for course creation
- `JoinCourse`: Join by code input

### Course Pages (`/courses/[courseId]`)

**Layout**: Shared navigation for all course pages

**Overview (`/courses/[courseId]`)**
- Course details
- Quick navigation to features

**Documents (`/courses/[courseId]/documents`)**
- Upload PDFs, documents
- View uploaded documents
- Document processing status
- Background processing with Celery (backend)

**Key Components:**
- `DocumentsView`: Main document page
- `DocumentList`: Display uploaded documents
- `UploadZone`: Drag-and-drop file upload

**Chat (`/courses/[courseId]/chat`)**
- Real-time chat with AI tutor
- Context-aware responses (RAG from uploaded documents)
- Markdown support for formatted responses
- Streaming responses

**Key Components:**
- `ChatView`: Main chat page
- `ChatInterface`: Chat UI with message display and input

**Study Tools (`/courses/[courseId]/study`)**
- Flashcards: Interactive flashcard sessions
- Quizzes: Multiple choice quizzes with instant feedback
- Notes: AI-generated study notes

**Key Components:**
- `StudyView`: Study tools dashboard
- `FlashcardSession`: Flashcard flip interface
- `QuizSession`: Quiz with radio button questions
- `NoteView`: Display study notes with markdown

## Styling Guidelines

### Tailwind CSS 4

This project uses **Tailwind CSS 4**, which has a different import system than v3:

```css
/* globals.css - Tailwind v4 syntax */
@import "tailwindcss";
@import "tw-animate-css";
@plugin "@tailwindcss/typography";
```

**No separate tailwind.config.js** - Configuration is done via CSS variables and `@theme` directive.

### CSS Variables

The app uses CSS custom properties for theming:

```css
:root {
  --primary: oklch(0.205 0 0);
  --primary-foreground: oklch(0.985 0 0);
  --background: oklch(1 0 0);
  --foreground: oklch(0.145 0 0);
  /* ... more variables */
}
```

### Component Styling Pattern

Use the `cn()` utility from `lib/utils.ts` to merge Tailwind classes:

```typescript
import { cn } from '@/lib/utils';

<div className={cn(
  "base-class",
  conditional && "conditional-class",
  className // Props override
)} />
```

### Responsive Design
- Mobile-first approach
- Use Tailwind breakpoints: `sm:`, `md:`, `lg:`, `xl:`, `2xl:`
- Test on multiple screen sizes

## Component Guidelines

### File Organization
- One component per file
- Named exports for components
- Co-locate related components in feature directories

### Component Pattern

```typescript
'use client'; // If using hooks, state, or browser APIs

import { ComponentProps } from '@/types';

interface MyComponentProps {
  title: string;
  optional?: boolean;
}

export function MyComponent({ title, optional = false }: MyComponentProps) {
  return (
    <div className="...">
      {/* Component JSX */}
    </div>
  );
}
```

### Client vs Server Components

**Use 'use client' when:**
- Using React hooks (`useState`, `useEffect`, etc.)
- Using browser APIs (`window`, `localStorage`, etc.)
- Adding event handlers (`onClick`, `onChange`, etc.)
- Using client-side libraries (animation, 3D graphics, etc.)

**Server components (default) when:**
- Fetching data (use async/await)
- Rendering static content
- No interactivity needed

### Forms

Use React Hook Form + Zod for all forms:

```typescript
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';

const schema = z.object({
  title: z.string().min(1, 'Required'),
});

const { register, handleSubmit, formState: { errors } } = useForm({
  resolver: zodResolver(schema),
});
```

## State Management

### Current Approach
- **Server State**: Fetched via services, managed in components
- **Client State**: React `useState` and `useEffect`
- **URL State**: Next.js routing and search params

### Future Considerations
- Consider React Query/TanStack Query for server state caching
- Consider Zustand or Context API for global client state

## Common Development Tasks

### Adding a New Page

1. Create page component in `app/` directory:
```typescript
// app/my-page/page.tsx
export default function MyPage() {
  return <div>My Page</div>;
}
```

2. Navigate to `/my-page`

### Adding a New API Service

1. Create service file in `services/`:
```typescript
// services/myservice.ts
import { api } from '@/lib/api';

export const getData = async () => {
  const response = await api.get('/my-endpoint');
  return response.data;
};
```

2. Use in component:
```typescript
import { getData } from '@/services/myservice';

const data = await getData();
```

### Adding a New Component

1. Create component file:
```typescript
// components/ui/my-component.tsx
export function MyComponent() {
  return <div>My Component</div>;
}
```

2. Import and use:
```typescript
import { MyComponent } from '@/components/ui/my-component';
```

### Working with the Canvas Animation

The landing page hero uses a custom canvas animation (`components/ui/canvas.tsx`).

**Important**: The `renderCanvas()` function requires the canvas element to exist in the DOM before being called. Always call it in `useEffect`:

```typescript
useEffect(() => {
  renderCanvas();
}, []);
```

## Common Issues & Solutions

### Port Already in Use

```bash
# Find and kill process on port 3000
lsof -i :3000
kill -9 <PID>

# Or let Next.js use next available port (auto-handled)
```

### Backend Connection Errors

**Issue**: API calls failing with network errors

**Solution**:
1. Ensure backend is running on `http://localhost:8000`
2. Check `.env.local` has correct `NEXT_PUBLIC_API_URL`
3. Check browser console for CORS errors
4. Verify backend Docker containers are up: `cd ../backend && docker-compose ps`

### Tailwind Styles Not Applying

**Issue**: Tailwind classes not working

**Solution**:
1. Restart dev server: `npm run dev`
2. Check `globals.css` has `@import "tailwindcss"`
3. Ensure class names are complete strings (not concatenated)

### TypeScript Errors

**Issue**: Type errors in development

**Solution**:
1. Check `tsconfig.json` paths configuration
2. Restart TypeScript server in editor
3. Run `npm run build` to see all type errors

### Canvas Animation Not Rendering

**Issue**: Canvas background not showing on hero

**Solution**:
1. Check browser console for errors
2. Ensure canvas element has `id="canvas"`
3. Verify `renderCanvas()` is called in `useEffect`
4. Check parent element has defined dimensions

### Infinite Loading on Page Load

**Issue**: Page loads but shows infinite loading spinner

**Possible causes**:
1. API calls failing (backend not running)
2. Uncaught error in component
3. Missing error boundaries
4. Infinite re-render loop

**Debug steps**:
1. Check browser console for errors
2. Check network tab for failed API calls
3. Add error logging in components
4. Use React DevTools to inspect component state

## Testing

### Manual Testing

**Test different user roles:**
```typescript
// Test as teacher
setUserEmail('teacher@clarity.com');

// Test as student
setUserEmail('student@clarity.com');

// Test as different student
setUserEmail('alice@clarity.com');
```

**Test API integration:**
1. Open browser console
2. Check network tab for API calls
3. Verify request headers include `x-user-email`
4. Check response status and data

### Future Testing Setup

Consider adding:
- **Jest**: Unit testing
- **React Testing Library**: Component testing
- **Playwright** or **Cypress**: E2E testing

## Performance Optimization

### Current Optimizations
- **Turbopack**: Fast builds and hot reload
- **Next.js Image**: Automatic image optimization (if using `next/image`)
- **Code Splitting**: Automatic route-based splitting

### Best Practices
- Use dynamic imports for heavy components
- Optimize images before upload
- Minimize client-side JavaScript
- Use React.memo for expensive renders
- Debounce API calls (search, autocomplete)

## Deployment

### Build for Production

```bash
# Create optimized production build
npm run build

# Test production build locally
npm start
```

### Environment Variables for Production

Set these in your hosting platform (Vercel, Netlify, etc.):

```env
NEXT_PUBLIC_API_URL=https://your-backend-api.com/api/v1
```

### Recommended Hosting
- **Vercel**: Official Next.js hosting (zero-config)
- **Netlify**: Alternative with good Next.js support
- **AWS Amplify**: AWS-based hosting
- **Docker**: Self-hosted with nginx

## Development Tips

1. **Use TypeScript**: Always define types for props and API responses
2. **Check Browser Console**: Errors and warnings appear here
3. **Use React DevTools**: Inspect component hierarchy and state
4. **Test Backend Connection**: Ensure backend is running before debugging frontend issues
5. **Read Error Messages**: Next.js provides helpful error overlays in development
6. **Use ESLint**: Run `npm run lint` to catch common issues
7. **Keep Components Small**: Break down large components into smaller ones
8. **Use Services Layer**: Don't put API calls directly in components
9. **Handle Loading States**: Always show loading UI during async operations
10. **Handle Error States**: Show user-friendly error messages

## Key Differences from Other Next.js Projects

1. **Tailwind CSS 4**: Uses new `@import` syntax, no separate config file
2. **React 19**: Latest React features (might have breaking changes)
3. **App Router**: Uses Next.js 13+ App Router (not Pages Router)
4. **Dev Auth**: Uses header-based auth instead of JWT (development only)
5. **Turbopack**: New bundler (faster than Webpack)

## Resources

- [Next.js Documentation](https://nextjs.org/docs)
- [React Documentation](https://react.dev)
- [Tailwind CSS v4 Documentation](https://tailwindcss.com/docs)
- [Radix UI Documentation](https://www.radix-ui.com)
- [React Hook Form Documentation](https://react-hook-form.com)
- [Zod Documentation](https://zod.dev)
- [Axios Documentation](https://axios-http.com)
