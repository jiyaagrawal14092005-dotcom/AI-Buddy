from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker


# ---------------------------------
# DATABASE PATH
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parents[2]

DATABASE_DIR = BASE_DIR / "database"

DATABASE_DIR.mkdir(
    parents=True,
    exist_ok=True
)

DATABASE_PATH = DATABASE_DIR / "ai_buddy.db"


# ---------------------------------
# DATABASE URL
# ---------------------------------

DATABASE_URL = (
    f"sqlite:///{DATABASE_PATH}"
)


# ---------------------------------
# DATABASE ENGINE
# ---------------------------------

engine = create_engine(
    DATABASE_URL,
    connect_args={
        "check_same_thread": False
    }
)


# ---------------------------------
# DATABASE SESSION
# ---------------------------------

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# ---------------------------------
# BASE MODEL
# ---------------------------------

Base = declarative_base()


# ---------------------------------
# DATABASE SESSION DEPENDENCY
# ---------------------------------

def get_db():

    db = SessionLocal()

    try:

        yield db

    finally:

        db.close()