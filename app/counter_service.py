from datetime import datetime
from typing import Optional
from sqlmodel import select
from app.database import get_session
from app.models import Counter, CounterCreate


def get_or_create_counter(counter_id: Optional[int] = None) -> Counter:
    """Get existing counter or create a new one if none exists."""
    with get_session() as session:
        if counter_id is not None:
            counter = session.get(Counter, counter_id)
            if counter is not None:
                return counter

        # Try to get the first counter if no specific ID requested
        if counter_id is None:
            statement = select(Counter).limit(1)
            counter = session.exec(statement).first()
            if counter is not None:
                return counter

        # Create new counter if none exists
        counter_data = CounterCreate()
        counter = Counter(value=counter_data.value, created_at=datetime.utcnow(), updated_at=datetime.utcnow())
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def increment_counter(counter_id: Optional[int] = None) -> Counter:
    """Increment counter value by 1."""
    with get_session() as session:
        counter = get_or_create_counter(counter_id)
        # Re-fetch from session to ensure we have the latest data
        counter = session.get(Counter, counter.id)
        if counter is None:
            raise ValueError("Counter not found")

        counter.value += 1
        counter.updated_at = datetime.utcnow()
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def decrement_counter(counter_id: Optional[int] = None) -> Counter:
    """Decrement counter value by 1."""
    with get_session() as session:
        counter = get_or_create_counter(counter_id)
        # Re-fetch from session to ensure we have the latest data
        counter = session.get(Counter, counter.id)
        if counter is None:
            raise ValueError("Counter not found")

        counter.value -= 1
        counter.updated_at = datetime.utcnow()
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def reset_counter(counter_id: Optional[int] = None) -> Counter:
    """Reset counter value to 0."""
    with get_session() as session:
        counter = get_or_create_counter(counter_id)
        # Re-fetch from session to ensure we have the latest data
        counter = session.get(Counter, counter.id)
        if counter is None:
            raise ValueError("Counter not found")

        counter.value = 0
        counter.updated_at = datetime.utcnow()
        session.add(counter)
        session.commit()
        session.refresh(counter)
        return counter


def get_current_value(counter_id: Optional[int] = None) -> int:
    """Get current counter value."""
    counter = get_or_create_counter(counter_id)
    return counter.value
