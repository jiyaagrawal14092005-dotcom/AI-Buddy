from datetime import datetime

from pydantic import BaseModel, ConfigDict


# ---------------------------------
# USER SCHEMAS
# ---------------------------------

class UserBase(BaseModel):

    username: str
    email: str


class UserCreate(UserBase):

    password: str


class UserResponse(UserBase):

    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# TASK SCHEMAS
# ---------------------------------

class TaskBase(BaseModel):

    title: str
    description: str | None = None


class TaskCreate(TaskBase):

    user_id: int


class TaskResponse(TaskBase):

    id: int
    user_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# NOTIFICATION SCHEMAS
# ---------------------------------

class NotificationBase(BaseModel):

    message: str
    notification_type: str = "in_app"


class NotificationCreate(NotificationBase):

    user_id: int


class NotificationResponse(NotificationBase):

    id: int
    user_id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# CONVERSATION SCHEMAS
# ---------------------------------

class ConversationCreate(BaseModel):

    user_id: int
    user_message: str
    assistant_response: str


class ConversationResponse(ConversationCreate):

    id: int
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# WORKFLOW SCHEMAS
# ---------------------------------

class WorkflowCreate(BaseModel):

    user_id: int
    name: str


class WorkflowResponse(WorkflowCreate):

    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# SCHEDULED JOB SCHEMAS
# ---------------------------------

class ScheduledJobCreate(BaseModel):

    user_id: int
    name: str
    schedule: str


class ScheduledJobResponse(ScheduledJobCreate):

    id: int
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


# ---------------------------------
# MEMORY SCHEMAS
# ---------------------------------

class MemoryCreate(BaseModel):

    user_id: int
    memory_key: str
    memory_value: str


class MemoryResponse(MemoryCreate):

    id: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )