"""
FastAPI Backend for Claude Code Project Template
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime

app = FastAPI(
    title="Claude Code Project Template API",
    description="Production-ready FastAPI backend with Next.js frontend integration",
    version="1.0.0"
)

# CORS configuration for Next.js frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Next.js dev server
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Claude Code Project Template API",
        "status": "running",
        "docs": "/docs"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "message": "FastAPI backend is running",
        "timestamp": datetime.now().isoformat()
    }

@app.get("/api/hello")
async def hello(name: str = "World"):
    """Example API endpoint"""
    return {
        "message": f"Hello, {name}!",
        "timestamp": datetime.now().isoformat()
    }
