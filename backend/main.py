"""
AnotherMe - Birthday Social Network Platform
Main FastAPI application entry point
"""
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.exceptions import RequestValidationError
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.exceptions import HTTPException as StarletteHTTPException
from app.core.config import settings
from app.core.database import engine, Base
from app.api import auth, posts, users, friends, messages, contact, statistics
import os

# Create database tables (only needed if not using schema.sql)
# Base.metadata.create_all(bind=engine)

# Initialize rate limiter
limiter = Limiter(key_func=get_remote_address)

app = FastAPI(
    title=settings.APP_NAME,
    description="Connect with your birthday twins",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add rate limiter to app state
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.get_allowed_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        # Security headers
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"

        # Content Security Policy - relaxed for development
        # Adjust for production with your actual domain
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "script-src 'self' 'unsafe-inline' https://cdn.tailwindcss.com https://unpkg.com; "
            "style-src 'self' 'unsafe-inline'; "
            "img-src 'self' data: blob:; "
            "font-src 'self' data:; "
            "connect-src 'self'"
        )

        return response


app.add_middleware(SecurityHeadersMiddleware)


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
app.include_router(posts.router, prefix="/api/posts", tags=["Posts"])
app.include_router(users.router, prefix="/api/users", tags=["Users"])
app.include_router(friends.router, prefix="/api/friends", tags=["Friends"])
app.include_router(messages.router, prefix="/api/messages", tags=["Messages"])
app.include_router(contact.router, prefix="/api/contact", tags=["Contact"])
app.include_router(statistics.router, prefix="/api/statistics", tags=["Statistics"])

# Mount static files for uploads (profile pictures)
# Ensure uploads directory exists
os.makedirs("uploads/profile_pictures", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")


# Custom error handlers
@app.exception_handler(StarletteHTTPException)
async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Custom handler for HTTP exceptions
    Returns custom error pages for 404 and 500 errors
    """
    # For API requests, return JSON
    if request.url.path.startswith("/api/"):
        return {
            "detail": exc.detail,
            "status_code": exc.status_code
        }

    # For page requests, return custom HTML error pages
    if exc.status_code == 404:
        error_page_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pages", "404.html")
        if os.path.exists(error_page_path):
            return FileResponse(error_page_path, status_code=404)

    # For other errors, return default JSON
    return {
        "detail": exc.detail,
        "status_code": exc.status_code
    }


@app.exception_handler(Exception)
async def custom_server_error_handler(request: Request, exc: Exception):
    """
    Custom handler for 500 Internal Server Errors
    Returns custom error page for non-API requests
    """
    # For API requests, return JSON
    if request.url.path.startswith("/api/"):
        return {
            "detail": "Internal server error",
            "status_code": 500
        }

    # For page requests, return custom HTML error page
    error_page_path = os.path.join(os.path.dirname(__file__), "..", "frontend", "pages", "500.html")
    if os.path.exists(error_page_path):
        return FileResponse(error_page_path, status_code=500)

    # Fallback to JSON
    return {
        "detail": "Internal server error",
        "status_code": 500
    }


# Additional routers to be added:
# app.include_router(groups.router, prefix="/api/groups", tags=["Groups"])
