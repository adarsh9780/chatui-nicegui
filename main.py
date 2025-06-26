from nicegui import ui
import httpx
import asyncio

ui.add_body_html("""
<style>
textarea {
    resize: none !important;
}
html, body {
    overflow: hidden !important;
    margin: 0;
    padding: 0;
}
</style>
""")

# Global typing indicator
typing_label = None


# Async send logic that calls external API
async def handle_send():
    global typing_label
    name = input_box.value.strip()
    if not name:
        return

    input_box.value = ""

    # Show user's message
    with chat_column:
        ui.markdown(f"**You:** {name}").classes(
            "self-end bg-gray-100 p-3 rounded-md max-w-[70%]"
        )

    chat_area.scroll_to(percent=1e6)

    # Show typing indicator
    with chat_column:
        typing_label = ui.row().classes("self-start items-center gap-2 p-3")
        with typing_label:
            ui.spinner(size="sm")
            ui.label("CRE-Suite is typing...").classes("text-gray-500 text-sm")

    chat_area.scroll_to(percent=1e6)

    # Call API asynchronously
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get("https://api.agify.io", params={"name": name})
            data = response.json()
            predicted_age = data.get("age", "unknown")
    except Exception as e:
        predicted_age = f"Error: {str(e)}"

    # Simulated processing delay
    await asyncio.sleep(2)

    # Remove typing indicator
    typing_label.clear()

    # Show system message
    with chat_column:
        ui.markdown(
            f"**CRE-Suite:** The predicted age for `{name}` is **{predicted_age}**."
        ).classes("self-start p-3 w-full")

    chat_area.scroll_to(percent=1e6)


# UI Layout
with ui.row().classes("w-screen h-screen overflow-hidden justify-center bg-white"):
    with ui.column().classes("w-full max-w-4xl h-full"):
        with ui.card().classes(
            "w-full h-full flex flex-col justify-between shadow-sm rounded-xl bg-white"
        ):
            # Header
            ui.label("CRE-Suite").classes("text-2xl text-center text-gray-800 pt-2")

            # Scrollable chat area
            with ui.scroll_area().classes("flex-1 overflow-y-auto px-4") as chat_area:
                chat_column = ui.column().classes("w-full space-y-3")

            # Input + buttons
            with ui.column().classes("w-full px-4 pb-2"):
                with ui.element("div").classes(
                    "w-full p-3 bg-gray-50 border border-gray-200 rounded-2xl shadow-inner flex flex-col gap-2"
                ):
                    input_box = (
                        ui.textarea(placeholder="Enter a name to predict age...")
                        .props("auto-grow rows=1")
                        .classes(
                            "w-full text-base bg-transparent focus:outline-none resize-none"
                        )
                    )
                    with ui.row().classes("justify-end"):
                        ui.button(icon="arrow_upward", on_click=handle_send).props(
                            "flat round dense"
                        ).classes("bg-black text-white")

                ui.markdown(
                    "CRE-Suite can make mistakes. Please **verify** important info."
                ).classes("text-sm text-gray-500 text-center mt-2")

# Allow Enter to trigger send
input_box.on(
    "keydown",
    lambda e: handle_send()
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

ui.run(port=8000, reload=False)
