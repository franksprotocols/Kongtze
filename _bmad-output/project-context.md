---
project_name: 'Kongtze'
user_name: 'Frankhu'
date: '2026-01-21'
sections_completed: ['technology_stack', 'language_rules', 'framework_rules', 'testing_rules', 'code_quality', 'critical_rules']
existing_patterns_found: 24
---

# Project Context for AI Agents

_This file contains critical rules and patterns that AI agents must follow when implementing code in this project. Focus on unobvious details that agents might otherwise miss._

**Reference Architecture:** `_bmad-output/planning-artifacts/architecture.md`

---

## Technology Stack & Versions

**Frontend Stack:**
- Node.js ≥18.0.0
- Next.js 15+ (App Router, Turbopack)
- React 19+
- TypeScript (strict mode)
- Tailwind CSS 4
- TanStack Query v5 (React 19 compatible)
- React Hook Form v7+ + Zod v3+
- Railway deployment

**Backend Stack:**
- Python ≥3.11
- FastAPI (async web framework)
- SQLAlchemy 2.0+ (async support, `mapped_column` syntax)
- Alembic (migrations)
- Pydantic V2
- asyncpg (PostgreSQL async driver)
- PyJWT (HS256 algorithm)
- passlib (bcrypt backend)
- Google Generative AI SDK ≥0.8.3
- Google Cloud Vision SDK ≥3.8.0
- Railway deployment

**Infrastructure:**
- PostgreSQL (Railway addon)
- Railway file storage (persistent disk at `/app/storage/`)
- No Redis (use PostgreSQL cache tables)

**Critical Version Requirements:**
- SQLAlchemy MUST be 2.0+ for `Mapped[T]` and `mapped_column` syntax
- Next.js MUST be 15+ for App Router + React 19 compatibility
- Python MUST be 3.11+ for modern async/await and type hints
- TanStack Query MUST be v5 (not v4) for React 19 compatibility

---

## Critical Implementation Rules

### Language-Specific Rules

**Python (Backend):**

1. **ALWAYS use async/await:**
   - All database operations: `async def`, `await session.execute()`
   - All FastAPI route handlers: `async def`
   - SQLAlchemy sessions: `AsyncSession`, never sync sessions
   - External API calls (Gemini, Vision): `async` functions

2. **Use modern SQLAlchemy 2.0 syntax:**
   ```python
   # ✅ CORRECT - SQLAlchemy 2.0
   class User(Base):
       user_id: Mapped[int] = mapped_column(primary_key=True)
       email: Mapped[str] = mapped_column(unique=True)

   # ❌ WRONG - Old SQLAlchemy 1.x syntax
   class User(Base):
       user_id = Column(Integer, primary_key=True)
   ```

3. **Type hints are MANDATORY:**
   - All function parameters and return types
   - Pydantic models with field types
   - SQLAlchemy `Mapped[T]` annotations

4. **snake_case for everything:**
   - File names: `test_generation.py`, `gemini_service.py`
   - Functions: `def get_user_data()`, `async def generate_test()`
   - Variables: `user_id`, `test_score`, `ai_explanation`
   - Database columns: `user_id`, `created_at`, `test_result_id`

**TypeScript (Frontend):**

1. **ALWAYS use TypeScript strict mode:**
   - No `any` types (use `unknown` if truly unknown)
   - Explicit return types on functions
   - Proper typing for all props and state

2. **Use Next.js 15 App Router patterns:**
   - Server Components by default (no `"use client"` unless needed)
   - `"use client"` ONLY for: hooks, event handlers, browser APIs, state
   - File-based routing in `app/` directory
   - Route groups: `(kid)/`, `(parent)/`, `(auth)/`

3. **camelCase for variables, PascalCase for components:**
   ```typescript
   // ✅ CORRECT
   const userId = 1;
   function getUserData() { }
   export function UserCard() { }

   // ❌ WRONG
   const user_id = 1;
   function get_user_data() { }
   export function userCard() { }
   ```

4. **kebab-case for utility files:**
   - ✅ `api-client.ts`, `format-date.ts`, `auth-utils.ts`
   - ❌ `apiClient.ts`, `formatDate.ts`, `authUtils.ts`

### Framework-Specific Rules

**Next.js (Frontend):**

1. **Co-locate components with routes:**
   ```
   app/(kid)/dashboard/
     ├── page.tsx              # Route component
     └── components/           # Components used ONLY by this route
         ├── WeeklyCalendar.tsx
         └── WeeklyCalendar.test.tsx
   ```

2. **Use TanStack Query for ALL server state:**
   ```typescript
   // ✅ CORRECT - TanStack Query
   const { data, isLoading } = useQuery({
     queryKey: ['tests', userId],
     queryFn: () => apiClient.getTests(userId),
   });

   // ❌ WRONG - Manual useState for API data
   const [data, setData] = useState(null);
   useEffect(() => { fetch(...).then(setData) }, []);
   ```

3. **Use React Hook Form + Zod for forms:**
   ```typescript
   const schema = z.object({
     email: z.string().email(),
     password: z.string().min(8),
   });

   const { register, handleSubmit } = useForm({
     resolver: zodResolver(schema),
   });
   ```

4. **NEVER use inline styles - use Tailwind classes:**
   - ✅ `<div className="flex items-center gap-4">`
   - ❌ `<div style={{ display: 'flex', alignItems: 'center' }}>`

**FastAPI (Backend):**

1. **Use Pydantic for ALL request/response validation:**
   ```python
   # ✅ CORRECT
   class TestCreate(BaseModel):
       subject_id: int
       difficulty_level: int = Field(ge=1, le=4)

   @router.post("/api/tests")
   async def create_test(test: TestCreate): ...

   # ❌ WRONG - Unvalidated dict
   @router.post("/api/tests")
   async def create_test(test: dict): ...
   ```

2. **Use custom exception classes, not generic exceptions:**
   ```python
   # ✅ CORRECT
   class TestNotFoundError(HTTPException):
       def __init__(self):
           super().__init__(status_code=404, detail="Test not found")

   raise TestNotFoundError()

   # ❌ WRONG
   raise Exception("Test not found")
   ```

3. **Use dependency injection for database sessions:**
   ```python
   async def get_db():
       async with AsyncSession(engine) as session:
           yield session

   @router.get("/api/tests")
   async def get_tests(db: AsyncSession = Depends(get_db)):
       result = await db.execute(select(Test))
       return result.scalars().all()
   ```

4. **Auto-generate OpenAPI docs - access at `/docs`:**
   - FastAPI generates Swagger UI automatically
   - Add docstrings to routes for better docs
   - Use Pydantic schema descriptions for field documentation

### Testing Rules

**Frontend Tests:**

1. **Co-locate tests with components:**
   - ✅ `UserCard.tsx` + `UserCard.test.tsx` side-by-side
   - ❌ Separate `tests/components/` directory

2. **Use React Testing Library (not Enzyme):**
   - Query by user-visible text, not implementation details
   - `getByRole`, `getByLabelText`, `getByText`
   - Test user interactions, not internal state

3. **Mock TanStack Query in tests:**
   - Use `QueryClient` with default options for tests
   - Mock API responses at the `apiClient` level

**Backend Tests:**

1. **Separate tests directory mirroring app structure:**
   ```
   tests/
     ├── test_api/
     │   ├── test_auth.py
     │   └── test_tests.py
     ├── test_services/
     │   └── test_gemini_service.py
     └── conftest.py  # Pytest fixtures
   ```

2. **Use pytest fixtures for test DB:**
   - Create test database for each test session
   - Use async test client (`httpx.AsyncClient`)
   - Mock external APIs (Gemini, Vision) - don't call real APIs in tests

3. **Test naming: `test_*` functions:**
   - ✅ `def test_get_user_returns_user_data():`
   - ❌ `def check_user_endpoint():`

### Code Quality & Style Rules

**Naming Conventions (CRITICAL):**

1. **Database/API use snake_case:**
   - Tables: `users`, `test_results`, `class_notes`
   - Columns: `user_id`, `created_at`, `test_score`
   - JSON fields: `{"user_id": 1, "created_at": "2026-01-21T10:30:00Z"}`
   - API endpoints: `/api/users/{user_id}`, `/api/test-results`

2. **Frontend uses PascalCase/camelCase/kebab-case by type:**
   - React components: `UserCard.tsx`, `TestTimer.tsx`
   - Variables/functions: `userId`, `getUserData()`
   - Utility files: `api-client.ts`, `format-date.ts`
   - Constants: `API_BASE_URL`, `MAX_UPLOAD_SIZE`

3. **Use PLURAL resource names for REST endpoints:**
   - ✅ `/api/users/{id}`, `/api/tests`, `/api/rewards`
   - ❌ `/api/user/{id}`, `/api/test`, `/api/reward`

**Error Handling:**

1. **Frontend: Error Boundaries + TanStack Query error states:**
   ```typescript
   // Global error boundary
   // app/error.tsx

   // Component-level error handling
   const { data, error, isError } = useQuery(...);
   if (isError) return <ErrorMessage message={error.message} />;
   ```

2. **Backend: Custom exceptions + FastAPI handlers:**
   ```python
   @app.exception_handler(TestNotFoundError)
   async def test_not_found_handler(request, exc):
       return JSONResponse(
           status_code=exc.status_code,
           content={"detail": exc.detail, "error_code": "TEST_NOT_FOUND"}
       )
   ```

**Date/Time Handling:**

1. **ALWAYS use ISO 8601 strings in JSON:**
   - ✅ `"created_at": "2026-01-21T10:30:00Z"` (datetime)
   - ✅ `"test_date": "2026-01-21"` (date only)
   - ❌ `"created_at": 1737454200` (Unix timestamp)
   - Pydantic automatically serializes Python `datetime` to ISO 8601

**API Response Format:**

1. **Direct responses (no wrapper):**
   ```json
   // ✅ CORRECT - Direct response
   GET /api/users/1
   {"user_id": 1, "name": "Student", "email": "..."}

   // ❌ WRONG - Unnecessary wrapper
   {"data": {"user_id": 1, ...}, "error": null}
   ```

2. **Metadata wrapper ONLY for pagination:**
   ```json
   GET /api/tests?page=1&page_size=20
   {
     "items": [{...}, {...}],
     "total": 50,
     "page": 1,
     "page_size": 20
   }
   ```

### Critical Don't-Miss Rules

**Authentication:**

1. **JWT stored in localStorage (frontend):**
   ```typescript
   // ✅ CORRECT
   localStorage.setItem('auth_token', token);

   // Include in all API requests
   headers: {
     'Authorization': `Bearer ${getToken()}`,
   }
   ```

2. **bcrypt for password hashing (backend):**
   ```python
   from passlib.context import CryptContext

   pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
   hashed = pwd_context.hash(plain_password)
   ```

**File Uploads:**

1. **Use multipart/form-data (not base64 JSON):**
   ```python
   @router.post("/api/homework")
   async def upload_homework(
       homework_photo: UploadFile,
       subject_id: int = Form(...),
   ):
       # Save to Railway storage: /app/storage/homework/
       file_path = f"/app/storage/homework/homework_{id}_{timestamp}.jpg"
   ```

**Database Migrations:**

1. **ALWAYS review auto-generated Alembic migrations:**
   ```bash
   # Generate migration
   alembic revision --autogenerate -m "Add class notes"

   # ⚠️ REVIEW alembic/versions/*.py before applying!
   # Check for: dropped columns, data loss, FK constraints

   # Apply migration
   alembic upgrade head
   ```

**State Management:**

1. **React Context for global state, TanStack Query for server state:**
   ```typescript
   // ✅ React Context for auth
   const AuthContext = createContext<AuthContextType>(...)

   // ✅ TanStack Query for API data
   const { data } = useQuery(['tests'], apiClient.getTests)

   // ❌ WRONG - useState for API data
   const [tests, setTests] = useState([]);
   ```

**Async Patterns:**

1. **Backend: ALL database operations are async:**
   ```python
   # ✅ CORRECT
   async def get_user(user_id: int, db: AsyncSession):
       result = await db.execute(select(User).where(User.user_id == user_id))
       return result.scalar_one_or_none()

   # ❌ WRONG - Sync database call
   def get_user(user_id: int, db: Session):
       return db.query(User).filter(User.user_id == user_id).first()
   ```

2. **Frontend: Client-side timers, server-side validation:**
   ```typescript
   // Client-side countdown timer
   const [secondsRemaining, setSecondsRemaining] = useState(timeLimit);
   useEffect(() => {
     const interval = setInterval(() => {
       setSecondsRemaining(prev => prev - 1);
     }, 1000);
     return () => clearInterval(interval);
   }, []);

   // Server validates elapsed time on submit
   // POST /api/tests/{id}/submit with {answers, time_taken}
   ```

**Code Organization:**

1. **Feature-based frontend, domain-driven backend:**
   ```
   # ✅ Frontend - Feature-based
   app/(kid)/dashboard/components/WeeklyCalendar.tsx

   # ✅ Backend - Domain-driven
   app/services/test_generation.py
   app/services/gamification.py

   # ❌ WRONG - Type-based organization
   components/all-components-here/
   services/all-services-here/
   ```

**Anti-Patterns to AVOID:**

1. ❌ **NEVER use Redis** - Use PostgreSQL cache tables for single-user app
2. ❌ **NEVER use sync SQLAlchemy** - Must be async with `AsyncSession`
3. ❌ **NEVER use wrapper responses** - Direct JSON responses only (except pagination)
4. ❌ **NEVER use `any` type in TypeScript** - Use proper types or `unknown`
5. ❌ **NEVER hardcode API URLs** - Use environment variables
6. ❌ **NEVER skip Pydantic validation** - All API inputs must be validated
7. ❌ **NEVER use manual state for API data** - Always use TanStack Query
8. ❌ **NEVER commit `.env` files** - Only commit `.env.example`
9. ❌ **NEVER use old SQLAlchemy syntax** - Must use 2.0 `Mapped[T]` syntax
10. ❌ **NEVER apply Alembic migrations without review** - Always check generated code

---

**For complete architectural decisions, patterns, and project structure, refer to:**
`_bmad-output/planning-artifacts/architecture.md`
