import logging
from nicegui import ui
from app.counter_service import increment_counter, decrement_counter, reset_counter, get_current_value

logger = logging.getLogger(__name__)


def create():
    @ui.page("/counter")
    def counter_page():
        # Apply modern color theme
        ui.colors(
            primary="#2563eb",  # Professional blue
            secondary="#64748b",  # Subtle gray
            accent="#10b981",  # Success green
            positive="#10b981",
            negative="#ef4444",  # Error red
            warning="#f59e0b",  # Warning amber
        )

        # Main container with modern styling
        with ui.column().classes(
            "items-center justify-center min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 p-8"
        ):
            # Title
            ui.label("Counter Application").classes("text-4xl font-bold text-gray-800 mb-8")

            # Counter card
            with ui.card().classes("p-8 shadow-xl rounded-2xl bg-white min-w-96"):
                # Counter display
                counter_label = ui.label().classes(
                    "text-6xl font-bold text-center text-gray-800 mb-8 p-4 bg-gray-50 rounded-lg"
                )

                # Button container
                with ui.row().classes("gap-4 justify-center mb-6"):
                    # Decrement button
                    ui.button("−", on_click=lambda: handle_decrement()).classes(
                        "w-16 h-16 text-2xl font-bold bg-red-500 hover:bg-red-600 text-white rounded-full shadow-lg transition-all"
                    )

                    # Reset button
                    ui.button("↺", on_click=lambda: handle_reset()).classes(
                        "w-16 h-16 text-2xl font-bold bg-gray-500 hover:bg-gray-600 text-white rounded-full shadow-lg transition-all"
                    )

                    # Increment button
                    ui.button("+", on_click=lambda: handle_increment()).classes(
                        "w-16 h-16 text-2xl font-bold bg-green-500 hover:bg-green-600 text-white rounded-full shadow-lg transition-all"
                    )

                # Button labels
                with ui.row().classes("gap-4 justify-center text-sm text-gray-600"):
                    ui.label("Decrement").classes("w-16 text-center")
                    ui.label("Reset").classes("w-16 text-center")
                    ui.label("Increment").classes("w-16 text-center")

                # Current value info
                with ui.row().classes("justify-center mt-6 p-4 bg-blue-50 rounded-lg"):
                    ui.icon("info").classes("text-blue-500 mr-2")
                    ui.label("Click buttons to modify the counter value").classes("text-blue-700 text-sm")

        def update_counter_display():
            """Update the counter display with current value."""
            current_value = get_current_value()
            counter_label.set_text(str(current_value))

        def handle_increment():
            """Handle increment button click."""
            try:
                increment_counter()
                update_counter_display()
                ui.notify("Counter incremented!", type="positive", position="top")
            except Exception as e:
                logger.error(f"Error incrementing counter: {str(e)}")
                ui.notify(f"Error: {str(e)}", type="negative", position="top")

        def handle_decrement():
            """Handle decrement button click."""
            try:
                decrement_counter()
                update_counter_display()
                ui.notify("Counter decremented!", type="positive", position="top")
            except Exception as e:
                logger.error(f"Error decrementing counter: {str(e)}")
                ui.notify(f"Error: {str(e)}", type="negative", position="top")

        def handle_reset():
            """Handle reset button click."""
            try:
                reset_counter()
                update_counter_display()
                ui.notify("Counter reset to zero!", type="info", position="top")
            except Exception as e:
                logger.error(f"Error resetting counter: {str(e)}")
                ui.notify(f"Error: {str(e)}", type="negative", position="top")

        # Initialize counter display
        update_counter_display()

    @ui.page("/")
    def index():
        """Redirect to counter page for better UX."""
        ui.navigate.to("/counter")
