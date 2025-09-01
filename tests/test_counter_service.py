import pytest
from app.database import reset_db
from app.counter_service import (
    get_or_create_counter,
    increment_counter,
    decrement_counter,
    reset_counter,
    get_current_value,
)


@pytest.fixture()
def new_db():
    """Reset database before each test."""
    reset_db()
    yield
    reset_db()


def test_get_or_create_counter_creates_new(new_db):
    """Test that get_or_create_counter creates a new counter when none exists."""
    counter = get_or_create_counter()

    assert counter is not None
    assert counter.id is not None
    assert counter.value == 0
    assert counter.created_at is not None
    assert counter.updated_at is not None


def test_get_or_create_counter_returns_existing(new_db):
    """Test that get_or_create_counter returns existing counter."""
    # Create first counter
    counter1 = get_or_create_counter()
    counter1_id = counter1.id

    # Get counter again - should return the same one
    counter2 = get_or_create_counter()

    assert counter2.id == counter1_id
    assert counter2.value == counter1.value


def test_increment_counter_increases_value(new_db):
    """Test that increment_counter increases the value by 1."""
    # Create initial counter
    initial_counter = get_or_create_counter()
    initial_value = initial_counter.value

    # Increment counter
    updated_counter = increment_counter()

    assert updated_counter.value == initial_value + 1
    assert updated_counter.updated_at > initial_counter.updated_at


def test_increment_counter_multiple_times(new_db):
    """Test multiple increments work correctly."""
    initial_counter = get_or_create_counter()
    initial_value = initial_counter.value

    # Increment 5 times
    for i in range(5):
        increment_counter()

    final_value = get_current_value()
    assert final_value == initial_value + 5


def test_decrement_counter_decreases_value(new_db):
    """Test that decrement_counter decreases the value by 1."""
    # Create initial counter with some value
    initial_counter = get_or_create_counter()
    increment_counter()  # Set to 1
    current_value = get_current_value()

    # Decrement counter
    updated_counter = decrement_counter()

    assert updated_counter.value == current_value - 1
    assert updated_counter.updated_at > initial_counter.updated_at


def test_decrement_counter_can_go_negative(new_db):
    """Test that counter can go negative."""
    # Start with 0 and decrement
    get_or_create_counter()
    decrement_counter()

    final_value = get_current_value()
    assert final_value == -1


def test_reset_counter_sets_to_zero(new_db):
    """Test that reset_counter sets value to 0."""
    # Create counter and increment it
    get_or_create_counter()
    increment_counter()
    increment_counter()
    increment_counter()

    # Verify it's not zero
    assert get_current_value() == 3

    # Reset counter
    updated_counter = reset_counter()

    assert updated_counter.value == 0
    assert get_current_value() == 0


def test_reset_counter_from_negative(new_db):
    """Test that reset works from negative values."""
    # Create counter and decrement it
    get_or_create_counter()
    decrement_counter()
    decrement_counter()

    # Verify it's negative
    assert get_current_value() == -2

    # Reset counter
    reset_counter()

    assert get_current_value() == 0


def test_get_current_value_returns_correct_value(new_db):
    """Test that get_current_value returns the current counter value."""
    # Create counter
    get_or_create_counter()

    # Value should initially be 0
    assert get_current_value() == 0

    # Increment and check
    increment_counter()
    assert get_current_value() == 1

    # Decrement and check
    decrement_counter()
    decrement_counter()
    assert get_current_value() == -1


def test_counter_operations_with_specific_id(new_db):
    """Test counter operations work with specific counter ID."""
    # Create first counter
    counter1 = get_or_create_counter()
    counter1_id = counter1.id

    # Increment it
    increment_counter(counter1_id)
    assert get_current_value(counter1_id) == 1

    # Operations on the same counter should work
    decrement_counter(counter1_id)
    assert get_current_value(counter1_id) == 0

    reset_counter(counter1_id)
    assert get_current_value(counter1_id) == 0


def test_counter_persistence_across_operations(new_db):
    """Test that counter state persists across multiple operations."""
    # Create and modify counter
    get_or_create_counter()

    # Perform various operations
    increment_counter()
    increment_counter()
    decrement_counter()
    increment_counter()
    increment_counter()

    # Final value should be 3
    assert get_current_value() == 3

    # Reset and verify
    reset_counter()
    assert get_current_value() == 0

    # Increment after reset
    increment_counter()
    assert get_current_value() == 1


def test_counter_edge_cases(new_db):
    """Test counter behavior in edge cases."""
    # Test with None counter_id (should work with default counter)
    get_or_create_counter(None)

    # Test operations with None ID
    increment_counter(None)
    assert get_current_value(None) == 1

    decrement_counter(None)
    assert get_current_value(None) == 0

    reset_counter(None)
    assert get_current_value(None) == 0
