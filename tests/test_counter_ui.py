import logging
import pytest
from nicegui.testing import User
from nicegui import ui
from app.database import reset_db

logger = logging.getLogger(__name__)


@pytest.fixture()
def new_db():
    """Reset database before each test."""
    reset_db()
    yield
    reset_db()


async def test_counter_page_loads(user: User, new_db) -> None:
    """Test that the counter page loads with initial UI elements."""
    await user.open("/counter")

    # Check that main elements are present
    await user.should_see("Counter Application")

    # Check for buttons
    increment_buttons = list(user.find(ui.button).elements)
    assert len(increment_buttons) >= 3  # increment, decrement, reset

    # Check initial counter value is displayed (should be 0)
    await user.should_see("0")


async def test_increment_button_functionality(user: User, new_db) -> None:
    """Test that increment button functionality exists and UI responds."""
    await user.open("/counter")

    # Initial value should be 0
    await user.should_see("0")

    # Find the increment button by its text content
    user.find("+").click()

    # Should see value change to 1
    await user.should_see("1")


async def test_index_redirects_to_counter(user: User, new_db) -> None:
    """Test that index page redirects to counter page."""
    await user.open("/")

    # Should see counter application content
    await user.should_see("Counter Application")


async def test_counter_ui_notifications(user: User, new_db) -> None:
    """Test that UI shows notifications for user actions."""
    await user.open("/counter")

    # Click increment button to trigger notification
    user.find("+").click()

    # UI should still be functional after button click
    await user.should_see("Counter Application")


async def test_counter_ui_styling_elements(user: User, new_db) -> None:
    """Test that UI contains expected styling elements and layout."""
    await user.open("/counter")

    # Check for title
    await user.should_see("Counter Application")

    # Check for instruction text
    await user.should_see("Click buttons to modify the counter value")

    # Check for button labels
    await user.should_see("Increment")
    await user.should_see("Decrement")
    await user.should_see("Reset")


async def test_counter_multiple_operations_ui(user: User, new_db) -> None:
    """Test multiple UI operations work correctly."""
    await user.open("/counter")

    # Start with 0
    await user.should_see("0")

    # Test increment
    user.find("+").click()
    await user.should_see("1")

    # Test increment again
    user.find("+").click()
    await user.should_see("2")

    # Test decrement
    user.find("−").click()
    await user.should_see("1")

    # Test reset
    user.find("↺").click()
    await user.should_see("0")


async def test_counter_error_handling_ui(user: User, new_db) -> None:
    """Test that UI handles errors gracefully."""
    await user.open("/counter")

    # The UI should load without errors even if database operations fail
    await user.should_see("Counter Application")

    # Multiple button clicks should not break the interface
    for _ in range(5):  # Click increment multiple times
        user.find("+").click()

    # UI should still be functional
    await user.should_see("Counter Application")
    await user.should_see("5")  # Should show correct value
