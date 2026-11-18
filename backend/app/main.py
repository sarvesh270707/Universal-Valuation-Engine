from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import time
import os
import logging

from backend.app.core.config import settings
from backend.app.core.init_db import init_db
from backend.app.api.v1.endpoints.valuation_api import router as valuation_router

# Initialize database tables on startup
init_db()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("UniversalDCFEngine")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Universal Multi-Company Financial Valuation & DCF Engine API supporting 21 Sectors, Dual DCF, DDM, NAV, SOTP, and Comps.",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Request Timing & Diagnostic Middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.perf_counter()
    response = await call_next(request)
    process_time = time.perf_counter() - start_time
    response.headers["X-Process-Time"] = f"{process_time:.4f}s"
    response.headers["X-Engine"] = "Universal-DCF-v1"
    return response

# Global Exception Handler
@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global unhandled exception on {request.url.path}: {str(exc)}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "Internal financial engine calculation error", "error": str(exc)}
    )

# Include API v1 Router
app.include_router(valuation_router, prefix=settings.API_V1_STR)

# Static Files & Web Portal Mount
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/portal", StaticFiles(directory=static_dir, html=True), name="portal")

@app.get("/app", tags=["Frontend"])
def serve_portal():
    index_file = os.path.join(static_dir, "index.html")
    return FileResponse(index_file)

# Base Root Endpoint
@app.get("/", tags=["Root"])
def root():
    return {
        "engine": settings.PROJECT_NAME,
        "version": "1.0.0",
        "status": "ONLINE",
        "interactive_portal": "/app",
        "api_docs": "/docs",
        "supported_sectors": 21,
        "methodologies": ["FCFF_DCF", "FCFE_DCF", "DDM", "RESIDUAL_INCOME", "NAV", "SOTP", "COMPS", "EMBEDDED_VALUE"]
    }

# Health Check Endpoint
@app.get("/health", tags=["Health"])
def health_check():
    return {
        "status": "HEALTHY",
        "database": "CONNECTED",
        "timestamp": time.time(),
        "environment": settings.ENVIRONMENT
    }
