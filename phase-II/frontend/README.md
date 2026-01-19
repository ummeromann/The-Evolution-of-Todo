# Phase-II Todo App - Frontend

This is the Next.js 16+ frontend for the Phase-II multi-user todo web application.

## Tech Stack

- **Framework:** Next.js 16+ (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS
- **Authentication:** Better Auth (JWT tokens)
- **API Client:** Fetch with custom wrapper

## Getting Started

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment Variables

Copy `.env.local.example` to `.env.local` and fill in your values:

```bash
cp .env.local.example .env.local
```

Required environment variables:
- `BETTER_AUTH_SECRET` - Secret key for Better Auth (min 32 characters)
- `BETTER_AUTH_URL` - Your app URL (e.g., http://localhost:3000)
- `DATABASE_URL` - Neon PostgreSQL connection string
- `NEXT_PUBLIC_API_URL` - FastAPI backend URL (e.g., http://localhost:8000)

### 3. Run Development Server

```bash
npm run dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser.

## Project Structure

```
frontend/
├── src/
│   ├── app/              # App Router pages and layouts
│   │   ├── layout.tsx    # Root layout
│   │   ├── page.tsx      # Home page
│   │   └── globals.css   # Global styles
│   ├── components/       # React components
│   ├── lib/             # Utility functions and API client
│   │   └── api.ts       # API client for FastAPI backend
│   └── types/           # TypeScript type definitions
│       └── index.ts     # Common types
├── public/              # Static assets
├── .env.local.example   # Environment variables template
├── next.config.ts       # Next.js configuration
├── tailwind.config.ts   # Tailwind CSS configuration
├── tsconfig.json        # TypeScript configuration
└── package.json         # Dependencies and scripts
```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm start` - Start production server
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript type checking

## Authentication Flow

1. User signs up/signs in via Better Auth
2. JWT token is issued and stored
3. Frontend includes token in `Authorization: Bearer <token>` header
4. FastAPI backend validates token and processes requests

## API Integration

The `src/lib/api.ts` file provides a typed API client for communicating with the FastAPI backend:

```typescript
import { apiClient } from '@/lib/api';

// Set token after login
apiClient.setToken(token);

// Make API calls
const todos = await apiClient.get('/api/todos');
const newTodo = await apiClient.post('/api/todos', { title: 'New task' });
```

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Better Auth Documentation](https://better-auth.com)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
