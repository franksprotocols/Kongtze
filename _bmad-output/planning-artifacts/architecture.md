---
stepsCompleted: ['step-01-init', 'step-02-context', 'step-03-starter', 'step-04-decisions', 'step-05-patterns', 'step-06-structure', 'step-07-validation', 'complete']
inputDocuments: 
  - '_bmad-output/planning-artifacts/prd.md'
  - '_bmad/_memory/project-vision-and-requirements.md'
workflowType: 'architecture'
project_name: 'Kongtze'
user_name: 'Frankhu'
date: '2026-01-21'
prdCount: 1
uxCount: 0
researchCount: 0
projectDocsCount: 0
memoryDocsCount: 1
---

# Architecture Decision Document - Kongtze

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

**Project:** Kongtze  
**Author:** Frankhu  
**Date:** 2026-01-21  
**Type:** Education Technology - AI-Powered Study Platform  
**Context:** Greenfield Project

---

## Project Context Analysis

### Requirements Overview

**Functional Requirements Summary:**

Kongtze has **96 functional requirements** organized into 9 major feature categories:

1. **Study Calendar Planning (7 FRs)** - Weekly scheduling with 2-3 sessions/day, parent customization
2. **Subject Management (5 FRs)** - Math, English, Chinese, Science with extensible architecture
3. **Homework Upload & OCR (7 FRs)** - Photo upload, digitization, parent review/correction
4. **Class Notes Upload & Curriculum Tracking (15 FRs)** - Daily notes upload, topic extraction, curriculum-aware test generation
5. **Extra Practice Test Generation (6 FRs)** - AI-generated tests based on difficulty and class notes context
6. **AI-Powered Difficulty Adjustment (7 FRs)** - Dynamic scaling: Beginner → Intermediate → Advanced → Expert
7. **Time Limits per Question (7 FRs)** - AI-calculated based on difficulty + student performance history
8. **Test Results & Reporting (7 FRs)** - Comprehensive breakdowns, accuracy tracking, historical trends
9. **AI Explanations (7 FRs)** - Step-by-step, age-appropriate (10-year-old), multilingual

**Gamification System (17 FRs):**
- Scoring: Points per question, speed bonuses, perfect test rewards
- Rewards: Daily/weekly tracking, milestone celebrations
- Lucky Draw: Blind box animations, gift inventory, parent-configurable catalog

**Parent Dashboard (11 FRs):**
- Daily overview, weekly performance graphs, subject breakdowns, calendar management, class notes viewer, settings

**Non-Functional Requirements:**

**Performance:**
- Page load: <2 seconds (4G connection)
- Test submission: <1 second response
- AI explanation generation: <5 seconds
- OCR processing: <30 seconds per photo

**Security (Simplified for Family Use):**
- HTTPS encryption for all data transmission
- Student PIN (4-digit) for kid interface
- Parent password authentication (no 2FA needed)
- Encrypted photo storage for homework/notes
- **Note:** No GDPR/COPPA compliance required - private family app

**Usability:**
- Kid interface: Large buttons (min 60px), bright colors, minimal text, font ≥16px
- Mobile-responsive design for iPad (primary) and laptop (secondary)
- WCAG 2.1 AA accessibility compliance
- Celebration animations for engagement

**Reliability:**
- 99.5% uptime during study hours (7am-9pm Singapore Time)
- Daily automated backups
- Graceful degradation if AI services unavailable

**Scalability:**
- **Single-user system** - optimized for one student (Year 5, Dulwich College)
- Architecture allows future multi-user expansion but NOT required for v1.0

### Scale & Complexity

**Project Classification:**
- **Complexity Level:** Medium-High
- **Project Type:** Progressive Web App (PWA)
- **Domain:** Education Technology (EdTech)
- **Context:** Greenfield project (built from scratch)
- **Deployment Scope:** Single-user private family application

**Primary Technical Domain:** Full-stack web application with AI/ML integration

**Estimated Architectural Components:** 11-14 major components

**Frontend Repository (Next.js/TypeScript):**
1. Kid Interface (React components, iPad-optimized)
2. Parent Dashboard (React components, laptop-optimized)
3. Shared UI Components
4. Client-side routing and state management

**Backend Repository (Python/FastAPI):**
5. REST API Server (FastAPI)
6. PostgreSQL Database (includes caching tables)
7. Google Gemini AI Service Integration
8. Google Cloud Vision OCR Pipeline
9. Railway File Storage (photos)
10. Authentication Service (JWT tokens)
11. Gamification Engine
12. Difficulty Adjustment Algorithm
13. Analytics & Performance Tracking
14. Session Scheduler & Reminders
15. Test Generation Service
16. Real-time Features (WebSocket for timers, live scoring)

### Technical Constraints & Dependencies

**External Service Dependencies:**
- **Google Gemini API** - Question generation, explanations, class notes analysis, custom question creation
- **Google Cloud Vision API** - OCR for homework and class notes photos, handwriting recognition
- **Railway** - Hosting platform, file storage for photos
- **Email service** (optional) - Parent notifications, weekly summaries

**Technical Dependencies:**

**Frontend:**
- Node.js ≥18.0.0 runtime
- Next.js 15+ with TypeScript
- React 19+
- Tailwind CSS 4

**Backend:**
- Python ≥3.11
- FastAPI framework
- SQLAlchemy 2.0 + Alembic (migrations)
- Pydantic V2 (data validation)
- PostgreSQL database (Railway addon) - includes data storage and caching
- Google Gemini Python SDK
- Google Cloud Vision Python SDK

**Deployment:**
- Railway platform (frontend + backend + PostgreSQL)
- No Redis needed - single-user system uses PostgreSQL for caching

**Educational Context Constraints:**
- **IB Curriculum Alignment** - Dulwich College Singapore uses International Baccalaureate Primary Years Programme (PYP)
- **NOT PSLE-aligned** - Singapore national curriculum not applicable
- **IB PYP Framework Requirements:**
  - Transdisciplinary themes and inquiry-based learning
  - Math AA group = advanced/accelerated mathematics track
  - Chinese as additional language (IB Language A or B)
  - Question content must reflect IB assessment approaches (formative, summative, conceptual understanding)

**Student Profile Constraints:**
- Age: 10 years old (Year 5)
- Attention span: 30-minute session maximum
- Academic challenges: Math AA struggling, Chinese writing weak, English average
- Single student - no multi-user complexity needed

**Device Constraints:**
- **Primary device: iPad** (main usage for student interface)
- **Secondary device: Laptop** (primarily for parent dashboard)
- Touch-optimized for iPad, mouse/keyboard optimized for laptop
- Responsive breakpoints: iPad (768px-1024px) and laptop (1024px+)

**Deployment Constraints:**
- Railway platform hosting
- Singapore timezone (SGT/UTC+8)
- Study hours: 7am-9pm SGT (uptime window)

**Budget Optimization:**
- Cache AI explanations to reduce Gemini API costs
- Optimize image storage (compression)
- Railway's cost-effective hosting tier

### Cross-Cutting Concerns Identified

These architectural concerns affect multiple components and require coordinated design:

1. **AI/ML Integration (Google Gemini)**
   - Question generation from class notes context
   - Difficulty level recommendations
   - Step-by-step explanations (age-appropriate)
   - Curriculum topic extraction from photos
   - Custom question creation when question bank doesn't match
   - Multimodal processing (text + images)

2. **OCR & Image Processing (Google Cloud Vision)**
   - Homework photo text extraction
   - Class notes digitization and topic identification
   - Handwriting recognition (Chinese characters, student answers)
   - Multi-page document handling
   - Error correction workflow (parent review)

3. **File Storage (Railway)**
   - Homework photo uploads (JPEG, PNG, HEIC)
   - Class notes photo storage
   - Original photo retention alongside digitized content
   - Image optimization and compression
   - Secure access control
   - Integration with Railway's file storage system

4. **Caching Strategy (PostgreSQL)**
   - AI explanation caching using database table (reduce Gemini API costs)
   - Session data stored in PostgreSQL or JWT tokens
   - Difficulty adjustment cached in database
   - No Redis needed - single-user system doesn't require separate cache layer
   - Simple cache invalidation strategies (TTL-based, size-based)

5. **Authentication & Authorization**
   - Dual-tier access: Student PIN (4-digit) + Parent password
   - Simple session management (single-user, no complex roles)
   - No 2FA required (simplified for family use)
   - No user registration/invitation flows needed

6. **Real-time Features**
   - Countdown timers per question (WebSocket or Server-Sent Events)
   - Live scoring display during tests
   - Instant feedback animations
   - Session reminders (5 minutes before start)

7. **Performance Optimization**
   - Frontend: Code splitting, lazy loading, image optimization
   - Backend: Database query optimization, connection pooling
   - CDN for static assets (Railway's built-in CDN)
   - Mobile-first responsive design for iPad primary use

8. **Error Handling & Resilience**
   - Graceful degradation when Gemini API unavailable
   - OCR error handling with parent correction workflow
   - Network timeout handling for student experience
   - Retry logic for failed API calls

9. **Device Responsiveness**
   - **iPad-first design** (primary device for student interface)
   - **Laptop-optimized** parent dashboard (secondary device)
   - Touch-friendly UI (60px minimum button size for iPad)
   - Responsive breakpoints for both device types
   - Offline capability for interrupted sessions (future consideration)

10. **Analytics & Performance Tracking**
    - Student performance per subject/topic
    - Difficulty progression history
    - Time analytics (avg per question, time pressure indicators)
    - Test completion rates, streak tracking
    - Parent dashboard data aggregation

11. **Multilingual Support**
    - English, Chinese language questions
    - Subject-specific input types (Chinese character writing, math equations)
    - Explanation language matching question language
    - IB PYP multilingual framework alignment

12. **Gamification State Management**
    - Reward points balance tracking
    - Gift inventory persistence
    - Lucky draw probability engine
    - Milestone detection and celebration triggers

---

## Starter Template Evaluation

### Primary Technology Domain

**Full-stack Progressive Web Application (PWA)** with dual interfaces:
- Kid-friendly testing interface (iPad-optimized)
- Professional parent dashboard (laptop-optimized)

### Architecture Approach

**Separate Frontend & Backend Repositories**

This project uses a **decoupled architecture** with two independent repositories:

1. **Frontend Repository** - Next.js/TypeScript (handles UI/UX for both kid and parent interfaces)
2. **Backend Repository** - Python/FastAPI (handles business logic, AI, database, file storage)

**Communication:** REST API over HTTPS

**Rationale for Separation:**
- **Independent deployment** - Deploy frontend and backend separately on Railway
- **Clear separation of concerns** - UI logic vs business logic
- **Technology optimization** - Python excels at AI/ML, TypeScript excels at modern web UI
- **Development workflow** - Can work on frontend/backend independently
- **Scalability** - Different scaling strategies if needed in future

### Technology Stack Selected

**Frontend Stack:**
- **Runtime:** Node.js ≥18.0.0
- **Framework:** Next.js 15+ with App Router
- **Language:** TypeScript
- **Styling:** Tailwind CSS 4
- **UI Library:** React 19+
- **Platform:** Railway (static hosting or Node.js service)

**Backend Stack:**
- **Runtime:** Python ≥3.11
- **Framework:** FastAPI (async web framework)
- **ORM:** SQLAlchemy 2.0 + Alembic (migrations)
- **Validation:** Pydantic V2
- **Database:** PostgreSQL (Railway addon)
- **Caching:** PostgreSQL tables (no Redis needed)
- **Platform:** Railway (Python service)

**Shared Infrastructure:**
- **Database:** Railway PostgreSQL addon (shared by backend)
- **File Storage:** Railway file storage system
- **AI Services:** Google Gemini API, Google Cloud Vision API

---

## Frontend: Next.js Starter

### Starter Options Considered

1. ✅ **Official create-next-app (Selected)** - Clean foundation with recommended defaults
2. ❌ Next.js Boilerplate by ixartz - Too many pre-configured features we don't need
3. ❌ Vercel's templates - Over-engineered for single-user app

### Selected Starter: create-next-app (Official Next.js CLI)

**Rationale for Selection:**

The official Next.js starter with recommended defaults provides optimal foundation for Kongtze frontend:

1. **Modern Best Practices** - App Router, Turbopack, TypeScript, Tailwind CSS
2. **Clean Architecture** - No opinionated extras; build exactly what we need
3. **Railway Compatible** - Deploys seamlessly to Railway
4. **Well-Documented** - Official Next.js docs cover everything
5. **Flexible** - Easy to add kid-friendly components, parent dashboard, API client
6. **Performance** - Built-in optimizations for images, fonts, code splitting
7. **iPad-First** - Responsive design utilities perfect for our primary device

**Repository Name:** `kongtze-frontend`

**Initialization Command:**

```bash
npx create-next-app@latest kongtze-frontend
```

**Interactive Setup (Recommended):**
```
√ Would you like to use TypeScript? ... Yes
√ Would you like to use ESLint? ... Yes
√ Would you like to use Tailwind CSS? ... Yes
√ Would you like your code inside a `src/` directory? ... No
√ Would you like to use App Router? (recommended) ... Yes
√ Would you like to use Turbopack for `next dev`? ... Yes
√ Would you like to customize the import alias (@/*)? ... No
```

**Alternative (Non-Interactive):**
```bash
npx create-next-app@latest kongtze-frontend \
  --typescript \
  --tailwind \
  --eslint \
  --app \
  --turbopack \
  --import-alias "@/*" \
  --no-src-dir
```

---

### Frontend Architectural Decisions Provided by Starter

**Language & Runtime:**
- TypeScript with strict mode enabled
- Modern ES modules (ESM)
- Node.js ≥18.0.0 requirement
- Type safety across components and API calls

**Framework & Routing:**
- Next.js 15+ with App Router (file-based routing)
- React Server Components for performance
- Client Components for interactivity (animations, timers, games)
- Automatic code splitting per route
- Built-in API route handlers (optional, we use separate backend)

**Styling Solution:**
- Tailwind CSS 4 (utility-first CSS framework)
- Perfect for rapid UI development
- Kid-friendly design utilities (colors, animations, responsive)
- JIT compiler for optimized builds
- Custom theme configuration for bright, playful interface
- Dark mode support (future consideration)

**Build Tooling:**
- Turbopack for fast development builds
- Next.js compiler for production optimization
- Automatic image optimization (`next/image`)
- Font optimization (`next/font`)
- Tree shaking and code splitting
- Static asset optimization

**Code Organization:**
```
kongtze-frontend/
├── app/
│   ├── layout.tsx              # Root layout
│   ├── page.tsx                # Home/landing page
│   ├── globals.css             # Global styles + Tailwind
│   ├── (kid)/                  # Kid interface routes
│   │   ├── dashboard/
│   │   ├── test/
│   │   ├── results/
│   │   └── lucky-draw/
│   └── (parent)/               # Parent dashboard routes
│       ├── dashboard/
│       ├── calendar/
│       ├── analytics/
│       └── settings/
├── components/
│   ├── kid/                    # Kid-specific components
│   ├── parent/                 # Parent-specific components
│   └── shared/                 # Shared components
├── lib/
│   ├── api-client.ts           # Backend API client
│   ├── types.ts                # TypeScript types
│   └── utils.ts                # Utility functions
├── public/                     # Static assets
├── tailwind.config.ts          # Tailwind customization
├── next.config.ts              # Next.js configuration
├── tsconfig.json               # TypeScript config
└── package.json
```

**Development Experience:**
- Hot Module Replacement (HMR) with Turbopack
- Fast Refresh for instant feedback
- TypeScript IntelliSense
- ESLint integration
- Automatic port detection (default: 3000)
- Clear error overlays

**Environment Configuration:**
```bash
# .env.local
NEXT_PUBLIC_API_URL=https://kongtze-backend.railway.app
```

**Additional Setup Required:**
1. API client library (axios or fetch wrapper)
2. Authentication state management (JWT storage)
3. Kid-friendly component library (buttons, timers, animations)
4. Parent dashboard charts (recharts or similar)
5. Form handling (React Hook Form)
6. Deployment config for Railway

---

## Backend: FastAPI Starter

### Starter Options Considered

1. ❌ **Official Full Stack FastAPI Template** - Includes React frontend we don't need
2. ✅ **Minimal FastAPI PostgreSQL Template (Selected)** - Lean, modern, production-ready
3. ❌ **Custom from scratch** - Too time-consuming, reinventing the wheel

### Selected Starter: Minimal FastAPI PostgreSQL Template

[minimal-fastapi-postgres-template](https://github.com/rafsaf/minimal-fastapi-postgres-template)

**Rationale for Selection:**

1. **Modern SQLAlchemy 2.0** - Uses latest `mapped_column` and `Mapped` patterns
2. **Production-Ready** - Alembic migrations, proper project structure
3. **Minimal & Clean** - No unnecessary features to remove
4. **PostgreSQL Native** - Built specifically for PostgreSQL
5. **Well-Structured** - Domain-based organization ready for Kongtze modules
6. **Python Best Practices** - Type hints, async/await, Pydantic V2

**Repository Name:** `kongtze-backend`

**Initialization Approach:**

**Option 1: Clone and Adapt (Recommended)**
```bash
git clone https://github.com/rafsaf/minimal-fastapi-postgres-template kongtze-backend
cd kongtze-backend
rm -rf .git
git init
# Clean up template-specific files and adapt to Kongtze
```

**Option 2: Manual Setup Following Best Practices**
Create directory structure manually:
```bash
mkdir kongtze-backend
cd kongtze-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

Create `requirements.txt`:
```txt
fastapi[standard]>=0.115.0
sqlalchemy>=2.0.35
alembic>=1.13.3
psycopg2-binary>=2.9.10
pydantic>=2.9.2
pydantic-settings>=2.6.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.9
google-generativeai>=0.8.3
google-cloud-vision>=3.8.0
pillow>=10.4.0
uvicorn[standard]>=0.32.0
```

---

### Backend Architectural Decisions

**Project Structure (Domain-Based):**
```
kongtze-backend/
├── app/
│   ├── main.py                 # FastAPI app entry point
│   ├── core/
│   │   ├── config.py           # Settings (Pydantic Settings)
│   │   ├── security.py         # Auth (JWT, password hashing)
│   │   └── database.py         # DB connection, session
│   ├── models/                 # SQLAlchemy models
│   │   ├── user.py
│   │   ├── subject.py
│   │   ├── test.py
│   │   ├── question.py
│   │   ├── result.py
│   │   ├── reward.py
│   │   └── cached_explanation.py
│   ├── schemas/                # Pydantic schemas
│   │   ├── user.py
│   │   ├── test.py
│   │   ├── question.py
│   │   └── ...
│   ├── api/
│   │   └── routes/             # API endpoints
│   │       ├── auth.py
│   │       ├── calendar.py
│   │       ├── tests.py
│   │       ├── homework.py
│   │       ├── notes.py
│   │       ├── ai.py
│   │       ├── rewards.py
│   │       └── dashboard.py
│   ├── services/               # Business logic
│   │   ├── gemini_service.py
│   │   ├── vision_service.py
│   │   ├── test_generation.py
│   │   ├── difficulty_adjustment.py
│   │   ├── gamification.py
│   │   └── analytics.py
│   └── dependencies.py         # Dependency injection
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── tests/                      # Pytest tests
├── .env                        # Environment variables
├── alembic.ini                 # Alembic configuration
├── requirements.txt
└── README.md
```

**Language & Framework:**
- Python ≥3.11 with type hints
- FastAPI for async REST API
- Uvicorn ASGI server
- Async/await patterns throughout

**Database & ORM:**
- SQLAlchemy 2.0 with modern `Mapped` syntax
- Alembic for database migrations
- PostgreSQL as primary database
- Connection pooling for performance
- Async database operations

**Data Validation:**
- Pydantic V2 for request/response schemas
- Automatic API documentation (OpenAPI/Swagger)
- Type-safe data validation
- Custom validators for business rules

**Authentication:**
- JWT tokens for stateless auth
- Parent password + Student PIN
- Password hashing with bcrypt
- Token expiration and refresh (optional)

**AI Integration:**
- Google Gemini Python SDK (`google-generativeai`)
- Google Cloud Vision Python SDK (`google-cloud-vision`)
- Async API calls to avoid blocking
- Error handling and retry logic
- Response caching in PostgreSQL

**File Handling:**
- Python Pillow for image processing
- Railway file storage integration
- Image compression before storage
- Multi-part form data handling

**Environment Configuration:**
```bash
# .env
DATABASE_URL=postgresql://user:pass@railway-postgres:5432/kongtze
SECRET_KEY=your-secret-key-here
GEMINI_API_KEY=your-gemini-api-key
GOOGLE_CLOUD_VISION_CREDENTIALS=path/to/credentials.json
RAILWAY_STORAGE_PATH=/app/storage
CORS_ORIGINS=https://kongtze-frontend.railway.app
```

**API Documentation:**
- Automatic OpenAPI schema generation
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- Request/response examples

**Testing:**
- Pytest for unit and integration tests
- Test database setup/teardown
- API endpoint testing
- Mock external services (Gemini, Vision)

**Development Tools:**
- Black for code formatting
- Ruff for linting
- MyPy for type checking
- Pre-commit hooks

---

## Deployment Architecture

**Two Separate Railway Services:**

1. **Frontend Service** (`kongtze-frontend`)
   - Type: Node.js or Static site
   - Port: 3000 (or Railway auto-assigned)
   - Environment: `NEXT_PUBLIC_API_URL`
   - Build: `npm run build`
   - Start: `npm start`

2. **Backend Service** (`kongtze-backend`)
   - Type: Python
   - Port: 8000 (or Railway auto-assigned)
   - Environment: Database URL, API keys, CORS origins
   - Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **PostgreSQL Database** (Railway Addon)
   - Attached to backend service
   - Automatic connection URL injection
   - Daily backups

**Communication Flow:**
```
User (iPad/Laptop)
    ↓
Frontend (Next.js on Railway)
    ↓ HTTPS REST API
Backend (FastAPI on Railway)
    ↓
PostgreSQL (Railway Addon)
    ↓
Google Gemini API / Cloud Vision API
```

**CORS Configuration:**
Backend must allow frontend origin:
```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://kongtze-frontend.railway.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

## Implementation Notes

**Project Initialization Steps:**

1. **Initialize Frontend:**
   ```bash
   npx create-next-app@latest kongtze-frontend
   cd kongtze-frontend
   npm install axios  # Or fetch wrapper
   # Create folder structure, API client
   git init && git add . && git commit -m "Initial Next.js setup"
   ```

2. **Initialize Backend:**
   ```bash
   git clone https://github.com/rafsaf/minimal-fastapi-postgres-template kongtze-backend
   cd kongtze-backend
   rm -rf .git
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   # Adapt structure to Kongtze domains
   git init && git add . && git commit -m "Initial FastAPI setup"
   ```

3. **Setup Railway:**
   - Create Railway project
   - Add PostgreSQL addon
   - Deploy backend service (connects to PostgreSQL)
   - Deploy frontend service (env var points to backend)

**Note:** These initialization commands should be the **first implementation stories** in Sprint Planning.

---

**References & Sources:**
- [Next.js Installation Guide](https://nextjs.org/docs/app/getting-started/installation)
- [Next.js CLI Reference](https://nextjs.org/docs/app/api-reference/cli/create-next-app)
- [Minimal FastAPI PostgreSQL Template](https://github.com/rafsaf/minimal-fastapi-postgres-template)
- [FastAPI Best Practices](https://github.com/zhanymkanov/fastapi-best-practices)
- [FastAPI Project Structure Guide](https://dev.to/mohammad222pr/structuring-a-fastapi-project-best-practices-53l6)
- [How to Structure Scalable FastAPI](https://fastlaunchapi.dev/blog/how-to-structure-fastapi)
- [Tailwind CSS with Next.js](https://tailwindcss.com/docs/guides/nextjs)

---

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- Database ORM approach (Code-First SQLAlchemy with Alembic)
- Async vs sync database operations (Async SQLAlchemy)
- Authentication mechanism (JWT stateless tokens)
- API documentation strategy (Auto-generated OpenAPI)
- Environment configuration (Railway + .env files)
- Database migrations strategy (Alembic auto-generate + manual review)

**Important Decisions (Shape Architecture):**
- Caching strategy (PostgreSQL cache table)
- Password hashing algorithm (bcrypt via passlib)
- Error handling standards (HTTP status codes + JSON)
- File upload handling (Multipart form data)
- Frontend state management (React Context + TanStack Query)
- Form handling (React Hook Form)
- Timer implementation (Client-side with server validation)

**Deferred Decisions (Post-MVP):**
- Advanced monitoring/observability tools (can use Railway built-in initially)
- Advanced rate limiting (single-user app doesn't require it immediately)
- CDN for static assets (Railway edge network sufficient for MVP)

---

### Data Architecture

**Decision 1.1: Database Design Approach**
- **Choice:** Code-First using SQLAlchemy 2.0+ models with Alembic migrations
- **Version:** SQLAlchemy 2.0+, Alembic latest stable
- **Rationale:** Define database schema in Python code, auto-generate migrations, maintain single source of truth in code
- **Affects:** All backend data models, database schema evolution
- **Alternative Considered:** Schema-first (SQL DDL) - rejected due to Python-centric stack

**Decision 1.2: Database Operations Pattern**
- **Choice:** Async SQLAlchemy with async session management
- **Version:** SQLAlchemy 2.0+ (async support), asyncpg driver
- **Rationale:** Non-blocking I/O for AI API calls, OCR processing, and database operations; better performance for I/O-heavy workloads
- **Affects:** All database queries, API route handlers, service layer
- **Alternative Considered:** Sync SQLAlchemy - rejected due to AI/OCR I/O bottlenecks

**Decision 1.3: AI Explanation Caching**
- **Choice:** Separate `cached_explanations` table with question hash as key
- **Version:** PostgreSQL built-in (no Redis)
- **Rationale:** Single-user app doesn't need separate cache layer; reduce Gemini API costs by caching identical questions
- **Schema:**
  ```python
  class CachedExplanation(Base):
      question_hash: str (PK)
      ai_explanation: text
      created_at: timestamp
      hit_count: int
  ```
- **Affects:** Test generation service, AI service layer
- **Alternative Considered:** Redis cache - rejected as over-engineering for single user

---

### Authentication & Security

**Decision 2.1: Authentication Mechanism**
- **Choice:** JWT-based stateless authentication
- **Version:** PyJWT latest stable, HS256 algorithm
- **Rationale:** Stateless tokens (no session storage needed), simple for single-user family app, works well with separate frontend/backend
- **Token Contents:** user_id, exp (expiration), iat (issued at)
- **Storage:** Frontend stores in httpOnly cookies or localStorage
- **Affects:** Login flow, API authentication middleware, all protected routes
- **Alternative Considered:** Session-based auth - rejected due to unnecessary complexity

**Decision 2.2: Password Hashing**
- **Choice:** bcrypt via passlib with cost factor 12
- **Version:** passlib latest stable, bcrypt backend
- **Rationale:** Industry-standard password hashing, proven security, built-in salt generation
- **Configuration:** Cost factor 12 (balanced security/performance)
- **Affects:** User registration, password change, authentication verification
- **Alternative Considered:** Argon2 - rejected as bcrypt is simpler and sufficient for single-user

---

### API & Communication Patterns

**Decision 3.1: API Documentation**
- **Choice:** FastAPI auto-generated OpenAPI/Swagger UI at `/docs`
- **Version:** FastAPI built-in, OpenAPI 3.0+
- **Rationale:** Zero-config interactive API docs, automatic from Pydantic schemas, excellent DX
- **Access:** Available at `/docs` (Swagger UI) and `/redoc` (ReDoc)
- **Affects:** All API endpoints, developer experience, frontend integration
- **Alternative Considered:** Manual OpenAPI - rejected as FastAPI provides it for free

**Decision 3.2: Error Handling Standards**
- **Choice:** RESTful HTTP status codes + consistent JSON error responses
- **Format:**
  ```json
  {
    "detail": "Error message",
    "error_code": "VALIDATION_ERROR",
    "timestamp": "2026-01-21T10:30:00Z"
  }
  ```
- **Status Codes:**
  - 200: Success
  - 400: Validation error
  - 401: Unauthorized
  - 404: Not found
  - 500: Server error
- **Affects:** All API responses, frontend error handling
- **Alternative Considered:** GraphQL-style errors - rejected due to REST API choice

**Decision 3.3: File Upload Handling**
- **Choice:** Multipart form data with FastAPI's `UploadFile`
- **Format:** `multipart/form-data` for homework/notes photos
- **File Types:** JPEG, PNG, HEIC (converted server-side if needed)
- **Max Size:** 10MB per photo (configurable)
- **Storage:** Railway persistent disk, file paths in PostgreSQL
- **Affects:** Homework upload, class notes upload, Google Cloud Vision integration
- **Alternative Considered:** Base64 JSON - rejected due to size overhead

---

### Frontend Architecture

**Decision 4.1: State Management**
- **Choice:** React Context for global state + TanStack Query for server state
- **Version:** React 19+ Context API, TanStack Query v5
- **Rationale:**
  - React Context: Simple global state (user auth, theme, app settings)
  - TanStack Query: Server state caching, automatic refetching, optimistic updates
  - No Redux needed for single-user app
- **State Categories:**
  - Auth context: Current user, login status
  - TanStack Query: API data (calendar, tests, scores, notes)
- **Affects:** All React components, API integration, data synchronization
- **Alternative Considered:** Redux - rejected as over-engineering

**Decision 4.2: Form Handling**
- **Choice:** React Hook Form with Zod validation
- **Version:** React Hook Form v7+, Zod v3+
- **Rationale:** Minimal re-renders, built-in validation, excellent TypeScript support
- **Forms:**
  - Login/password change
  - Study session preferences
  - Photo uploads (homework/notes)
  - Manual test adjustments (parent dashboard)
- **Affects:** All user input forms, validation logic
- **Alternative Considered:** Formik - rejected in favor of better performance

**Decision 4.3: Test Timer Implementation**
- **Choice:** Client-side JavaScript timers with server-side validation
- **Approach:**
  - Frontend: `setInterval` countdown display
  - Backend: Record start_time, validate on submission (elapsed < time_limit)
  - Auto-submit: Frontend sends test when timer expires
- **Rationale:** Simple for single-user, no cheating concern (family app), reduces server load
- **Affects:** Test-taking interface, test submission validation
- **Alternative Considered:** WebSocket timers - rejected as unnecessary for single user

---

### Infrastructure & Deployment

**Decision 5.1: Configuration Management**
- **Choice:** `.env` files for local + Railway dashboard for production
- **Pattern:**
  - `.env.example` in repo (template with dummy values)
  - `.env` in gitignore (local development secrets)
  - Railway dashboard: Production environment variables
- **Variables:**
  - `DATABASE_URL` (Railway PostgreSQL addon)
  - `GEMINI_API_KEY` (Google AI)
  - `GOOGLE_CLOUD_VISION_KEY` (OCR)
  - `JWT_SECRET_KEY`
  - `RAILWAY_STATIC_URL` (file storage)
- **Affects:** All services requiring configuration, deployment process
- **Alternative Considered:** HashiCorp Vault - rejected as over-engineering

**Decision 5.2: Database Migrations Strategy**
- **Choice:** Alembic auto-generate migrations + manual review before applying
- **Version:** Alembic latest stable
- **Workflow:**
  1. Change SQLAlchemy models
  2. Run `alembic revision --autogenerate -m "description"`
  3. **Review generated migration** (catch edge cases)
  4. Run `alembic upgrade head` to apply
  5. Railway: Auto-run migrations on deploy
- **Rationale:** Alembic generates 95% of migration code, manual review catches issues, safe for production
- **Affects:** Database schema changes, deployment pipeline
- **Alternative Considered:** Manual migrations - rejected as too time-consuming

---

### Decision Impact Analysis

**Implementation Sequence:**

1. **Phase 1 - Foundation** (Day 1-2):
   - Set up PostgreSQL with SQLAlchemy async models
   - Configure Alembic migrations
   - Implement JWT authentication with bcrypt

2. **Phase 2 - Core Services** (Day 3-5):
   - FastAPI routes with OpenAPI docs
   - File upload handling (multipart form data)
   - Google Cloud Vision integration
   - Gemini AI integration with cache table

3. **Phase 3 - Frontend Foundation** (Day 6-8):
   - React Context + TanStack Query setup
   - React Hook Form configuration
   - Authentication flow (login/logout)

4. **Phase 4 - Feature Implementation** (Day 9+):
   - Study calendar (client-side timers)
   - Homework photo upload
   - Class notes photo upload
   - Test generation with caching
   - Gamification (scoring, rewards)
   - Parent dashboard

**Cross-Component Dependencies:**

1. **Authentication affects everything:**
   - JWT tokens required for all protected API routes
   - Frontend auth context gates kid/parent interfaces
   - bcrypt hashing used in login validation

2. **Database architecture drives service layer:**
   - Async SQLAlchemy requires async FastAPI route handlers
   - Code-First models generate database schema
   - Alembic migrations track schema evolution

3. **File uploads enable AI features:**
   - Multipart form data → Google Cloud Vision OCR → Gemini AI
   - Cached explanations table reduces API costs
   - Railway file storage persists uploaded photos

4. **Frontend state connects to backend:**
   - TanStack Query hooks call FastAPI endpoints
   - React Hook Form submits to multipart endpoints
   - Client-side timers validated server-side on test submission

5. **Railway deployment integrates all pieces:**
   - `.env` variables configure all services
   - PostgreSQL addon shared by both repos
   - Alembic migrations run automatically on backend deploy

---

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 24 areas where AI agents could make different choices without clear patterns

**Purpose:** These patterns ensure that multiple AI agents (or the same agent in different sessions) write compatible, consistent code that works together seamlessly across the Kongtze frontend and backend.

---

### Naming Patterns

#### Database Naming Conventions

**All database elements use snake_case (PostgreSQL/Python convention):**

- **Table names:** Lowercase, plural, snake_case
  - ✅ `users`, `test_results`, `cached_explanations`, `class_notes`
  - ❌ `Users`, `TestResults`, `test-results`

- **Column names:** Lowercase, snake_case
  - ✅ `user_id`, `created_at`, `test_score`, `ai_explanation`
  - ❌ `userId`, `createdAt`, `testScore`

- **Foreign keys:** `{table_singular}_id` format
  - ✅ `user_id`, `test_id`, `subject_id`
  - ❌ `fk_user`, `userID`, `user_ref`

- **Indexes:** `idx_{table}_{column(s)}` format
  - ✅ `idx_users_email`, `idx_test_results_user_id_created_at`
  - ❌ `users_email_index`, `test_results_idx`

- **SQLAlchemy Models:** PascalCase class, snake_case fields
  ```python
  class TestResult(Base):
      __tablename__ = "test_results"
      test_id: Mapped[int] = mapped_column(primary_key=True)
      user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))
      created_at: Mapped[datetime] = mapped_column(default=func.now())
  ```

#### API Naming Conventions

**REST endpoints use plural resource names:**

- **Resource paths:** Lowercase, plural, kebab-case for multi-word
  - ✅ `/api/users/{id}`, `/api/test-results`, `/api/class-notes`
  - ❌ `/api/user/{id}`, `/api/testResults`, `/api/class_notes`

- **Path parameters:** `{id}` format (FastAPI style)
  - ✅ `/api/users/{user_id}`, `/api/tests/{test_id}/submit`
  - ❌ `/api/users/:id`, `/api/users/<int:id>`

- **Query parameters:** snake_case
  - ✅ `?subject_id=1&difficulty_level=2&page=1`
  - ❌ `?subjectId=1&difficultyLevel=2`

- **JSON field names:** snake_case (backend owns naming)
  - ✅ `{"user_id": 1, "created_at": "2026-01-21T10:30:00Z"}`
  - ❌ `{"userId": 1, "createdAt": "..."}`

- **HTTP headers:** Standard capitalization
  - ✅ `Authorization: Bearer <token>`, `Content-Type: application/json`
  - ❌ `authorization`, `content-type`

**API Versioning:** No versioning initially (single-user app), add `/api/v2/` prefix if breaking changes needed

#### Code Naming Conventions

**Frontend (TypeScript/React):**

- **React Components:** PascalCase
  - ✅ `UserCard.tsx`, `TestTimer.tsx`, `LuckyDrawBox.tsx`
  - ❌ `userCard.tsx`, `test-timer.tsx`, `User_Card.tsx`

- **Component instances:** camelCase
  - ✅ `<UserCard />`, `<TestTimer />`
  
- **Utility files:** kebab-case
  - ✅ `api-client.ts`, `format-date.ts`, `auth-utils.ts`
  - ❌ `apiClient.ts`, `formatDate.ts`, `authUtils.ts`

- **TypeScript interfaces/types:** PascalCase, prefixed with `I` for interfaces (optional)
  - ✅ `interface User`, `type TestResult`, `interface IApiResponse`
  - ❌ `interface user`, `type testResult`

- **Variables/functions:** camelCase
  - ✅ `const userId = 1;`, `function getUserData() {...}`
  - ❌ `const user_id`, `function get_user_data()`

- **Constants:** UPPER_SNAKE_CASE
  - ✅ `const API_BASE_URL`, `const MAX_UPLOAD_SIZE`
  - ❌ `const apiBaseUrl`, `const maxUploadSize`

**Backend (Python/FastAPI):**

- **Python modules/files:** snake_case
  - ✅ `gemini_service.py`, `test_generation.py`, `difficulty_adjustment.py`
  - ❌ `geminiService.py`, `TestGeneration.py`

- **Classes:** PascalCase
  - ✅ `class User`, `class TestResult`, `class GeminiService`
  - ❌ `class user`, `class test_result`

- **Functions/methods:** snake_case
  - ✅ `def get_user_data()`, `async def generate_test()`
  - ❌ `def getUserData()`, `def GenerateTest()`

- **Variables:** snake_case
  - ✅ `user_id = 1`, `test_score = 85`
  - ❌ `userId`, `testScore`

- **Constants:** UPPER_SNAKE_CASE
  - ✅ `GEMINI_API_KEY`, `MAX_QUESTIONS_PER_TEST`
  - ❌ `gemini_api_key`, `maxQuestionsPerTest`

- **Pydantic schemas:** PascalCase class, snake_case fields
  ```python
  class TestResultCreate(BaseModel):
      user_id: int
      test_score: int
      created_at: datetime
  ```

---

### Structure Patterns

#### Project Organization

**Frontend (Next.js App Router):**

**Organization by feature** - components live near their routes:

```
kongtze-frontend/
├── app/
│   ├── (kid)/                      # Kid interface routes
│   │   ├── dashboard/
│   │   │   ├── page.tsx            # Dashboard page
│   │   │   └── components/         # Dashboard-specific components
│   │   │       ├── WeeklyCalendar.tsx
│   │   │       └── WeeklyCalendar.test.tsx
│   │   ├── test/
│   │   │   ├── [test_id]/
│   │   │   │   └── page.tsx
│   │   │   └── components/
│   │   │       ├── QuestionCard.tsx
│   │   │       ├── TestTimer.tsx
│   │   │       └── ProgressBar.tsx
│   │   └── lucky-draw/
│   │       ├── page.tsx
│   │       └── components/
│   ├── (parent)/                   # Parent dashboard routes
│   │   ├── dashboard/
│   │   │   ├── page.tsx
│   │   │   └── components/
│   │   ├── analytics/
│   │   └── settings/
│   ├── layout.tsx                  # Root layout
│   └── globals.css                 # Global styles
├── components/
│   └── shared/                     # Truly shared components
│       ├── Button.tsx
│       ├── Modal.tsx
│       └── LoadingSpinner.tsx
├── lib/
│   ├── api-client.ts               # Backend API client
│   ├── auth-context.tsx            # Auth context provider
│   ├── types.ts                    # Shared TypeScript types
│   └── utils/
│       ├── format-date.ts
│       └── calculate-score.ts
├── public/                         # Static assets
│   ├── images/
│   ├── icons/
│   └── fonts/
└── hooks/                          # Custom React hooks
    ├── use-auth.ts
    └── use-test-timer.ts
```

**Backend (FastAPI):**

**Organization by domain** - clear separation of concerns:

```
kongtze-backend/
├── app/
│   ├── main.py                     # FastAPI app entry
│   ├── core/
│   │   ├── config.py               # Settings (Pydantic Settings)
│   │   ├── security.py             # JWT, password hashing
│   │   └── database.py             # DB connection, session
│   ├── models/                     # SQLAlchemy models (by domain)
│   │   ├── user.py
│   │   ├── subject.py
│   │   ├── test.py
│   │   ├── question.py
│   │   ├── result.py
│   │   ├── homework.py
│   │   ├── class_note.py
│   │   ├── reward.py
│   │   └── cached_explanation.py
│   ├── schemas/                    # Pydantic schemas (by domain)
│   │   ├── user.py
│   │   ├── test.py
│   │   ├── homework.py
│   │   └── reward.py
│   ├── api/
│   │   └── routes/                 # API endpoints (by domain)
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── calendar.py
│   │       ├── tests.py
│   │       ├── homework.py
│   │       ├── class_notes.py
│   │       ├── ai.py
│   │       ├── rewards.py
│   │       └── dashboard.py
│   ├── services/                   # Business logic (by domain)
│   │   ├── gemini_service.py
│   │   ├── vision_service.py
│   │   ├── test_generation.py
│   │   ├── difficulty_adjustment.py
│   │   ├── gamification.py
│   │   └── analytics.py
│   └── dependencies.py             # FastAPI dependency injection
├── alembic/                        # Database migrations
│   ├── versions/
│   │   └── 001_initial_schema.py
│   └── env.py
├── tests/                          # Pytest tests (mirrors app/)
│   ├── test_api/
│   │   ├── test_auth.py
│   │   └── test_tests.py
│   ├── test_services/
│   │   ├── test_gemini_service.py
│   │   └── test_test_generation.py
│   └── conftest.py                 # Pytest fixtures
├── .env.example                    # Template for .env
├── requirements.txt
└── README.md
```

#### File Structure Patterns

**Test Files:**

- **Frontend:** Co-located with components
  - ✅ `UserCard.tsx` + `UserCard.test.tsx` side-by-side
  - ❌ Separate `tests/components/` directory

- **Backend:** Separate `tests/` directory mirrors `app/` structure
  - ✅ `tests/test_services/test_gemini_service.py`
  - ❌ `app/services/gemini_service.test.py`

**Configuration Files:**

- **Frontend:** Root-level Next.js config files
  - `next.config.ts`, `tailwind.config.ts`, `tsconfig.json`
  - `.env.local` (gitignored), `.env.example` (committed)

- **Backend:** Root-level Python config files
  - `requirements.txt`, `alembic.ini`, `.env` (gitignored), `.env.example` (committed)

**Static Assets:**

- **Frontend:** `public/` directory organized by type
  - `public/images/kid/`, `public/images/parent/`
  - `public/icons/rewards/`, `public/fonts/`
  - ✅ Descriptive names: `lucky-draw-box-gold.png`
  - ❌ Generic names: `image1.png`, `icon.svg`

---

### Format Patterns

#### API Response Formats

**Success Responses:**

**Direct response (no wrapper):**
```json
GET /api/users/1
{
  "user_id": 1,
  "name": "Student",
  "email": "student@example.com",
  "created_at": "2026-01-21T10:30:00Z"
}

POST /api/tests
{
  "test_id": 123,
  "subject_id": 1,
  "difficulty_level": 2,
  "created_at": "2026-01-21T10:30:00Z"
}
```

**Array responses:**
```json
GET /api/tests
[
  {"test_id": 1, "subject_id": 1, "created_at": "..."},
  {"test_id": 2, "subject_id": 2, "created_at": "..."}
]
```

**Paginated responses** (when pagination needed):
```json
GET /api/tests?page=1&page_size=20
{
  "items": [
    {"test_id": 1, ...},
    {"test_id": 2, ...}
  ],
  "total": 50,
  "page": 1,
  "page_size": 20,
  "total_pages": 3
}
```

**Error Responses** (FastAPI default format):
```json
{
  "detail": "User not found",
  "error_code": "USER_NOT_FOUND",
  "timestamp": "2026-01-21T10:30:00Z"
}
```

**HTTP Status Codes** (from Decision 3.2):
- `200 OK` - Successful GET, PUT, PATCH
- `201 Created` - Successful POST creating resource
- `204 No Content` - Successful DELETE
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Missing or invalid JWT
- `403 Forbidden` - Valid JWT but insufficient permissions
- `404 Not Found` - Resource doesn't exist
- `422 Unprocessable Entity` - Pydantic validation error
- `500 Internal Server Error` - Unexpected server error

#### Data Exchange Formats

**Date/Time Fields:**

**Always use ISO 8601 strings:**
- ✅ `"created_at": "2026-01-21T10:30:00Z"` (UTC with Z suffix)
- ✅ `"test_date": "2026-01-21"` (date-only)
- ❌ `"created_at": 1737454200` (Unix timestamp)
- ❌ `"created_at": "21/01/2026"` (ambiguous format)

**Frontend/Backend:** Pydantic automatically serializes Python `datetime` to ISO 8601

**Boolean Fields:**
- ✅ `"is_completed": true` (JSON boolean)
- ❌ `"is_completed": 1` (integer)
- ❌ `"is_completed": "yes"` (string)

**Null Handling:**
- ✅ `"optional_field": null` (JSON null for missing values)
- ❌ `"optional_field": ""` (empty string)
- ❌ Omit field entirely (include with null for clarity)

**JSON Field Naming:**
- **Backend → Frontend:** snake_case (backend owns naming)
  - API sends: `{"user_id": 1, "created_at": "..."}`
  - Frontend TypeScript interface maps to camelCase internally if desired

**File Upload Format:**
- **Content-Type:** `multipart/form-data`
- **Field name:** Descriptive, snake_case
  - ✅ `homework_photo`, `class_note_photo`
  - ❌ `file`, `upload`, `image`
- **Metadata:** Separate form fields
  ```
  homework_photo: [File]
  subject_id: 1
  uploaded_at: "2026-01-21"
  ```

---

### Communication Patterns

#### State Management Patterns

**Frontend (React Context + TanStack Query):**

**Auth State (React Context):**
```typescript
// lib/auth-context.tsx
interface AuthContext {
  user: User | null;
  token: string | null;
  login: (email: string, password: string) => Promise<void>;
  logout: () => void;
  isAuthenticated: boolean;
}
```

**Server State (TanStack Query):**
```typescript
// hooks/use-tests.ts
const { data, isLoading, error } = useQuery({
  queryKey: ['tests', userId],
  queryFn: () => apiClient.getTests(userId),
});
```

**State Update Pattern:**
- ✅ Immutable updates for React state
  ```typescript
  setState(prev => ({ ...prev, score: newScore }));
  ```
- ❌ Direct mutation
  ```typescript
  state.score = newScore; // Don't do this
  ```

**TanStack Query Cache Invalidation:**
```typescript
// After creating test
queryClient.invalidateQueries({ queryKey: ['tests'] });
```

#### Event Naming (Future WebSocket/SSE)

**If real-time features are added later:**

- **Event names:** snake_case, past tense
  - ✅ `test_submitted`, `reward_earned`, `timer_expired`
  - ❌ `TestSubmitted`, `REWARD_EARNED`, `timerExpire`

- **Event payload:** Consistent snake_case JSON
  ```json
  {
    "event": "test_submitted",
    "data": {
      "test_id": 123,
      "user_id": 1,
      "submitted_at": "2026-01-21T10:30:00Z"
    }
  }
  ```

---

### Process Patterns

#### Error Handling Patterns

**Frontend:**

**Global Error Boundary:**
```typescript
// app/error.tsx (Next.js App Router)
'use client';
export default function Error({ error, reset }: ErrorProps) {
  return (
    <div>
      <h2>Something went wrong!</h2>
      <button onClick={reset}>Try again</button>
    </div>
  );
}
```

**Local API Error Handling:**
```typescript
// In component
const { data, error, isError } = useQuery({
  queryKey: ['tests'],
  queryFn: apiClient.getTests,
});

if (isError) {
  return <ErrorMessage message={error.message} />;
}
```

**API Client Error Handling:**
```typescript
// lib/api-client.ts
async function apiRequest(url: string, options: RequestInit) {
  const response = await fetch(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${getToken()}`,
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {
    const error = await response.json();
    throw new Error(error.detail || 'API request failed');
  }
  
  return response.json();
}
```

**Backend:**

**Custom Exception Classes:**
```python
# app/core/exceptions.py
from fastapi import HTTPException

class TestNotFoundError(HTTPException):
    def __init__(self):
        super().__init__(status_code=404, detail="Test not found")

class InvalidDifficultyError(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Invalid difficulty level")
```

**Exception Handlers:**
```python
# app/main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(TestNotFoundError)
async def test_not_found_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail, "error_code": "TEST_NOT_FOUND"}
    )
```

**Service Layer Error Pattern:**
```python
# app/services/test_generation.py
async def generate_test(user_id: int, difficulty: int):
    if difficulty not in [1, 2, 3, 4]:
        raise InvalidDifficultyError()
    
    user = await get_user(user_id)
    if not user:
        raise UserNotFoundError()
    
    # Generate test...
```

#### Loading State Patterns

**Frontend:**

**TanStack Query Automatic Loading:**
```typescript
const { data, isLoading, isFetching } = useQuery({
  queryKey: ['test', testId],
  queryFn: () => apiClient.getTest(testId),
});

if (isLoading) return <LoadingSpinner />;
if (data) return <TestView test={data} />;
```

**Manual Loading (for non-query operations):**
```typescript
const [isSubmitting, setIsSubmitting] = useState(false);

const handleSubmit = async () => {
  setIsSubmitting(true);
  try {
    await apiClient.submitTest(testId, answers);
  } finally {
    setIsSubmitting(false);
  }
};
```

**Loading UI Convention:**
- Global navigation loading: Next.js built-in top progress bar
- Component loading: Local `<LoadingSpinner />` component
- Button loading: Disabled state + spinner inside button

#### Form Validation Patterns

**Frontend (React Hook Form + Zod):**

```typescript
import { z } from 'zod';
import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';

const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be 8+ characters'),
});

type LoginForm = z.infer<typeof loginSchema>;

function LoginForm() {
  const { register, handleSubmit, formState: { errors } } = useForm<LoginForm>({
    resolver: zodResolver(loginSchema),
  });
  
  const onSubmit = async (data: LoginForm) => {
    await apiClient.login(data);
  };
  
  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <input {...register('email')} />
      {errors.email && <span>{errors.email.message}</span>}
    </form>
  );
}
```

**Backend (Pydantic automatic validation):**

```python
from pydantic import BaseModel, EmailStr, Field

class UserLogin(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)

@app.post("/api/auth/login")
async def login(credentials: UserLogin):
    # Pydantic automatically validates
    # Returns 422 if validation fails
    ...
```

**Validation Strategy:**
- ✅ Client-side validation for UX (immediate feedback)
- ✅ Server-side validation for security (never trust client)
- Both use same validation rules where possible

#### Authentication Flow Pattern

**Login Flow:**

1. Frontend: User submits email/password via React Hook Form
2. Frontend: POST `/api/auth/login` with credentials
3. Backend: Verify password with bcrypt, generate JWT
4. Backend: Return `{"token": "...", "user": {...}}`
5. Frontend: Store token in localStorage
6. Frontend: Set auth context state
7. Frontend: Redirect to dashboard

**Authenticated Requests:**

```typescript
// lib/api-client.ts
function getToken(): string | null {
  return localStorage.getItem('auth_token');
}

async function authenticatedRequest(url: string, options: RequestInit = {}) {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  
  return apiRequest(url, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,
      ...options.headers,
    },
  });
}
```

**Logout Flow:**

1. Frontend: User clicks logout
2. Frontend: Clear localStorage token
3. Frontend: Reset auth context
4. Frontend: Redirect to login page
5. (Optional) Backend: Blacklist token if using token blacklist

**Token Refresh (Optional for MVP):**
- Not required for single-user family app
- Can add later if sessions need to persist longer

---

### Enforcement Guidelines

#### All AI Agents MUST:

1. **Follow snake_case for all backend code** (Python/PostgreSQL)
   - Database columns, JSON API fields, Python variables, file names

2. **Follow PascalCase for React components**, kebab-case for utilities
   - `UserCard.tsx`, `api-client.ts`, `format-date.ts`

3. **Use plural resource names for REST endpoints**
   - `/api/users/{id}`, `/api/tests`, `/api/rewards`

4. **Return ISO 8601 strings for all dates/times**
   - `"2026-01-21T10:30:00Z"` for datetimes
   - `"2026-01-21"` for dates

5. **Use TanStack Query for all server state management**
   - No manual `useState` for API data
   - Use `useQuery` for GET, `useMutation` for POST/PUT/DELETE

6. **Co-locate frontend tests**, separate backend tests
   - Frontend: `UserCard.test.tsx` next to `UserCard.tsx`
   - Backend: `tests/test_services/test_gemini_service.py`

7. **Organize code by feature/domain**, not by type
   - Frontend: Components in `app/(kid)/dashboard/components/`
   - Backend: Services in `services/` grouped by domain

8. **Use direct JSON responses**, metadata wrapper only for pagination
   - Simple GET: Return object/array directly
   - Paginated: `{"items": [...], "total": 50, "page": 1}`

9. **Handle errors consistently**
   - Frontend: Error Boundaries + local try/catch with TanStack Query
   - Backend: Custom exception classes + FastAPI exception handlers

10. **Store JWT in localStorage**, include in `Authorization` header
    - Login stores token, logout clears it
    - All protected requests include `Bearer <token>`

#### Pattern Enforcement:

**Code Review Checklist:**
- [ ] Database/API naming follows snake_case convention
- [ ] React components use PascalCase, files match component names
- [ ] API endpoints use plural resource names
- [ ] Dates/times serialized as ISO 8601 strings
- [ ] TanStack Query used for all API data fetching
- [ ] Tests co-located (frontend) or in tests/ (backend)
- [ ] Error handling uses established patterns
- [ ] No hardcoded values (use config/env vars)

**Automated Enforcement (Future):**
- ESLint rules for frontend naming conventions
- Ruff/Black for backend Python formatting
- Pre-commit hooks to validate patterns
- TypeScript strict mode catches type inconsistencies

**Pattern Violation Process:**
1. Identify pattern violation in code review
2. Document specific pattern violated
3. Provide correction example from this document
4. Update code to follow pattern
5. If pattern is unclear, update this architecture doc

---

### Pattern Examples

#### Good Examples

**Database Model (Backend):**
```python
# app/models/test_result.py
from sqlalchemy.orm import Mapped, mapped_column
from datetime import datetime

class TestResult(Base):
    __tablename__ = "test_results"  # ✅ Plural, snake_case
    
    test_result_id: Mapped[int] = mapped_column(primary_key=True)  # ✅ snake_case
    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"))  # ✅ {table}_id
    test_score: Mapped[int]  # ✅ snake_case
    created_at: Mapped[datetime] = mapped_column(default=func.now())  # ✅ snake_case
```

**API Route (Backend):**
```python
# app/api/routes/tests.py
from fastapi import APIRouter, HTTPException

router = APIRouter(prefix="/api/tests", tags=["tests"])  # ✅ Plural

@router.get("/{test_id}")  # ✅ {id} format
async def get_test(test_id: int):  # ✅ snake_case param
    test = await get_test_by_id(test_id)
    if not test:
        raise HTTPException(status_code=404, detail="Test not found")  # ✅ 404 status
    return test  # ✅ Direct response (no wrapper)
```

**API Response (Backend → Frontend):**
```json
{
  "test_id": 123,
  "subject_id": 1,
  "difficulty_level": 2,
  "time_limit_seconds": 1800,
  "created_at": "2026-01-21T10:30:00Z",
  "questions": [
    {
      "question_id": 1,
      "question_text": "What is 2 + 2?",
      "correct_answer": "4"
    }
  ]
}
```

**React Component (Frontend):**
```typescript
// app/(kid)/test/components/TestTimer.tsx
'use client';
import { useState, useEffect } from 'react';

interface TestTimerProps {  // ✅ PascalCase interface
  timeLimitSeconds: number;  // ✅ camelCase prop (internal)
  onTimeExpired: () => void;
}

export function TestTimer({ timeLimitSeconds, onTimeExpired }: TestTimerProps) {  // ✅ PascalCase component
  const [secondsRemaining, setSecondsRemaining] = useState(timeLimitSeconds);  // ✅ camelCase
  
  useEffect(() => {
    const interval = setInterval(() => {
      setSecondsRemaining(prev => {
        if (prev <= 1) {
          onTimeExpired();
          return 0;
        }
        return prev - 1;
      });
    }, 1000);
    
    return () => clearInterval(interval);
  }, [onTimeExpired]);
  
  return <div className="text-2xl font-bold">{secondsRemaining}s</div>;
}
```

**TanStack Query Usage (Frontend):**
```typescript
// app/(kid)/test/[test_id]/page.tsx
'use client';
import { useQuery, useMutation } from '@tanstack/react-query';
import { apiClient } from '@/lib/api-client';

export default function TestPage({ params }: { params: { test_id: string } }) {
  // ✅ TanStack Query for fetching
  const { data: test, isLoading, error } = useQuery({
    queryKey: ['test', params.test_id],
    queryFn: () => apiClient.getTest(parseInt(params.test_id)),
  });
  
  // ✅ TanStack Query for mutation
  const submitMutation = useMutation({
    mutationFn: (answers: Record<number, string>) => 
      apiClient.submitTest(parseInt(params.test_id), answers),
    onSuccess: () => {
      // Navigate to results
    },
  });
  
  if (isLoading) return <LoadingSpinner />;  // ✅ TanStack Query loading state
  if (error) return <ErrorMessage message={error.message} />;  // ✅ Error handling
  if (!test) return null;
  
  return <TestView test={test} onSubmit={submitMutation.mutate} />;
}
```

**API Client (Frontend):**
```typescript
// lib/api-client.ts
const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL;  // ✅ UPPER_SNAKE_CASE constant

function getToken(): string | null {  // ✅ camelCase function
  return localStorage.getItem('auth_token');  // ✅ JWT in localStorage
}

async function authenticatedRequest<T>(  // ✅ Generic type
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getToken();
  if (!token) throw new Error('Not authenticated');
  
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Authorization': `Bearer ${token}`,  // ✅ Bearer token
      'Content-Type': 'application/json',
      ...options.headers,
    },
  });
  
  if (!response.ok) {  // ✅ Error handling
    const error = await response.json();
    throw new Error(error.detail || 'Request failed');
  }
  
  return response.json();
}

export const apiClient = {
  getTest: (testId: number) => 
    authenticatedRequest<Test>(`/api/tests/${testId}`),  // ✅ Plural endpoint
  submitTest: (testId: number, answers: Record<number, string>) =>
    authenticatedRequest(`/api/tests/${testId}/submit`, {
      method: 'POST',
      body: JSON.stringify({ answers }),  // ✅ snake_case sent to backend
    }),
};
```

#### Anti-Patterns (What to Avoid)

**❌ Wrong Database Naming:**
```python
class TestResults(Base):  # ❌ Class name matches table (should be TestResult)
    __tablename__ = "TestResults"  # ❌ PascalCase table name
    
    TestID: Mapped[int]  # ❌ PascalCase column
    userId: Mapped[int]  # ❌ camelCase column
    fk_user: Mapped[int]  # ❌ Prefix instead of {table}_id format
```

**❌ Wrong API Naming:**
```python
@router.get("/api/test/{id}")  # ❌ Singular resource
async def getTest(id: int):  # ❌ camelCase function, generic param name
    pass

@router.get("/api/tests/:test_id")  # ❌ Express.js style :param instead of {param}
```

**❌ Wrong API Response:**
```json
{
  "data": {  // ❌ Unnecessary wrapper
    "testId": 123,  // ❌ camelCase (should be snake_case)
    "createdAt": 1737454200  // ❌ Unix timestamp (should be ISO 8601)
  },
  "error": null
}
```

**❌ Wrong React Component:**
```typescript
// components/test-timer.tsx  ❌ kebab-case filename for component
export function test_timer() {  // ❌ snake_case component name
  const [seconds_remaining, setSecondsRemaining] = useState(0);  // ❌ snake_case variable
  return <div>{seconds_remaining}</div>;
}
```

**❌ Wrong State Management:**
```typescript
// ❌ Manual state for API data instead of TanStack Query
const [test, setTest] = useState(null);
const [loading, setLoading] = useState(false);

useEffect(() => {
  setLoading(true);
  fetch('/api/tests/123')
    .then(res => res.json())
    .then(data => setTest(data))
    .finally(() => setLoading(false));
}, []);
```

**❌ Wrong Error Handling:**
```python
# ❌ Generic exception instead of custom HTTP exception
@router.get("/api/tests/{test_id}")
async def get_test(test_id: int):
    test = await db.get(test_id)
    if not test:
        raise Exception("Not found")  # ❌ Generic exception
    return test
```

**❌ Wrong Date Format:**
```python
# ❌ Returning Unix timestamp instead of ISO 8601
class TestResponse(BaseModel):
    created_at: int  # ❌ Should be datetime
    
# Frontend
const timestamp = 1737454200;  // ❌ Should use ISO string
```

**❌ Wrong File Organization:**
```
app/
  components/  # ❌ All components in one flat directory
    UserCard.tsx
    TestTimer.tsx
    WeeklyCalendar.tsx
    Analytics.tsx
    
  tests/  # ❌ Frontend tests in separate directory
    UserCard.test.tsx
```

**❌ Wrong Authentication:**
```typescript
// ❌ Token in state instead of localStorage
const [token, setToken] = useState(null);  // Lost on refresh

// ❌ Missing Authorization header
fetch('/api/tests', {
  headers: {
    'token': token  // ❌ Wrong header name
  }
});
```

---

**Summary:**

These implementation patterns ensure that any AI agent working on Kongtze (now or in future sessions) will write code that integrates seamlessly. The patterns cover:

- ✅ **24 conflict points** addressed across naming, structure, format, and process
- ✅ **Concrete examples** for every pattern (good and anti-pattern)
- ✅ **Technology-specific** conventions for Next.js/React and FastAPI/Python
- ✅ **Enforcement guidelines** for code review and validation
- ✅ **Single source of truth** for all implementation decisions

---

## Project Structure & Boundaries

### Complete Project Directory Structure

This section defines the complete physical structure of both Kongtze repositories, mapping all 96 functional requirements from the PRD to specific files and directories.

---

#### Frontend Repository: kongtze-frontend

```
kongtze-frontend/
├── README.md
├── package.json
├── package-lock.json
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
├── postcss.config.js
├── .env.local                      # Gitignored (local development)
├── .env.example                    # Committed template (dummy values)
├── .gitignore
├── .eslintrc.json
├── .prettierrc
├── app/
│   ├── layout.tsx                  # Root layout (auth providers, TanStack Query)
│   ├── page.tsx                    # Landing/login page
│   ├── globals.css                 # Tailwind directives + global styles
│   ├── error.tsx                   # Global error boundary
│   ├── not-found.tsx               # 404 page
│   │
│   ├── (auth)/                     # Auth routes (no persistent layout)
│   │   ├── login/
│   │   │   └── page.tsx            # Parent login (email/password)
│   │   └── pin/                    # Student PIN entry (4-digit)
│   │       └── page.tsx
│   │
│   ├── (kid)/                      # Kid interface routes (iPad-optimized)
│   │   ├── layout.tsx              # Kid-specific layout (bright colors, large buttons)
│   │   │
│   │   ├── dashboard/
│   │   │   ├── page.tsx            # Kid dashboard (calendar, upcoming tests, points)
│   │   │   └── components/
│   │   │       ├── WeeklyCalendar.tsx
│   │   │       ├── WeeklyCalendar.test.tsx
│   │   │       ├── UpcomingTests.tsx
│   │   │       ├── UpcomingTests.test.tsx
│   │   │       ├── RewardPoints.tsx
│   │   │       └── RewardPoints.test.tsx
│   │   │
│   │   ├── test/
│   │   │   ├── [test_id]/
│   │   │   │   ├── page.tsx        # Take test page (timer, questions)
│   │   │   │   └── results/
│   │   │   │       └── page.tsx    # Test results page (score, explanations)
│   │   │   └── components/
│   │   │       ├── QuestionCard.tsx
│   │   │       ├── QuestionCard.test.tsx
│   │   │       ├── TestTimer.tsx
│   │   │       ├── TestTimer.test.tsx
│   │   │       ├── ProgressBar.tsx
│   │   │       ├── ProgressBar.test.tsx
│   │   │       ├── ResultsSummary.tsx
│   │   │       ├── ResultsSummary.test.tsx
│   │   │       └── ExplanationCard.tsx
│   │   │
│   │   ├── homework/
│   │   │   ├── upload/
│   │   │   │   └── page.tsx        # Upload homework photo
│   │   │   └── components/
│   │   │       ├── PhotoUploader.tsx
│   │   │       ├── PhotoUploader.test.tsx
│   │   │       └── UploadPreview.tsx
│   │   │
│   │   ├── notes/                  # Class notes upload (FR-NOTES-001 to 015)
│   │   │   ├── upload/
│   │   │   │   └── page.tsx        # Upload class notes photo
│   │   │   └── components/
│   │   │       ├── NotesUploader.tsx
│   │   │       ├── NotesUploader.test.tsx
│   │   │       └── NotesPreview.tsx
│   │   │
│   │   └── lucky-draw/
│   │       ├── page.tsx            # Lucky draw blind box (gamification)
│   │       └── components/
│   │           ├── LuckyDrawBox.tsx
│   │           ├── LuckyDrawBox.test.tsx
│   │           ├── GiftAnimation.tsx
│   │           ├── GiftAnimation.test.tsx
│   │           └── GiftInventory.tsx
│   │
│   └── (parent)/                   # Parent dashboard routes (laptop-optimized)
│       ├── layout.tsx              # Parent-specific layout (professional theme)
│       │
│       ├── dashboard/
│       │   ├── page.tsx            # Parent overview dashboard
│       │   └── components/
│       │       ├── DailyOverview.tsx
│       │       ├── DailyOverview.test.tsx
│       │       ├── WeeklyPerformanceGraph.tsx
│       │       ├── SubjectBreakdown.tsx
│       │       └── RecentActivity.tsx
│       │
│       ├── calendar/
│       │   ├── page.tsx            # Manage study calendar (weekly sessions)
│       │   └── components/
│       │       ├── CalendarEditor.tsx
│       │       ├── CalendarEditor.test.tsx
│       │       └── SessionForm.tsx
│       │
│       ├── analytics/
│       │   ├── page.tsx            # Detailed analytics (trends, difficulty progress)
│       │   └── components/
│       │       ├── PerformanceTrends.tsx
│       │       ├── DifficultyProgress.tsx
│       │       └── TimeAnalytics.tsx
│       │
│       ├── notes/
│       │   ├── page.tsx            # View class notes & curriculum tracking
│       │   └── components/
│       │       ├── NotesViewer.tsx
│       │       └── TopicList.tsx
│       │
│       ├── homework/
│       │   ├── page.tsx            # Review homework OCR results
│       │   └── components/
│       │       ├── HomeworkReviewer.tsx
│       │       └── OCRCorrector.tsx
│       │
│       └── settings/
│           ├── page.tsx            # App settings, gift catalog, notifications
│           └── components/
│               ├── GiftCatalog.tsx
│               ├── NotificationSettings.tsx
│               └── ProfileSettings.tsx
│
├── components/
│   └── shared/                     # Truly shared components (kid + parent)
│       ├── Button.tsx
│       ├── Button.test.tsx
│       ├── Modal.tsx
│       ├── Modal.test.tsx
│       ├── LoadingSpinner.tsx
│       ├── LoadingSpinner.test.tsx
│       ├── ErrorMessage.tsx
│       ├── ErrorMessage.test.tsx
│       ├── Card.tsx
│       └── Input.tsx
│
├── lib/
│   ├── api-client.ts               # Backend API client (fetch wrapper with auth)
│   ├── auth-context.tsx            # Auth context provider (React Context)
│   ├── query-provider.tsx          # TanStack Query provider wrapper
│   ├── types.ts                    # Shared TypeScript types/interfaces
│   └── utils/
│       ├── format-date.ts
│       ├── calculate-score.ts
│       ├── format-time.ts
│       └── validators.ts
│
├── hooks/                          # Custom React hooks
│   ├── use-auth.ts                 # Auth hook (from context)
│   ├── use-test-timer.ts           # Test timer hook (client-side countdown)
│   ├── use-tests.ts                # TanStack Query hooks for tests API
│   ├── use-homework.ts             # TanStack Query hooks for homework API
│   ├── use-class-notes.ts          # TanStack Query hooks for class notes API
│   └── use-rewards.ts              # TanStack Query hooks for rewards API
│
├── public/
│   ├── images/
│   │   ├── kid/
│   │   │   ├── celebration.gif     # Gamification animations
│   │   │   └── mascot.png
│   │   └── parent/
│   │       └── logo.png
│   ├── icons/
│   │   └── rewards/
│   │       ├── gold-box.svg
│   │       ├── silver-box.svg
│   │       └── bronze-box.svg
│   └── fonts/
│       └── (custom fonts if needed)
│
└── .github/
    └── workflows/
        └── deploy.yml              # Railway deployment workflow
```

---

#### Backend Repository: kongtze-backend

```
kongtze-backend/
├── README.md
├── requirements.txt
├── requirements-dev.txt            # Dev dependencies (pytest, black, ruff, mypy)
├── .env                            # Gitignored (local + Railway secrets)
├── .env.example                    # Committed template (dummy values)
├── .gitignore
├── .python-version                 # 3.11
├── alembic.ini
├── pyproject.toml                  # Black, Ruff, MyPy config
├── app/
│   ├── main.py                     # FastAPI app entry, CORS, middleware, routers
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py               # Pydantic Settings (DATABASE_URL, API keys)
│   │   ├── security.py             # JWT creation/verification, bcrypt hashing
│   │   ├── database.py             # Async SQLAlchemy session, engine, Base
│   │   └── exceptions.py           # Custom HTTP exception classes
│   │
│   ├── models/                     # SQLAlchemy models (async ORM)
│   │   ├── __init__.py
│   │   ├── user.py                 # User (parent + student), password, PIN
│   │   ├── subject.py              # Math, English, Chinese, Science
│   │   ├── study_session.py        # Calendar sessions (weekly schedule)
│   │   ├── test.py                 # Test metadata (subject, difficulty, time_limit)
│   │   ├── question.py             # Question bank (linked to tests)
│   │   ├── test_result.py          # Test results, answers, scores, time_taken
│   │   ├── homework.py             # Homework uploads, OCR results
│   │   ├── class_note.py           # Class notes uploads (FR-NOTES category)
│   │   ├── topic.py                # Curriculum topics extracted from notes (AI)
│   │   ├── reward.py               # Reward points, transactions, milestones
│   │   ├── gift.py                 # Gift catalog (parent-configurable)
│   │   └── cached_explanation.py   # AI explanation cache (question_hash → explanation)
│   │
│   ├── schemas/                    # Pydantic schemas (request/response validation)
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── auth.py                 # LoginRequest, TokenResponse
│   │   ├── subject.py
│   │   ├── study_session.py
│   │   ├── test.py                 # TestCreate, TestResponse
│   │   ├── question.py
│   │   ├── test_result.py          # TestSubmission, TestResultResponse
│   │   ├── homework.py
│   │   ├── class_note.py
│   │   ├── topic.py
│   │   ├── reward.py
│   │   └── dashboard.py            # DashboardResponse (aggregated analytics)
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── routes/                 # API endpoints (by domain, plural resources)
│   │       ├── __init__.py
│   │       ├── auth.py             # POST /api/auth/login, POST /api/auth/logout
│   │       ├── users.py            # GET /api/users/{user_id}, PUT /api/users/{user_id}
│   │       ├── subjects.py         # GET /api/subjects
│   │       ├── calendar.py         # GET/POST/PUT/DELETE /api/study-sessions
│   │       ├── tests.py            # POST /api/tests (generate), GET /api/tests/{test_id}
│   │       ├── questions.py        # GET /api/tests/{test_id}/questions
│   │       ├── test_results.py     # POST /api/tests/{test_id}/submit, GET /api/test-results
│   │       ├── homework.py         # POST /api/homework (upload), GET /api/homework/{homework_id}
│   │       ├── class_notes.py      # POST /api/class-notes (upload), GET /api/class-notes
│   │       ├── topics.py           # GET /api/topics (curriculum tracking from notes)
│   │       ├── rewards.py          # GET /api/rewards, POST /api/rewards/lucky-draw
│   │       ├── gifts.py            # GET /api/gifts (catalog), PUT /api/gifts/{gift_id}
│   │       ├── ai.py               # POST /api/ai/explain (get cached/new explanation)
│   │       └── dashboard.py        # GET /api/dashboard (parent analytics aggregation)
│   │
│   ├── services/                   # Business logic (by domain)
│   │   ├── __init__.py
│   │   ├── gemini_service.py       # Google Gemini API integration (test gen, explanations)
│   │   ├── vision_service.py       # Google Cloud Vision OCR (homework, notes)
│   │   ├── test_generation.py      # Test generation logic (difficulty, class notes context)
│   │   ├── difficulty_adjustment.py # Algorithm for difficulty scaling (4 levels)
│   │   ├── gamification.py         # Scoring, rewards, lucky draw probability logic
│   │   ├── analytics.py            # Parent dashboard analytics calculations
│   │   ├── topic_extraction.py     # Extract topics/concepts from class notes (Gemini)
│   │   └── cache_service.py        # AI explanation caching (question hash lookup)
│   │
│   └── dependencies.py             # FastAPI dependency injection (get_db, get_current_user)
│
├── alembic/                        # Database migrations
│   ├── env.py                      # Alembic async engine config
│   ├── script.py.mako              # Migration template
│   └── versions/
│       ├── 001_initial_schema.py   # Users, subjects, tests, questions
│       ├── 002_add_class_notes.py  # Class notes, topics (from PRD update)
│       └── (future migrations auto-generated + reviewed)
│
├── tests/                          # Pytest tests (mirrors app/ structure)
│   ├── __init__.py
│   ├── conftest.py                 # Pytest fixtures (test DB, async client, mock Gemini/Vision)
│   │
│   ├── test_api/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_tests.py
│   │   ├── test_test_results.py
│   │   ├── test_homework.py
│   │   ├── test_class_notes.py
│   │   ├── test_rewards.py
│   │   └── test_dashboard.py
│   │
│   ├── test_services/
│   │   ├── __init__.py
│   │   ├── test_gemini_service.py
│   │   ├── test_vision_service.py
│   │   ├── test_test_generation.py
│   │   ├── test_difficulty_adjustment.py
│   │   ├── test_gamification.py
│   │   └── test_topic_extraction.py
│   │
│   └── test_models/
│       ├── __init__.py
│       ├── test_user.py
│       ├── test_test.py
│       ├── test_class_note.py
│       └── test_reward.py
│
├── storage/                        # Local file storage (Railway persistent disk)
│   ├── homework/
│   │   └── (uploaded photos: homework_<id>_<timestamp>.jpg)
│   ├── class_notes/
│   │   └── (uploaded photos: note_<id>_<timestamp>.jpg)
│   └── .gitkeep
│
└── .github/
    └── workflows/
        └── deploy.yml              # Railway deployment workflow (auto-run migrations)
```

---

### Architectural Boundaries

#### API Boundaries

**External API Surface (Frontend → Backend):**

All API endpoints follow REST conventions with plural resource names and snake_case JSON fields:

**Authentication:**
- `POST /api/auth/login` - Parent login (email/password) → Returns JWT token
- `POST /api/auth/pin` - Student PIN verification → Returns JWT token

**User Management:**
- `GET /api/users/{user_id}` - Get user profile
- `PUT /api/users/{user_id}` - Update user profile (parent only)

**Study Calendar:**
- `GET /api/study-sessions` - Get weekly schedule
- `POST /api/study-sessions` - Create session (parent only)
- `PUT /api/study-sessions/{session_id}` - Update session (parent only)
- `DELETE /api/study-sessions/{session_id}` - Delete session (parent only)

**Test Management:**
- `POST /api/tests` - Generate new test (difficulty, subject, class notes context)
- `GET /api/tests/{test_id}` - Get test metadata
- `GET /api/tests/{test_id}/questions` - Get test questions
- `POST /api/tests/{test_id}/submit` - Submit test answers → Returns results + explanations

**Homework:**
- `POST /api/homework` - Upload homework photo (multipart/form-data)
- `GET /api/homework/{homework_id}` - Get homework OCR results
- `PUT /api/homework/{homework_id}` - Parent correction of OCR (if needed)

**Class Notes (Curriculum Tracking):**
- `POST /api/class-notes` - Upload class notes photo (multipart/form-data)
- `GET /api/class-notes` - List all class notes
- `GET /api/class-notes/{note_id}` - Get specific note with extracted topics
- `GET /api/topics` - Get all curriculum topics (from notes AI extraction)

**Gamification:**
- `GET /api/rewards` - Get current points, transaction history
- `POST /api/rewards/lucky-draw` - Trigger lucky draw → Returns gift
- `GET /api/gifts` - Get gift catalog (parent-configurable)
- `PUT /api/gifts/{gift_id}` - Update gift catalog (parent only)

**AI Explanations:**
- `POST /api/ai/explain` - Get explanation for question (cached if available)

**Parent Dashboard:**
- `GET /api/dashboard` - Get aggregated analytics (daily/weekly performance, trends)
- `GET /api/test-results?user_id={id}&date_range={range}` - Get historical results

**Backend Service Boundaries:**

- **Gemini AI Service:** `services/gemini_service.py` → Encapsulates all Google Gemini API calls
- **Vision Service:** `services/vision_service.py` → Encapsulates all Google Cloud Vision OCR
- **Test Generation:** `services/test_generation.py` → Uses Gemini + class notes context
- **Difficulty Adjustment:** `services/difficulty_adjustment.py` → Algorithm for 4-level scaling
- **Gamification:** `services/gamification.py` → Scoring, rewards, lucky draw logic
- **Analytics:** `services/analytics.py` → Aggregates data for parent dashboard
- **Topic Extraction:** `services/topic_extraction.py` → AI extracts curriculum topics from notes
- **Cache Service:** `services/cache_service.py` → Question hash → AI explanation lookup

**Authentication Boundary:**

- All API endpoints except `/api/auth/login` and `/api/auth/pin` require JWT token
- JWT token validated by `dependencies.get_current_user`
- Parent-only endpoints check user role in JWT payload
- Kid interface uses 4-digit PIN (mapped to JWT internally)

#### Component Boundaries

**Frontend Component Communication:**

**1. Kid Interface Components:**
- **Dashboard** (`app/(kid)/dashboard/`)
  - Displays: Weekly calendar (from `/api/study-sessions`), upcoming tests, reward points
  - Communicates: TanStack Query fetches, no direct component-to-component state passing

- **Test Taking** (`app/(kid)/test/[test_id]/`)
  - Receives: `test_id` from route params
  - Fetches: Questions from `/api/tests/{test_id}/questions`
  - Manages: Client-side timer (JavaScript `setInterval`), local answer state
  - Submits: Answers to `/api/tests/{test_id}/submit` → Server validates time
  - Navigates: To results page on completion

- **Results** (`app/(kid)/test/[test_id]/results/`)
  - Receives: `test_id` from route params
  - Fetches: Results from `/api/test-results/{test_id}`
  - Displays: Score, explanations, celebration animations (gamification)

- **Upload Interfaces** (`app/(kid)/homework/upload/`, `app/(kid)/notes/upload/`)
  - Manages: File selection, preview
  - Uploads: Multipart form data to `/api/homework` or `/api/class-notes`
  - Shows: Upload progress, OCR processing status

- **Lucky Draw** (`app/(kid)/lucky-draw/`)
  - Fetches: Available points from `/api/rewards`
  - Triggers: Lucky draw via `/api/rewards/lucky-draw`
  - Displays: Blind box animation, gift reveal

**2. Parent Dashboard Components:**
- **Overview** (`app/(parent)/dashboard/`)
  - Fetches: Aggregated analytics from `/api/dashboard`
  - Displays: Daily overview, weekly graphs, subject breakdown

- **Calendar Editor** (`app/(parent)/calendar/`)
  - Fetches: Study sessions from `/api/study-sessions`
  - Creates/Updates: Sessions via POST/PUT
  - Uses: React Hook Form for session editing

- **Analytics** (`app/(parent)/analytics/`)
  - Fetches: Historical test results from `/api/test-results`
  - Calculates: Client-side charting (performance trends, difficulty progress)

- **Class Notes Viewer** (`app/(parent)/notes/`)
  - Fetches: Class notes from `/api/class-notes`
  - Displays: Uploaded photos, extracted topics (from AI)

**3. Shared Components** (`components/shared/`)
- Pure presentational components (Button, Modal, Card, etc.)
- No direct API calls or complex state
- Receive props from parent components
- Emit events via callbacks

**State Management Boundaries:**

- **Auth Context** (`lib/auth-context.tsx`): Global auth state (user, token, login/logout functions)
  - Consumed by: All authenticated routes
  - Updated by: Login/logout actions

- **TanStack Query**: Server state caching per API endpoint
  - Query keys: `['tests', testId]`, `['homework']`, `['rewards']`, etc.
  - Cache invalidation: After mutations (POST/PUT/DELETE)
  - No cross-query dependencies (each query is independent)

- **Local Component State**: UI-only state (modals open/closed, form inputs, timers)
  - Never shared between components
  - No global UI state (except auth)

#### Service Boundaries

**Backend Service Layer Organization:**

Each service is a standalone module with clear input/output contracts:

**1. Gemini Service** (`services/gemini_service.py`)
- **Input:** Question text, difficulty level, subject, curriculum context (topics from class notes)
- **Output:** Generated test questions, AI explanations, custom questions
- **Dependencies:** Google Gemini API, `GEMINI_API_KEY` env var
- **Used by:** `test_generation.py`, `topic_extraction.py`, `ai.py` routes

**2. Vision Service** (`services/vision_service.py`)
- **Input:** Image file path (homework photo, class note photo)
- **Output:** OCR extracted text, handwriting recognition results
- **Dependencies:** Google Cloud Vision API, `GOOGLE_CLOUD_VISION_CREDENTIALS` env var
- **Used by:** `homework.py` routes, `class_notes.py` routes

**3. Test Generation** (`services/test_generation.py`)
- **Input:** User ID, subject, difficulty level, class notes context (optional)
- **Output:** Generated test with questions, time limits, difficulty metadata
- **Dependencies:** `gemini_service.py`, database (question bank, topics)
- **Logic:** 
  - Fetch recent class notes topics for context
  - Call Gemini to generate curriculum-aware questions
  - Apply difficulty adjustment
  - Calculate time limits per question
- **Used by:** `tests.py` routes

**4. Difficulty Adjustment** (`services/difficulty_adjustment.py`)
- **Input:** User ID, subject, recent test results
- **Output:** Recommended difficulty level (1-4: Beginner → Expert)
- **Dependencies:** Database (test_results table)
- **Algorithm:** 
  - Analyze last 5 tests per subject
  - If 3+ tests with 80%+ accuracy → Increase difficulty
  - If 3+ tests with <50% accuracy → Decrease difficulty
  - Cap at Beginner/Expert boundaries
- **Used by:** `test_generation.py`, `tests.py` routes

**5. Gamification** (`services/gamification.py`)
- **Input:** Test results (score, time taken, difficulty)
- **Output:** Reward points, lucky draw probability, milestone detection
- **Dependencies:** Database (rewards, gifts tables)
- **Logic:**
  - Base points: `score * difficulty_multiplier`
  - Speed bonus: Extra points if completed in <80% of time limit
  - Perfect score bonus: +50 points for 100% accuracy
  - Lucky draw: Weighted probability (gold 10%, silver 30%, bronze 60%)
- **Used by:** `test_results.py` routes, `rewards.py` routes

**6. Analytics** (`services/analytics.py`)
- **Input:** User ID, date range
- **Output:** Aggregated statistics (daily/weekly performance, subject breakdowns, trends)
- **Dependencies:** Database (test_results, study_sessions tables)
- **Calculations:**
  - Average score per subject
  - Difficulty progression timeline
  - Time analytics (avg time per question, pressure indicators)
  - Streak tracking (consecutive days with tests)
- **Used by:** `dashboard.py` routes

**7. Topic Extraction** (`services/topic_extraction.py`)
- **Input:** OCR text from class notes photo
- **Output:** List of curriculum topics, concepts, keywords
- **Dependencies:** `gemini_service.py` (AI topic analysis)
- **Logic:**
  - Send OCR text to Gemini with prompt: "Extract IB PYP curriculum topics"
  - Parse AI response into structured topic list
  - Store in `topics` table linked to class note
- **Used by:** `class_notes.py` routes

**8. Cache Service** (`services/cache_service.py`)
- **Input:** Question text (for hashing), AI explanation
- **Output:** Cached explanation (if exists) or trigger new Gemini call
- **Dependencies:** Database (`cached_explanations` table)
- **Logic:**
  - Hash question text (SHA256)
  - Check if hash exists in cache
  - If yes: Return cached explanation, increment hit_count
  - If no: Call Gemini, store new explanation, return result
- **Used by:** `ai.py` routes, `test_results.py` routes (auto-generate explanations)

**Service Communication Pattern:**

- Services never call each other directly via import (to avoid circular dependencies)
- Services are injected as dependencies where needed
- Routes orchestrate service calls (e.g., `tests.py` calls `test_generation.py` → calls `gemini_service.py`)

#### Data Boundaries

**Database Schema Organization:**

**Core Tables:**
- `users` - Parent + student profiles (shared authentication)
- `subjects` - Math, English, Chinese, Science (static data)

**Study Management:**
- `study_sessions` - Weekly calendar (2-3 sessions/day, 30 min each)

**Testing:**
- `tests` - Test metadata (subject, difficulty, time_limit, created_at)
- `questions` - Question bank (linked to tests via foreign key)
- `test_results` - Results, scores, answers, time_taken

**Content Upload:**
- `homework` - Homework photos, OCR results, parent corrections
- `class_notes` - Class notes photos, OCR results, upload date
- `topics` - Curriculum topics extracted from class notes (AI-generated)

**Gamification:**
- `rewards` - Reward points, transactions, balance
- `gifts` - Gift catalog (parent-configurable, linked to lucky draw)

**Caching:**
- `cached_explanations` - Question hash → AI explanation (reduce Gemini API costs)

**Data Access Patterns:**

- **ORM Layer:** All database access via SQLAlchemy async ORM
  - No raw SQL queries (except complex analytics in `analytics.py`)
  - Models define relationships (e.g., `Test.questions` relationship)

- **Repository Pattern (Optional):** Not implemented initially (services query ORM directly)
  - Can add later if services grow complex

- **Database Session Management:**
  - Session injected via `dependencies.get_db`
  - Auto-commit on success, auto-rollback on exception
  - Connection pooling configured in `core/database.py`

**Caching Boundaries:**

- **PostgreSQL Cache Table:** `cached_explanations`
  - Key: `question_hash` (SHA256 of question text)
  - Value: `ai_explanation` (JSON text)
  - TTL: None (cache indefinitely for single-user app)
  - Invalidation: Manual via parent dashboard (future feature)

- **No Redis:** Single-user app doesn't need separate cache layer

**External Data Integration:**

- **Google Gemini API:** Question generation, explanations, topic extraction
  - Rate limiting: Free tier allows ~60 requests/minute
  - Error handling: Retry with exponential backoff
  - Fallback: If Gemini unavailable, return generic error to frontend

- **Google Cloud Vision API:** OCR for homework, class notes
  - Rate limiting: Free tier allows 1000 requests/month
  - Supported formats: JPEG, PNG, HEIC (convert HEIC server-side if needed)
  - Error handling: Return partial OCR results if processing fails

---

### Requirements to Structure Mapping

#### Feature Category Mapping (96 Functional Requirements → Files)

**1. Study Calendar Planning (7 FRs: FR-CAL-001 to 007)**
- **Frontend:**
  - Kid view: `app/(kid)/dashboard/components/WeeklyCalendar.tsx`
  - Parent editor: `app/(parent)/calendar/page.tsx`, `CalendarEditor.tsx`
- **Backend:**
  - API: `api/routes/calendar.py` (CRUD for study_sessions)
  - Model: `models/study_session.py`
  - Schema: `schemas/study_session.py`

**2. Subject Management (5 FRs: FR-SUB-001 to 005)**
- **Backend:**
  - API: `api/routes/subjects.py` (GET /api/subjects)
  - Model: `models/subject.py`
  - Schema: `schemas/subject.py`
  - Note: Subjects are static (Math, English, Chinese, Science), seeded in migration

**3. Homework Upload & OCR (7 FRs: FR-HW-001 to 007)**
- **Frontend:**
  - Kid upload: `app/(kid)/homework/upload/page.tsx`, `PhotoUploader.tsx`
  - Parent review: `app/(parent)/homework/page.tsx`, `HomeworkReviewer.tsx`
- **Backend:**
  - API: `api/routes/homework.py` (POST upload, GET results, PUT corrections)
  - Model: `models/homework.py`
  - Service: `services/vision_service.py` (OCR processing)
  - Storage: `storage/homework/` (Railway persistent disk)

**4. Class Notes Upload & Curriculum Tracking (15 FRs: FR-NOTES-001 to 015)**
- **Frontend:**
  - Kid upload: `app/(kid)/notes/upload/page.tsx`, `NotesUploader.tsx`
  - Parent view: `app/(parent)/notes/page.tsx`, `NotesViewer.tsx`, `TopicList.tsx`
- **Backend:**
  - API: `api/routes/class_notes.py` (POST upload, GET notes)
  - API: `api/routes/topics.py` (GET extracted topics)
  - Models: `models/class_note.py`, `models/topic.py`
  - Services: `services/vision_service.py` (OCR), `services/topic_extraction.py` (AI)
  - Storage: `storage/class_notes/` (Railway persistent disk)

**5. Extra Practice Test Generation (6 FRs: FR-TEST-001 to 006)**
- **Frontend:**
  - Test taking: `app/(kid)/test/[test_id]/page.tsx`, `QuestionCard.tsx`
  - Results: `app/(kid)/test/[test_id]/results/page.tsx`
- **Backend:**
  - API: `api/routes/tests.py` (POST generate, GET test)
  - API: `api/routes/questions.py` (GET test questions)
  - Models: `models/test.py`, `models/question.py`
  - Services: `services/test_generation.py` (uses class notes context)
  - Services: `services/gemini_service.py` (AI question generation)

**6. AI-Powered Difficulty Adjustment (7 FRs: FR-DIFF-001 to 007)**
- **Backend:**
  - Service: `services/difficulty_adjustment.py` (4-level algorithm)
  - Used by: `services/test_generation.py` (auto-adjust before generating test)
  - Data source: `models/test_result.py` (historical performance)

**7. Time Limits per Question (7 FRs: FR-TIME-001 to 007)**
- **Frontend:**
  - Timer component: `app/(kid)/test/components/TestTimer.tsx`
  - Client-side countdown: JavaScript `setInterval`
  - Auto-submit: On timer expiration
- **Backend:**
  - Service: `services/test_generation.py` (AI calculates time limits)
  - Validation: `api/routes/test_results.py` (server-side time check on submit)

**8. Test Results & Reporting (7 FRs: FR-RES-001 to 007)**
- **Frontend:**
  - Kid results: `app/(kid)/test/[test_id]/results/page.tsx`, `ResultsSummary.tsx`
  - Parent analytics: `app/(parent)/analytics/page.tsx`, `PerformanceTrends.tsx`
- **Backend:**
  - API: `api/routes/test_results.py` (POST submit, GET results)
  - Model: `models/test_result.py`
  - Service: `services/analytics.py` (aggregations for parent dashboard)

**9. AI Explanations (7 FRs: FR-EXP-001 to 007)**
- **Frontend:**
  - Explanation display: `app/(kid)/test/components/ExplanationCard.tsx`
- **Backend:**
  - API: `api/routes/ai.py` (POST /api/ai/explain)
  - Service: `services/gemini_service.py` (generate explanations)
  - Service: `services/cache_service.py` (cache by question hash)
  - Model: `models/cached_explanation.py`

**10. Gamification System (17 FRs: FR-SCORE-001 to 006, FR-REWARD-001 to 006, FR-LUCKY-001 to 005)**
- **Frontend:**
  - Points display: `app/(kid)/dashboard/components/RewardPoints.tsx`
  - Lucky draw: `app/(kid)/lucky-draw/page.tsx`, `LuckyDrawBox.tsx`, `GiftAnimation.tsx`
- **Backend:**
  - API: `api/routes/rewards.py` (GET points, POST lucky-draw)
  - API: `api/routes/gifts.py` (GET catalog, PUT update)
  - Models: `models/reward.py`, `models/gift.py`
  - Service: `services/gamification.py` (scoring logic, lucky draw probability)

**11. Parent Dashboard (11 FRs: FR-DASH-001 to 011)**
- **Frontend:**
  - Overview: `app/(parent)/dashboard/page.tsx`, `DailyOverview.tsx`, `WeeklyPerformanceGraph.tsx`
  - Subject breakdown: `SubjectBreakdown.tsx`
- **Backend:**
  - API: `api/routes/dashboard.py` (GET aggregated analytics)
  - Service: `services/analytics.py`

#### Cross-Cutting Concerns Mapping

**Authentication & Authorization:**
- **Frontend:**
  - Auth context: `lib/auth-context.tsx` (global state)
  - Login pages: `app/(auth)/login/page.tsx`, `app/(auth)/pin/page.tsx`
  - Auth hook: `hooks/use-auth.ts`
- **Backend:**
  - API: `api/routes/auth.py` (login, logout)
  - Core: `core/security.py` (JWT creation, bcrypt hashing)
  - Dependency: `dependencies.get_current_user` (JWT validation)

**Error Handling:**
- **Frontend:**
  - Global boundary: `app/error.tsx`
  - Shared component: `components/shared/ErrorMessage.tsx`
  - API client: `lib/api-client.ts` (HTTP error handling)
- **Backend:**
  - Exceptions: `core/exceptions.py` (custom HTTP exceptions)
  - Handlers: `app/main.py` (FastAPI exception handlers)

**Loading States:**
- **Frontend:**
  - TanStack Query: Automatic `isLoading`, `isFetching` states
  - Shared component: `components/shared/LoadingSpinner.tsx`

**File Uploads:**
- **Frontend:**
  - Shared uploader: `app/(kid)/homework/components/PhotoUploader.tsx`
  - Reused by: `app/(kid)/notes/components/NotesUploader.tsx`
- **Backend:**
  - Multipart handling: `api/routes/homework.py`, `api/routes/class_notes.py`
  - Storage: `storage/homework/`, `storage/class_notes/` (Railway persistent disk)

**Multilingual Support:**
- **Frontend:**
  - Language context: Future feature (not in MVP)
  - UI text: Hardcoded English initially
- **Backend:**
  - Database: Store question language in `questions.language` field
  - Gemini: Prompt specifies language (English, Chinese)

---

### Integration Points

#### Internal Communication

**Frontend ↔ Backend:**

- **Protocol:** HTTPS REST API (JSON over HTTP)
- **Authentication:** JWT token in `Authorization: Bearer <token>` header
- **Data Format:** JSON with snake_case field names
- **Error Handling:** HTTP status codes + JSON error response
- **File Uploads:** Multipart form data for photos

**Frontend State Flow:**

1. User interaction (button click, form submit)
2. React Hook Form validation (client-side)
3. TanStack Query mutation (`useMutation`)
4. API client (`lib/api-client.ts`) sends request
5. Backend validates (Pydantic), processes, returns response
6. TanStack Query updates cache
7. React components re-render with new data

**Backend Service Flow:**

1. API route receives request (`api/routes/*.py`)
2. FastAPI validates request (Pydantic schema)
3. Route calls service layer (`services/*.py`)
4. Service performs business logic, calls external APIs (Gemini, Vision)
5. Service updates database via ORM (SQLAlchemy async)
6. Service returns result to route
7. Route returns JSON response (Pydantic schema serialization)

#### External Integrations

**Google Gemini API:**
- **Purpose:** AI question generation, explanations, topic extraction
- **Integration Point:** `services/gemini_service.py`
- **Authentication:** `GEMINI_API_KEY` environment variable
- **Rate Limiting:** Free tier ~60 requests/minute
- **Error Handling:** Retry with exponential backoff, fallback to generic error
- **Used By:**
  - `services/test_generation.py` (generate questions)
  - `services/topic_extraction.py` (extract topics from notes)
  - `api/routes/ai.py` (generate explanations)

**Google Cloud Vision API:**
- **Purpose:** OCR for homework and class notes photos
- **Integration Point:** `services/vision_service.py`
- **Authentication:** `GOOGLE_CLOUD_VISION_CREDENTIALS` (JSON key file path)
- **Rate Limiting:** Free tier 1000 requests/month
- **Supported Formats:** JPEG, PNG, HEIC (convert HEIC server-side using Pillow)
- **Error Handling:** Return partial results if processing fails
- **Used By:**
  - `api/routes/homework.py` (OCR homework photos)
  - `api/routes/class_notes.py` (OCR class notes)

**Railway Platform:**
- **Purpose:** Hosting (frontend + backend), PostgreSQL database, file storage
- **Integration Points:**
  - Frontend: Deployed as Node.js service or static site
  - Backend: Deployed as Python service (uvicorn)
  - Database: PostgreSQL addon (connection via `DATABASE_URL` env var)
  - File Storage: Persistent disk mounted at `/app/storage/`
- **Configuration:** Railway dashboard environment variables
- **Deployment:** Auto-deploy on git push (GitHub Actions workflow)

#### Data Flow

**Test Taking Flow (End-to-End):**

1. **Kid navigates to dashboard** (`app/(kid)/dashboard/page.tsx`)
   - TanStack Query: `useQuery(['study-sessions'])` → Fetches from `/api/study-sessions`
   - Displays: Upcoming tests, weekly calendar

2. **Kid clicks "Start Test"** button
   - Frontend: POST `/api/tests` (subject, difficulty auto-selected)
   - Backend: `test_generation.py` → Calls Gemini with class notes topics
   - Backend: Returns test ID, saves to `tests` table
   - Frontend: Navigates to `/test/{test_id}`

3. **Test page loads** (`app/(kid)/test/[test_id]/page.tsx`)
   - TanStack Query: `useQuery(['test', testId])` → Fetches `/api/tests/{test_id}/questions`
   - Backend: Returns questions array (JSON)
   - Frontend: Renders `QuestionCard` components, starts `TestTimer`

4. **Kid answers questions**
   - Local state: Answers stored in React state (`useState`)
   - Timer: Client-side countdown (`setInterval`)
   - Progress bar: Updates as kid completes questions

5. **Kid submits test** (or timer expires)
   - Frontend: POST `/api/tests/{test_id}/submit` with `{answers: {...}, time_taken: 1234}`
   - Backend: `test_results.py` validates time, scores answers
   - Backend: `gamification.py` calculates points, checks for lucky draw
   - Backend: `cache_service.py` fetches explanations (cached or generate new)
   - Backend: Returns `{score, explanations, points_earned, lucky_draw_available}`

6. **Results page** (`app/(kid)/test/[test_id]/results/page.tsx`)
   - Frontend: Fetches `/api/test-results/{test_id}`
   - Displays: Score, celebration animation, explanations, points earned
   - Option: Navigate to lucky draw if available

**Class Notes Upload Flow (End-to-End):**

1. **Kid uploads class notes photo** (`app/(kid)/notes/upload/page.tsx`)
   - Frontend: File selection via `<input type="file">`
   - Frontend: Preview image, show "Upload" button

2. **Kid clicks "Upload"**
   - Frontend: POST `/api/class-notes` (multipart/form-data with photo + subject_id)
   - Backend: `class_notes.py` receives file, saves to `storage/class_notes/`
   - Backend: `vision_service.py` performs OCR on photo
   - Backend: `topic_extraction.py` sends OCR text to Gemini → Extracts topics
   - Backend: Saves topics to `topics` table linked to class note
   - Backend: Returns `{note_id, ocr_text, topics: [...]}`

3. **Parent views class notes** (`app/(parent)/notes/page.tsx`)
   - TanStack Query: `useQuery(['class-notes'])` → Fetches `/api/class-notes`
   - Displays: List of uploaded notes with extracted topics
   - Parent can see: What kid is learning, curriculum progress

4. **Future test generation uses topics**
   - `test_generation.py` queries recent topics from `topics` table
   - Sends topics to Gemini as context: "Generate questions related to [topics]"
   - AI generates curriculum-aware test questions

---

### File Organization Patterns

#### Configuration Files

**Frontend (kongtze-frontend):**

- **Root level:**
  - `package.json` - Dependencies, scripts, project metadata
  - `next.config.ts` - Next.js configuration (API rewrites, env vars, build settings)
  - `tailwind.config.ts` - Tailwind CSS customization (colors, fonts, breakpoints)
  - `tsconfig.json` - TypeScript compiler options
  - `.env.local` - Local environment variables (gitignored)
  - `.env.example` - Template with dummy values (committed)
  - `.eslintrc.json` - ESLint rules
  - `.prettierrc` - Prettier formatting rules

- **Environment variables:**
  ```
  NEXT_PUBLIC_API_URL=https://kongtze-backend.railway.app
  ```

**Backend (kongtze-backend):**

- **Root level:**
  - `requirements.txt` - Python dependencies
  - `requirements-dev.txt` - Dev dependencies (pytest, black, ruff)
  - `alembic.ini` - Alembic migrations config
  - `pyproject.toml` - Black, Ruff, MyPy configuration
  - `.env` - Local environment variables (gitignored)
  - `.env.example` - Template with dummy values (committed)
  - `.python-version` - Python 3.11

- **Environment variables:**
  ```
  DATABASE_URL=postgresql+asyncpg://user:pass@host:5432/kongtze
  SECRET_KEY=your-jwt-secret-key
  GEMINI_API_KEY=your-gemini-api-key
  GOOGLE_CLOUD_VISION_CREDENTIALS=/path/to/credentials.json
  RAILWAY_STORAGE_PATH=/app/storage
  CORS_ORIGINS=https://kongtze-frontend.railway.app
  ```

#### Source Organization

**Frontend:**

- **App Router structure:** File-based routing in `app/` directory
  - Route groups: `(kid)`, `(parent)`, `(auth)` for layout isolation
  - Co-located components: Each route has `components/` subdirectory
  - Shared components: `components/shared/` for truly shared UI

- **Utilities:** `lib/` for non-component code (API client, contexts, utils)
- **Hooks:** `hooks/` for custom React hooks (TanStack Query hooks, timers)
- **Types:** `lib/types.ts` for shared TypeScript interfaces

**Backend:**

- **Domain-driven structure:** Code organized by feature domain
  - `models/` - Database models (one file per table)
  - `schemas/` - Pydantic schemas (one file per domain)
  - `api/routes/` - API endpoints (one file per resource)
  - `services/` - Business logic (one file per service)

- **Core infrastructure:** `core/` for cross-cutting concerns (config, security, database)
- **Dependencies:** `dependencies.py` for FastAPI dependency injection

#### Test Organization

**Frontend:**

- **Co-located tests:** `Component.tsx` + `Component.test.tsx` side-by-side
- **Test framework:** Jest + React Testing Library (Next.js defaults)
- **Test files:** `*.test.tsx` or `*.test.ts` naming convention

**Backend:**

- **Separate `tests/` directory:** Mirrors `app/` structure
  - `test_api/` - API endpoint tests (integration tests)
  - `test_services/` - Service layer tests (unit + integration)
  - `test_models/` - Model tests (unit tests)

- **Test framework:** Pytest
- **Fixtures:** `conftest.py` (test DB setup, async client, mock external APIs)
- **Test naming:** `test_*.py` files, `test_*` functions

#### Asset Organization

**Frontend Static Assets:**

- **`public/` directory:**
  - `images/` - Organized by interface (kid/, parent/)
  - `icons/` - Organized by purpose (rewards/)
  - `fonts/` - Custom fonts if needed

- **Naming convention:** Descriptive, kebab-case
  - ✅ `lucky-draw-box-gold.svg`
  - ❌ `icon1.svg`, `img.png`

**Backend File Storage:**

- **`storage/` directory** (Railway persistent disk):
  - `homework/` - Uploaded homework photos
  - `class_notes/` - Uploaded class notes photos

- **Naming convention:** `{type}_{id}_{timestamp}.{ext}`
  - Example: `homework_123_1737454200.jpg`
  - Example: `note_456_1737454300.jpg`

---

### Development Workflow Integration

#### Development Server Structure

**Frontend Development:**

```bash
cd kongtze-frontend
npm install
npm run dev  # Starts Next.js dev server on http://localhost:3000
```

- **Hot Module Replacement:** Turbopack enables instant updates
- **Environment:** Uses `.env.local` for local API URL
- **API Proxy:** Next.js can proxy `/api/*` to backend during dev (optional)

**Backend Development:**

```bash
cd kongtze-backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
alembic upgrade head  # Run migrations
uvicorn app.main:app --reload  # Starts FastAPI dev server on http://localhost:8000
```

- **Auto-reload:** Uvicorn `--reload` watches for file changes
- **Environment:** Uses `.env` for local DATABASE_URL, API keys
- **API Docs:** Access Swagger UI at http://localhost:8000/docs

#### Build Process Structure

**Frontend Build:**

```bash
npm run build  # Next.js production build
npm start      # Serve production build
```

- **Output:** `.next/` directory (optimized production files)
- **Static optimization:** Next.js auto-optimizes images, fonts, code splitting
- **Environment:** Uses `NEXT_PUBLIC_*` env vars from Railway dashboard

**Backend Build:**

- **No build step** (Python is interpreted)
- **Dependencies:** Railway runs `pip install -r requirements.txt` automatically
- **Migrations:** Railway runs `alembic upgrade head` on deploy (via GitHub Actions)

#### Deployment Structure

**Railway Deployment:**

**1. Frontend Service:**
- **Build command:** `npm run build`
- **Start command:** `npm start`
- **Port:** Auto-assigned by Railway (`$PORT` env var)
- **Environment variables:**
  - `NEXT_PUBLIC_API_URL=https://kongtze-backend.railway.app`

**2. Backend Service:**
- **Build command:** `pip install -r requirements.txt`
- **Start command:** `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- **Port:** Auto-assigned by Railway (`$PORT` env var)
- **Environment variables:**
  - `DATABASE_URL` (Railway PostgreSQL addon, auto-injected)
  - `GEMINI_API_KEY`, `GOOGLE_CLOUD_VISION_CREDENTIALS` (from Railway dashboard)
  - `CORS_ORIGINS=https://kongtze-frontend.railway.app`
- **Migrations:** Auto-run via GitHub Actions workflow before deploy

**3. PostgreSQL Database:**
- **Type:** Railway PostgreSQL addon
- **Attached to:** Backend service
- **Connection:** `DATABASE_URL` env var auto-injected
- **Backups:** Daily automated backups by Railway

**GitHub Actions Workflow** (`.github/workflows/deploy.yml`):

```yaml
# Backend deployment
- Run migrations: alembic upgrade head
- Deploy to Railway: railway up

# Frontend deployment  
- Build: npm run build
- Deploy to Railway: railway up
```

---

**Summary:**

This complete project structure defines:

- ✅ **Two separate repositories** with full directory trees (frontend 50+ files, backend 60+ files)
- ✅ **Clear architectural boundaries** (API, component, service, data layers)
- ✅ **96 functional requirements mapped** to specific files and directories
- ✅ **Integration points** documented (internal communication + external APIs)
- ✅ **Development workflow** (dev servers, build process, deployment)
- ✅ **Technology-specific organization** (Next.js App Router, FastAPI domain-driven design)
- ✅ **Ready for AI agent implementation** with no ambiguity about file locations

---

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**

All 12 core architectural decisions are fully compatible and mutually reinforcing:

- **Technology Stack:** Next.js 15+ (React 19, TypeScript) + Python 3.11+ (FastAPI, SQLAlchemy 2.0 async) + PostgreSQL + Railway → All current stable versions with proven compatibility
- **Async Architecture:** Async SQLAlchemy (Decision 1.2) works seamlessly with async FastAPI route handlers
- **Authentication:** JWT stateless tokens (Decision 2.1) + bcrypt hashing (Decision 2.2) perfectly suited for separate frontend/backend architecture
- **State Management:** React Context + TanStack Query (Decision 4.1) aligns with REST API design and supports caching strategy
- **Form Handling:** React Hook Form + Zod (Decision 4.2) provides TypeScript-safe validation matching Pydantic backend validation
- **No Conflicting Decisions:** Every decision supports and enhances others (e.g., PostgreSQL cache table eliminates Redis complexity while serving single-user needs)

**Pattern Consistency:**

All implementation patterns directly support architectural decisions:

- **Naming Patterns:** snake_case backend (Python/PostgreSQL convention) + PascalCase frontend components (React convention) → Consistent with technology choices
- **Structure Patterns:** Feature-based organization (Next.js App Router co-location) + domain-driven backend (FastAPI best practice) → Aligns with chosen frameworks
- **Format Patterns:** Direct JSON responses + ISO 8601 dates + HTTP status codes → Standard REST API patterns matching FastAPI defaults
- **Communication Patterns:** TanStack Query automatic loading states + React Context auth + JWT localStorage → All patterns work together seamlessly
- **Process Patterns:** Error Boundaries (Next.js) + FastAPI exception handlers + Alembic migrations → Complete error handling and schema evolution strategy

**Structure Alignment:**

Project structure fully supports all architectural decisions:

- **Separate Repositories:** Frontend (kongtze-frontend) and Backend (kongtze-backend) enable independent deployment, clear separation of concerns, and technology optimization
- **Frontend Organization:** App Router feature-based structure supports co-located components, TanStack Query hooks, and React Hook Form patterns
- **Backend Organization:** Domain-driven services (test_generation, gamification, analytics) enable clear boundaries and single-responsibility principle
- **Integration Points:** 24+ REST API endpoints clearly defined, service layer encapsulates external APIs (Gemini, Vision), Railway deployment integrates all pieces
- **No Structural Conflicts:** Every file and directory has a clear purpose, no overlapping responsibilities, boundaries respected

---

### Requirements Coverage Validation ✅

**Epic/Feature Coverage:**

All 96 functional requirements from the PRD are architecturally supported:

**9 Feature Categories Mapped:**

1. **Study Calendar Planning (7 FRs)** ✅
   - Architecture: `study_sessions` table + `/api/study-sessions` CRUD API + Kid dashboard calendar component + Parent calendar editor
   - Coverage: Weekly scheduling, 2-3 sessions/day, parent customization

2. **Subject Management (5 FRs)** ✅
   - Architecture: `subjects` table (static seed) + `/api/subjects` GET endpoint
   - Coverage: Math, English, Chinese, Science with extensible design

3. **Homework Upload & OCR (7 FRs)** ✅
   - Architecture: `homework` table + Vision service (OCR) + `/api/homework` upload endpoint + Railway file storage + Upload components
   - Coverage: Photo upload (JPEG/PNG/HEIC), digitization, parent review/correction

4. **Class Notes Upload & Curriculum Tracking (15 FRs)** ✅
   - Architecture: `class_notes` + `topics` tables + Vision service (OCR) + Gemini topic extraction + `/api/class-notes` + `/api/topics` endpoints
   - Coverage: Daily notes upload, AI topic extraction, curriculum-aware test generation context

5. **Extra Practice Test Generation (6 FRs)** ✅
   - Architecture: `tests` + `questions` tables + Gemini service + Test generation service (uses class notes context) + `/api/tests` endpoints
   - Coverage: AI-generated tests based on difficulty and curriculum context

6. **AI-Powered Difficulty Adjustment (7 FRs)** ✅
   - Architecture: Difficulty adjustment service (4-level algorithm: Beginner → Expert) + Historical test results analysis
   - Coverage: Dynamic scaling based on performance history

7. **Time Limits per Question (7 FRs)** ✅
   - Architecture: Client-side timer component (JavaScript setInterval) + Server-side validation + AI time calculation (Gemini)
   - Coverage: AI-calculated time limits based on difficulty + student history

8. **Test Results & Reporting (7 FRs)** ✅
   - Architecture: `test_results` table + Analytics service + `/api/test-results` + `/api/dashboard` endpoints + Results components + Parent analytics
   - Coverage: Comprehensive breakdowns, accuracy tracking, historical trends

9. **AI Explanations (7 FRs)** ✅
   - Architecture: `cached_explanations` table + Gemini service + Cache service (question hash lookup) + `/api/ai/explain` endpoint
   - Coverage: Step-by-step, age-appropriate (10-year-old), multilingual, cost-optimized caching

**Gamification System (17 FRs)** ✅
- Architecture: `rewards` + `gifts` tables + Gamification service (scoring logic, lucky draw probability) + `/api/rewards` + Lucky draw components
- Coverage: Points per question, speed bonuses, perfect test rewards, daily/weekly tracking, blind box animations, parent-configurable catalog

**Parent Dashboard (11 FRs)** ✅
- Architecture: Dashboard API endpoint (aggregated analytics) + Analytics service + Parent dashboard routes/components
- Coverage: Daily overview, weekly graphs, subject breakdowns, calendar management, class notes viewer, settings

**Functional Requirements Coverage:**

✅ **100% FR Coverage:** All 96 functional requirements have specific architectural support (models, services, APIs, components)

✅ **Cross-Cutting FRs Addressed:**
- Authentication: JWT + bcrypt + Auth context (FR-AUTH category)
- File Uploads: Multipart form data + Railway storage (FR-HW, FR-NOTES)
- AI Integration: Gemini + Vision services + Caching (FR-TEST, FR-EXP, FR-NOTES)
- Real-time: Client-side timers + Server validation (FR-TIME)

**Non-Functional Requirements Coverage:**

✅ **Performance (Target: <2s page load, <1s API response):**
- Async SQLAlchemy for non-blocking I/O during AI/OCR processing
- TanStack Query automatic caching reduces redundant API calls
- PostgreSQL cache table for AI explanations (reduces Gemini API latency)
- Next.js automatic code splitting + image optimization
- Railway CDN for static assets

✅ **Security (Simplified for family app - no GDPR/COPPA):**
- HTTPS encryption (Railway default)
- JWT authentication with bcrypt password hashing
- Student 4-digit PIN (mapped to JWT internally)
- Encrypted photo storage on Railway persistent disk
- CORS configured to allow only frontend origin

✅ **Usability (Kid-friendly + Parent-professional):**
- iPad-first responsive design (Tailwind breakpoints)
- Kid interface: Large buttons (60px min), bright colors, minimal text, celebration animations
- Parent dashboard: Professional theme, detailed analytics, management controls
- React Hook Form provides immediate client-side validation feedback
- Error messages age-appropriate for 10-year-old

✅ **Reliability (99.5% uptime 7am-9pm SGT):**
- Railway infrastructure SLA
- Error boundaries prevent full app crashes
- Graceful degradation if Gemini/Vision APIs unavailable
- Daily automated PostgreSQL backups
- Alembic migrations ensure safe schema evolution

✅ **Scalability (Single-user optimized, future multi-user possible):**
- No over-engineering (no Redis, no complex caching, no rate limiting)
- PostgreSQL cache table sufficient for one student
- Architecture allows future expansion (add multi-tenancy, Redis, rate limiting if needed)
- Decoupled frontend/backend enables independent scaling

---

### Implementation Readiness Validation ✅

**Decision Completeness:**

✅ **All Critical Decisions Documented:**
- **6 Critical Decisions:** Database ORM, Async operations, Authentication, API docs, Environment config, Migrations strategy
- **7 Important Decisions:** Caching, Password hashing, Error handling, File uploads, State management, Form handling, Timers
- **3 Deferred Decisions:** Advanced monitoring (Railway built-in initially), Rate limiting (not needed), CDN (Railway edge sufficient)
- **All with Versions:** SQLAlchemy 2.0+, FastAPI latest, Next.js 15+, React 19+, Python 3.11+, etc.
- **Rationale Provided:** Each decision includes "why" and "alternatives considered"

✅ **Implementation Patterns Comprehensive:**
- **24 Conflict Points Addressed:** Naming (8), Structure (6), Format (5), Process (5)
- **Concrete Examples:** Good examples + anti-patterns for every category
- **Enforcement Guidelines:** Code review checklist, automated tools (ESLint, Black, Ruff), pattern violation process

✅ **Consistency Rules Clear:**
- **10 Mandatory Rules:** snake_case backend, PascalCase components, plural endpoints, ISO 8601 dates, TanStack Query, co-located tests, feature organization, direct responses, error patterns, JWT in localStorage
- **Enforceable:** Specific enough for automated linting and human code review

**Structure Completeness:**

✅ **Complete Project Trees:**
- **Frontend:** 50+ files/directories defined (routes, components, hooks, lib, public assets)
- **Backend:** 60+ files/directories defined (models, schemas, routes, services, tests, migrations)
- **No Placeholders:** Every file has a specific purpose (e.g., `test_generation.py` for AI test creation, `WeeklyCalendar.tsx` for kid calendar view)

✅ **Integration Points Clearly Specified:**
- **24+ API Endpoints:** All CRUD operations mapped (auth, users, subjects, calendar, tests, homework, notes, topics, rewards, gifts, AI, dashboard)
- **Service Boundaries:** Each service is standalone with clear inputs/outputs (Gemini, Vision, Test Generation, Difficulty, Gamification, Analytics, Topic Extraction, Cache)
- **Data Flow Documented:** End-to-end flows for test taking and class notes upload show how data moves through architecture

✅ **Component Boundaries Well-Defined:**
- **Frontend:** Kid interface (iPad-optimized) vs Parent dashboard (laptop-optimized) vs Shared components
- **Backend:** API routes → Services → Models separation with no circular dependencies
- **State Management:** Auth context (global) vs TanStack Query (server state) vs Local state (UI-only)

**Pattern Completeness:**

✅ **All Potential Conflicts Addressed:**
- **Naming:** Backend snake_case, API plural resources, Frontend PascalCase/camelCase/kebab-case by file type
- **Structure:** Feature-based frontend, domain-driven backend, co-located frontend tests, separate backend tests
- **Format:** Direct JSON responses, ISO 8601 dates, HTTP status codes, snake_case JSON fields
- **Communication:** TanStack Query for all API data, React Context for auth, JWT in localStorage
- **Process:** Error boundaries + exception handlers, TanStack Query loading, React Hook Form + Pydantic validation

✅ **Examples Provided for All Major Patterns:**
- Database models (SQLAlchemy async)
- API routes (FastAPI with validation)
- React components (TypeScript, TanStack Query)
- API client (fetch wrapper with auth)
- Error handling (frontend + backend)
- Form validation (Zod + Pydantic)

---

### Gap Analysis Results

**Critical Gaps:** ✅ **NONE FOUND**

All blocking decisions, patterns, and structures are complete and ready for implementation.

**Important Gaps:** ✅ **NONE FOUND**

All significant architectural elements needed for MVP development are fully specified.

**Nice-to-Have Gaps (Non-Blocking):**

These enhancements can be added during or after implementation without affecting architecture:

1. **CI/CD Pipeline Details (Low Priority)**
   - Current: GitHub Actions workflow mentioned for Railway deployment
   - Enhancement: Add specific steps (run tests, lint checks, build validation)
   - Impact: Improves code quality automation
   - Timing: Can configure during first sprint

2. **Monitoring & Observability (Low Priority)**
   - Current: Deferred to post-MVP, Railway built-in monitoring initially
   - Enhancement: Specify logging format (JSON structured logs), error tracking service (Sentry integration)
   - Impact: Better production debugging
   - Timing: Add after MVP launch if needed

3. **Development Tooling (Low Priority)**
   - Current: Black, Ruff, ESLint, Prettier mentioned
   - Enhancement: Pre-commit hooks config, Docker Compose for local dev, Makefile for common commands
   - Impact: Improves developer experience
   - Timing: Can add during setup

4. **API Rate Limiting (Not Needed for MVP)**
   - Current: Deferred (single-user app doesn't require it)
   - Enhancement: Add rate limiting middleware if expanding to multi-user
   - Impact: Prevents API abuse in multi-user scenario
   - Timing: Only needed if scaling beyond family use

5. **Token Refresh Flow (Not Needed for MVP)**
   - Current: Simple JWT without refresh tokens (acceptable for family app)
   - Enhancement: Add refresh token rotation for extended sessions
   - Impact: Better UX for long-lived sessions
   - Timing: Add if JWT expiration becomes annoying

**Gap Resolution:** None of these gaps block implementation. All are post-MVP enhancements or development conveniences that can be added iteratively.

---

### Validation Issues Addressed

✅ **NO BLOCKING ISSUES FOUND**

The architecture passed all validation checks with no critical or important issues:

- **Coherence:** All decisions are compatible, patterns are consistent, structure aligns
- **Coverage:** All 96 FRs + NFRs + cross-cutting concerns architecturally supported
- **Readiness:** Complete decisions, patterns, structure enable consistent AI agent implementation
- **Gaps:** Only nice-to-have enhancements identified, no blocking gaps

---

### Architecture Completeness Checklist

**✅ Requirements Analysis**

- [x] Project context thoroughly analyzed (10-year-old student, IB curriculum, single-user family app, iPad primary device)
- [x] Scale and complexity assessed (Medium-High, 96 FRs, 11-14 components)
- [x] Technical constraints identified (Google Gemini API, Cloud Vision API, Railway hosting, IB PYP alignment)
- [x] Cross-cutting concerns mapped (Authentication, AI integration, File uploads, Gamification, Real-time timers)

**✅ Architectural Decisions**

- [x] Critical decisions documented with versions (6 decisions: ORM, Async, Auth, API docs, Config, Migrations)
- [x] Technology stack fully specified (Next.js 15+, React 19+, Python 3.11+, FastAPI, SQLAlchemy 2.0, PostgreSQL, Railway)
- [x] Integration patterns defined (REST API, JWT auth, Multipart uploads, External APIs: Gemini + Vision)
- [x] Performance considerations addressed (Async I/O, TanStack Query caching, PostgreSQL cache table, Code splitting)

**✅ Implementation Patterns**

- [x] Naming conventions established (Database: snake_case, API: plural + snake_case, Frontend: PascalCase/camelCase/kebab-case)
- [x] Structure patterns defined (Feature-based frontend, Domain-driven backend, Co-located frontend tests, Separate backend tests)
- [x] Communication patterns specified (TanStack Query, React Context, JWT localStorage, ISO 8601 dates, Direct JSON responses)
- [x] Process patterns documented (Error boundaries, FastAPI exception handlers, Form validation, Loading states, Auth flow)

**✅ Project Structure**

- [x] Complete directory structure defined (Frontend: 50+ files, Backend: 60+ files, all routes/components/services/models specified)
- [x] Component boundaries established (Kid interface, Parent dashboard, Shared components, API routes, Services, Models)
- [x] Integration points mapped (24+ API endpoints, Service boundaries, Data flow, External APIs: Gemini + Vision + Railway)
- [x] Requirements to structure mapping complete (All 96 FRs mapped to specific files/directories, Cross-cutting concerns addressed)

---

### Architecture Readiness Assessment

**Overall Status:** ✅ **READY FOR IMPLEMENTATION**

**Confidence Level:** **HIGH**

Based on validation results:
- ✅ Zero blocking issues
- ✅ 100% requirements coverage
- ✅ All critical decisions documented
- ✅ Complete project structure
- ✅ Comprehensive implementation patterns
- ✅ Clear architectural boundaries

**Key Strengths:**

1. **Coherent Decision Set:** All 12 architectural decisions work together seamlessly with no conflicts
2. **Technology Clarity:** Modern, stable tech stack (Next.js 15, FastAPI, PostgreSQL) with verified compatibility
3. **Complete Structure:** Both repositories fully specified with 110+ files/directories mapped
4. **Comprehensive Patterns:** 24 conflict points addressed with concrete examples and anti-patterns
5. **Requirements Traceability:** Every one of 96 FRs directly maps to specific architectural elements
6. **Single-User Optimization:** No over-engineering (no Redis, no microservices, no complex auth), appropriate for family app
7. **AI Agent Readiness:** Clear, unambiguous patterns prevent implementation conflicts between agents
8. **Future-Proof:** Architecture allows scaling to multi-user if needed without fundamental redesign

**Areas for Future Enhancement (Post-MVP):**

1. **Observability:** Add structured logging and error tracking (Sentry) after launch
2. **CI/CD Automation:** Enhance GitHub Actions with test running, lint checks, automated deployment
3. **Development Tooling:** Pre-commit hooks, Docker Compose for local environment consistency
4. **Multi-User Expansion:** Add rate limiting, tenant isolation, user management if scaling beyond family
5. **Advanced Caching:** Add Redis if cache requirements grow beyond PostgreSQL table (unlikely for single user)

---

### Implementation Handoff

**AI Agent Guidelines:**

When implementing the Kongtze project, AI agents MUST:

1. **Follow All Architectural Decisions Exactly**
   - Use async SQLAlchemy with Code-First models and Alembic migrations (Decisions 1.1, 1.2, 5.2)
   - Implement JWT stateless authentication with bcrypt password hashing (Decisions 2.1, 2.2)
   - Generate API documentation using FastAPI auto-generated OpenAPI at `/docs` (Decision 3.1)
   - Handle errors with HTTP status codes + JSON responses (Decision 3.2)
   - Use multipart form data for file uploads (Decision 3.3)
   - Manage frontend state with React Context + TanStack Query (Decision 4.1)
   - Handle forms with React Hook Form + Zod validation (Decision 4.2)
   - Implement timers client-side with server-side validation (Decision 4.3)
   - Configure environment with .env files + Railway dashboard (Decision 5.1)
   - Cache AI explanations in PostgreSQL table (Decision 1.3)

2. **Use Implementation Patterns Consistently**
   - **Naming:** snake_case for backend (database, API, Python), PascalCase for React components, kebab-case for utilities
   - **API Endpoints:** Plural resource names (`/api/users/{id}`, `/api/tests`)
   - **Dates:** ISO 8601 strings in JSON (`"2026-01-21T10:30:00Z"`)
   - **Responses:** Direct JSON (no wrapper), metadata wrapper only for pagination
   - **Tests:** Co-locate frontend tests (`Component.test.tsx`), separate backend tests (`tests/test_api/`)
   - **Organization:** Feature-based frontend (App Router co-location), domain-driven backend (services by domain)

3. **Respect Project Structure and Boundaries**
   - **Frontend:** Follow `kongtze-frontend/` directory tree (50+ files specified)
   - **Backend:** Follow `kongtze-backend/` directory tree (60+ files specified)
   - **API Boundaries:** Use only documented endpoints (24+ endpoints specified)
   - **Service Boundaries:** Services never import each other directly (dependency injection via routes)
   - **Data Boundaries:** All database access via SQLAlchemy async ORM (no raw SQL except complex analytics)

4. **Refer to This Document for All Architectural Questions**
   - **Naming Conventions:** See "Naming Patterns" section with examples and anti-patterns
   - **Project Structure:** See "Complete Project Directory Structure" for file locations
   - **API Design:** See "API Boundaries" for endpoint patterns and formats
   - **Requirements Mapping:** See "Requirements to Structure Mapping" for FR → file mapping
   - **Integration Points:** See "Data Flow" for end-to-end process flows

**First Implementation Priority:**

**Step 1: Initialize Repositories**

```bash
# Frontend
npx create-next-app@latest kongtze-frontend \
  --typescript --tailwind --eslint --app --turbopack --no-src-dir
cd kongtze-frontend
npm install @tanstack/react-query react-hook-form zod @hookform/resolvers/zod
# Create project structure per architecture document

# Backend
git clone https://github.com/rafsaf/minimal-fastapi-postgres-template kongtze-backend
cd kongtze-backend
rm -rf .git && git init
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
# Adapt structure to Kongtze domains per architecture document
```

**Step 2: Set Up Railway**

1. Create Railway project
2. Add PostgreSQL addon
3. Deploy backend service (configure `DATABASE_URL`, `GEMINI_API_KEY`, `GOOGLE_CLOUD_VISION_CREDENTIALS`, `CORS_ORIGINS`)
4. Deploy frontend service (configure `NEXT_PUBLIC_API_URL`)

**Step 3: Implement Core Models** (Backend)

Based on ERD in PRD, create SQLAlchemy models in this order:
1. `models/user.py` (parent + student)
2. `models/subject.py` (Math, English, Chinese, Science)
3. `models/study_session.py` (calendar)
4. `models/test.py`, `models/question.py`, `models/test_result.py`
5. `models/homework.py`, `models/class_note.py`, `models/topic.py`
6. `models/reward.py`, `models/gift.py`
7. `models/cached_explanation.py`

**Step 4: Run Initial Migration**

```bash
alembic revision --autogenerate -m "Initial schema"
# Review generated migration
alembic upgrade head
```

**Step 5: Implement Authentication** (Backend + Frontend)

- Backend: `api/routes/auth.py` (login endpoint) + `core/security.py` (JWT + bcrypt)
- Frontend: `lib/auth-context.tsx` + `app/(auth)/login/page.tsx`

**Step 6: Implement First Feature** (Test full stack)

Choose simplest feature to validate end-to-end flow:
- **Subjects API** (backend: `api/routes/subjects.py`)
- **Kid Dashboard** (frontend: `app/(kid)/dashboard/page.tsx` fetches subjects)

This validates: Database → API → Frontend → TanStack Query → Component rendering

**Next Steps After Core Setup:**

Proceed with implementation in order:
1. Study Calendar (FR-CAL category)
2. Test Generation (FR-TEST category)
3. Homework Upload (FR-HW category)
4. Class Notes Upload (FR-NOTES category)
5. Gamification (FR-SCORE, FR-REWARD, FR-LUCKY)
6. Parent Dashboard (FR-DASH category)

**Reference:**
- Architecture patterns: See "Implementation Patterns & Consistency Rules"
- Project structure: See "Complete Project Directory Structure"
- API design: See "API Boundaries"
- Requirements: See `_bmad-output/planning-artifacts/prd.md`