import asyncio

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.auth import router as auth_router
from app.api.chat import router as chat_router
from app.api.voice import router as voice_router
from app.api.tasks import router as tasks_router
from app.api.workflows import router as workflows_router
from app.api.scheduler import router as scheduler_router
from app.api.integrations import router as integrations_router
from app.api.memory import router as memory_router
from app.api.notifications import router as notifications_router
from app.api.security import router as security_router
from app.api.timer import router as timer_router
from app.api.approval import router as approval_router
from app.api.booking import router as booking_router
from app.api.shopping import router as shopping_router


app = FastAPI(
    title="AI Buddy",
    description=(
        "An Autonomous AI Agent for "
        "Intelligent Digital Task Automation"
    ),
    version="1.0.0"
)


# ============================================================
# CORS CONFIGURATION
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# API ROUTERS
# ============================================================

app.include_router(
    auth_router,
    prefix="/api"
)

app.include_router(
    chat_router,
    prefix="/api"
)

app.include_router(
    voice_router,
    prefix="/api"
)

app.include_router(
    tasks_router,
    prefix="/api"
)

app.include_router(
    workflows_router,
    prefix="/api"
)

app.include_router(
    scheduler_router,
    prefix="/api"
)

app.include_router(
    integrations_router,
    prefix="/api"
)

app.include_router(
    memory_router,
    prefix="/api"
)

app.include_router(
    notifications_router,
    prefix="/api"
)

app.include_router(
    security_router,
    prefix="/api"
)

app.include_router(
    timer_router
)

# Approval router already contains /api/approval prefix
app.include_router(
    approval_router
)

app.include_router(
    booking_router,
    prefix="/api"
)

app.include_router(
    shopping_router,
    prefix="/api"
)


# ============================================================
# BASIC ENDPOINTS
# ============================================================

@app.get("/")
def home():

    return {
        "message": "AI Buddy is running!",
        "status": "online"
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }


@app.get("/debug/event-loop")
async def debug_event_loop():

    loop = asyncio.get_running_loop()

    return {
        "event_loop": type(loop).__name__,
        "platform": __import__("sys").platform
    }