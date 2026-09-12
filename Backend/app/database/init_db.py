from app.database.connection import Base, engine

# Import all models so SQLAlchemy knows about the tables.
from app.database.models import (
    User,
    Task,
    Notification,
    Conversation,
    Workflow,
    ScheduledJob,
    Memory
)


def initialize_database():
    """
    Create all database tables defined in the models.
    """

    Base.metadata.create_all(
        bind=engine
    )

    print(
        "AI Buddy database initialized successfully."
    )


if __name__ == "__main__":

    initialize_database()