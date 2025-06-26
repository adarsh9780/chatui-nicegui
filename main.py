from nicegui import ui

ui.add_body_html("""
<style>
    html, body {
        overflow: hidden !important;
        margin: 0;
        padding: 0;
    }
</style>
""")


# Send logic
def handle_send():
    text = input_box.value.strip()
    if not text:
        return

    # USER MESSAGE: right aligned, narrower, gray bubble
    with chat_column:
        ui.markdown(text).classes("self-end bg-gray-100 rounded-md p-3 max-w-[70%]")
    input_box.value = ""
    chat_area.scroll_to(percent=1e6)

    # SYSTEM MESSAGE: left aligned, full width, no background
    with chat_column:
        ui.markdown(text).classes("self-start p-3 w-full")
    chat_area.scroll_to(percent=1e6)


# Fullscreen fixed layout
with ui.row().classes("w-screen h-screen overflow-hidden justify-center bg-white"):
    with ui.column().classes("w-full max-w-5xl h-full"):
        with ui.card().classes(
            "w-full h-full flex flex-col justify-between shadow-sm rounded-xl bg-white"
        ):
            # Header
            ui.label("CRE-Suite").classes("text-2xl text-center text-gray-800 pt-2")

            # Scrollable chat area
            with ui.scroll_area().classes("flex-1 overflow-y-auto px-4") as chat_area:
                chat_column = ui.column().classes("w-full space-y-3")

            # Bottom input + footer
            with ui.column().classes("w-full px-4 pb-2"):
                # Input container
                with ui.element("div").classes(
                    "w-full p-3 bg-gray-50 border border-gray-200 rounded-2xl shadow-inner flex flex-col gap-2"
                ):
                    input_box = (
                        ui.textarea(placeholder="Ask anything...")
                        .props("auto-grow rows=1")
                        .classes(
                            "w-full text-base bg-transparent focus:outline-none resize-none"
                        )
                    )
                    with ui.row().classes("justify-between items-center"):
                        with ui.row().classes("gap-2"):
                            ui.button("View Schema").props("flat dense").classes(
                                "bg-gray-100 text-sm"
                            )
                            ui.button("New Session").props("flat dense").classes(
                                "bg-red-100 text-red-800 text-sm"
                            )
                        ui.button(icon="arrow_upward", on_click=handle_send).props(
                            "flat round dense"
                        ).classes("bg-black text-white")

                # Footer info message
                ui.markdown(
                    "CRE-Suite can make mistakes. Please **verify** important info."
                ).classes("text-sm text-gray-500 text-center mt-2")


# Trigger send on Enter (unless Shift is held)
input_box.on(
    "keydown",
    lambda e: handle_send()
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

ui.run()
