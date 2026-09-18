from datetime import datetime

from sqlalchemy import (
    Boolean,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text
)

from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship
)

from app.database.connection import Base


# ---------------------------------
# USER MODEL
# ---------------------------------

class User(Base):

    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    username: Mapped[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )

    email: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    is_active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    tasks: Mapped[list["Task"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    notifications: Mapped[list["Notification"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    conversations: Mapped[list["Conversation"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    oauth_tokens: Mapped[list["OAuthToken"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )

    oauth_connections: Mapped[list["OAuthConnection"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan"
    )


# ---------------------------------
# TASK MODEL
# ---------------------------------

class Task(Base):

    __tablename__ = "tasks"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    title: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    description: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="tasks"
    )


# ---------------------------------
# NOTIFICATION MODEL
# ---------------------------------

class Notification(Base):

    __tablename__ = "notifications"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    notification_type: Mapped[str] = mapped_column(
        String(50),
        default="in_app",
        nullable=False
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="created",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="notifications"
    )


# ---------------------------------
# CONVERSATION / MEMORY MODEL
# ---------------------------------

class Conversation(Base):

    __tablename__ = "conversations"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    user_message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    assistant_response: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="conversations"
    )


# ---------------------------------
# WORKFLOW MODEL
# ---------------------------------

class Workflow(Base):

    __tablename__ = "workflows"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="created",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ---------------------------------
# SCHEDULED JOB MODEL
# ---------------------------------

class ScheduledJob(Base):

    __tablename__ = "scheduled_jobs"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    schedule: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        default="scheduled",
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )


# ---------------------------------
# MEMORY MODEL
# ---------------------------------

class Memory(Base):

    __tablename__ = "memories"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False
    )

    memory_key: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    memory_value: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )


# ---------------------------------
# OAUTH TOKEN MODEL
# ---------------------------------

class OAuthToken(Base):

    __tablename__ = "oauth_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    token_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    encrypted_access_token: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    encrypted_refresh_token: Mapped[str | None] = mapped_column(
        Text,
        nullable=True
    )

    expires_at: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True
    )

    active: Mapped[bool] = mapped_column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="oauth_tokens"
    )


# ---------------------------------
# OAUTH CONNECTION MODEL
# ---------------------------------

class OAuthConnection(Base):

    __tablename__ = "oauth_connections"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        index=True
    )

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    provider: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True
    )

    connection_id: Mapped[str] = mapped_column(
        String(255),
        unique=True,
        nullable=False,
        index=True
    )

    scopes: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    status: Mapped[str] = mapped_column(
        String(50),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user: Mapped["User"] = relationship(
        back_populates="oauth_connections"
    )