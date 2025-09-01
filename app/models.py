from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional


class Counter(SQLModel, table=True):
    """Counter model for storing counter state."""

    __tablename__ = "counters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class CounterUpdate(SQLModel, table=False):
    """Schema for updating counter value."""

    value: int


class CounterCreate(SQLModel, table=False):
    """Schema for creating a new counter."""

    value: int = Field(default=0)
