from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import os

# Import your route modules
from backend.routes.auth_routes import router as auth_router
from backend.routes.ai_routes import router as ai_router

app = FastAPI(title="AI Age Recognition")

# -------------------------
# CORS Configuration
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000", "http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------
# API ROUTES (imported)
# -------------------------
# MUST come BEFORE the Vue catch-all

app.include_router(auth_router)
app.include_router(ai_router)

@app.get("/health")
def health_check():
    return JSONResponse({"status": "ok", "message": "API is running"})


# -------------------------
# FRONTEND (placed LAST)
# -------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST_DIR = os.path.join(BASE_DIR, "frontend", "age_recognition", "dist")

if os.path.exists(DIST_DIR):
    # Static assets (JS, CSS)
    app.mount("/assets", StaticFiles(directory=os.path.join(DIST_DIR, "assets")), name="assets")

    # Root
    @app.get("/")
    async def serve_index():
        return FileResponse(os.path.join(DIST_DIR, "index.html"))

    # Catch-all for Vue Router
    @app.get("/{full_path:path}")
    async def catch_all(full_path: str):
        return FileResponse(os.path.join(DIST_DIR, "index.html"))
