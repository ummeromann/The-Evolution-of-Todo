"""
FastAPI application entry point.

This module creates and configures the main FastAPI application with:
- CORS middleware for cross-origin requests from the Next.js frontend
- API route handlers for health checks and task management
- OpenAPI documentation at /docs and /redoc
- Global error handling and validation

Environment Configuration:
    See backend/.env.example for required environment variables:
    - DATABASE_URL: Neon PostgreSQL connection string
    - BETTER_AUTH_SECRET: JWT secret key (must match frontend)
    - CORS_ORIGINS: Comma-separated list of allowed origins
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.config import settings
from app.api.routes import health_router, tasks_router, auth_router, chat_router

app = FastAPI(
    title="Todo API",
    description="RESTful API for multi-user task management with JWT authentication",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS middleware configuration
# Allows the Next.js frontend to make cross-origin requests to this API
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(health_router)
app.include_router(tasks_router)
app.include_router(auth_router)
app.include_router(chat_router)


@app.get("/")
async def root():
    """
    Root endpoint providing API information.

    Returns basic API metadata and links to documentation.
    This is useful for API discovery and quick verification.

    Returns:
        dict: API name, version, and documentation links

    Example Response:
        {
            "message": "Todo API",
            "version": "1.0.0",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    """
    return {
        "message": "Todo API",
        "version": "1.0.0",
        "docs": "/docs",
        "redoc": "/redoc",
    }


# Global exception handlers for consistent error responses
@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    """
    Handle HTTP exceptions with consistent response format.
    """
    error_codes = {
        401: "UNAUTHORIZED",
        403: "FORBIDDEN",
        404: "NOT_FOUND",
        500: "INTERNAL_SERVER_ERROR",
    }
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "code": error_codes.get(exc.status_code, "ERROR"),
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle validation errors with detailed error information.
    """
    return JSONResponse(
        status_code=422,
        content={
            "detail": [
                {
                    "loc": list(error["loc"]),
                    "msg": error["msg"],
                    "type": error["type"],
                }
                for error in exc.errors()
            ],
            "code": "VALIDATION_ERROR",
        },
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Handle unexpected exceptions with a generic error response.
    """
    import traceback
    print(f"ERROR: {type(exc).__name__}: {exc}")
    traceback.print_exc()
    return JSONResponse(
        status_code=500,
        content={
            "detail": "An unexpected error occurred",
            "code": "INTERNAL_SERVER_ERROR",
        },
    )
