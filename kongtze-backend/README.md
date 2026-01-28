# Kongtze Backend

AI-Powered Education Platform - Backend API

## Tech Stack

- **Runtime:** Python 3.11+
- **Framework:** FastAPI (async)
- **ORM:** SQLAlchemy 2.0+ (async with Mapped syntax)
- **Migrations:** Alembic
- **Validation:** Pydantic V2
- **Database:** PostgreSQL (asyncpg driver)
- **Authentication:** JWT (HS256) + bcrypt
- **AI Services:** Google Gemini API, Google Cloud Vision API

## Getting Started

### Install Dependencies

```bash
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt -r requirements-dev.txt
```

### Environment Setup

1. Copy `.env.example` to `.env`
2. Update values in `.env` with your configuration

### Run Development Server

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API will be available at [http://localhost:8000](http://localhost:8000)

API Documentation: [http://localhost:8000/docs](http://localhost:8000/docs)

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Review the generated migration file
# Then apply it
alembic upgrade head
```

## Project Structure

```
app/
├── core/
│   ├── config.py           # Settings (Pydantic Settings)
│   ├── security.py         # JWT + bcrypt utilities
│   └── database.py         # Async SQLAlchemy setup
├── models/                 # SQLAlchemy models
│   ├── user.py
│   ├── subject.py
│   ├── test.py
│   └── ...
├── schemas/                # Pydantic schemas
├── api/routes/             # API endpoints
│   ├── auth.py
│   ├── tests.py
│   └── ...
├── services/               # Business logic
│   ├── gemini_service.py
│   ├── vision_service.py
│   └── ...
└── main.py                 # FastAPI application
alembic/                    # Database migrations
tests/                      # Pytest tests
storage/                    # File uploads
```

## Architecture

See `../_bmad-output/planning-artifacts/architecture.md` for complete architectural decisions.

See `../_bmad-output/project-context.md` for critical implementation rules.

## API Documentation

FastAPI automatically generates interactive API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

```bash
pytest
```
