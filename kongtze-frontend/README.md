# Kongtze Frontend

AI-Powered Education Platform - Frontend Application

## Tech Stack

- **Framework:** Next.js 15+ with App Router
- **Language:** TypeScript (strict mode)
- **UI Library:** React 19+
- **Styling:** Tailwind CSS 4
- **State Management:** TanStack Query v5 + React Context
- **Forms:** React Hook Form + Zod

## Getting Started

### Install Dependencies

```bash
npm install
```

### Development Server

```bash
npm run dev
```

Opens at [http://localhost:3000](http://localhost:3000)

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
app/
├── (kid)/              # Kid interface routes (iPad-optimized)
│   ├── dashboard/
│   ├── test/
│   └── lucky-draw/
├── (parent)/           # Parent dashboard routes (laptop-optimized)
│   ├── dashboard/
│   ├── analytics/
│   └── settings/
components/
├── shared/             # Shared components
lib/
├── api-client.ts       # Backend API client
├── auth-context.tsx    # Authentication context
└── types.ts            # TypeScript types
hooks/                  # Custom React hooks
```

## Architecture

See `../_bmad-output/planning-artifacts/architecture.md` for complete architectural decisions.

See `../_bmad-output/project-context.md` for critical implementation rules.

## Learn More

- [Next.js Documentation](https://nextjs.org/docs)
- [Kongtze PRD](../_bmad-output/planning-artifacts/prd.md)
