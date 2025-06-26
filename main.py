from nicegui import ui


# Send logic
def handle_send():
    text = input_box.value.strip()
    if not text:
        return

    with chat_column:
        ui.label(text).classes("self-start bg-gray-100 rounded-md p-3")
    input_box.value = ""
    chat_area.scroll_to(percent=1e6)

    with chat_column:
        ui.label(text).classes("self-end bg-blue-100 rounded-md p-3")
    chat_area.scroll_to(percent=1e6)


# Fullscreen centered layout
with ui.row().classes("w-full min-h-screen items-center justify-center bg-white"):
    with ui.column().classes("w-full max-w-3xl h-[90vh] justify-between"):
        # Chat card
        with ui.card().classes(
            "w-full flex flex-col flex-grow shadow-sm rounded-xl bg-white"
        ):
            # Static header
            ui.label("CRE-Suite").classes("text-2xl text-center text-gray-800 my-4")

            # Scrollable chat area
            with ui.scroll_area().classes(
                "flex-grow overflow-auto px-4 pb-2"
            ) as chat_area:
                chat_column = ui.column().classes("w-full space-y-3")

            # Input + tools container
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

                # Button row inside the container
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

# Handle Enter vs Shift+Enter
input_box.on(
    "keydown",
    lambda e: handle_send()
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

ui.run()
