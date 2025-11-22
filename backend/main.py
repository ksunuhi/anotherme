"""
AnotherMe - Birthday Social Network Platform
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth

# Create database tables (only needed if not using schema.sql)
# Base.metadata.create_all(bind=engine)

app = FastAPI(
    title=settings.APP_NAME,
    description="Connect with your birthday twins",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "Welcome to AnotherMe API",
        "version": "1.0.0",
        "status": "running"
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy"}


# Register API routers
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])

# Additional routers will be added here:
# app.include_router(users.router, prefix="/api/users", tags=["Users"])
# app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
# app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
# app.include_router(friends.router, prefix="/api/friends", tags=["Friends"])
# app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
