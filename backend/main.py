"""多语种在线学习平台 · LinguaGo FastAPI 应用入口。"""
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from . import database, seed
from .routers import achievements, auth, community, courses, progress

BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "frontend"

app = FastAPI(title="LinguaGo 多语种学习平台")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def no_store_cache(request, call_next):
    response = await call_next(request)
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    return response


@app.on_event("startup")
def startup() -> None:
    database.init_db()
    seed.seed_if_needed()


app.include_router(auth.router)
app.include_router(courses.router)
app.include_router(progress.router)
app.include_router(achievements.router)
app.include_router(community.router)


@app.get("/api/health")
def health():
    return {"status": "ok"}


if FRONTEND_DIR.exists():
    app.mount("/", StaticFiles(directory=str(FRONTEND_DIR), html=True), name="frontend")