from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api import auth, subjects, study_sessions, tests, homework, class_notes, rewards

app = FastAPI(
    title="Kongtze API",
    description="AI-Powered Education Platform for Students",
    version="0.1.0",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router, prefix=settings.API_PREFIX)
app.include_router(subjects.router, prefix=settings.API_PREFIX)
app.include_router(study_sessions.router, prefix=settings.API_PREFIX)
app.include_router(tests.router, prefix=settings.API_PREFIX)
app.include_router(homework.router, prefix=settings.API_PREFIX)
app.include_router(class_notes.router, prefix=settings.API_PREFIX)
app.include_router(rewards.router, prefix=settings.API_PREFIX)

@app.get("/")
async def root():
    return {"message": "Kongtze API is running", "version": "0.1.0"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
