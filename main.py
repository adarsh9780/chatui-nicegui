from nicegui import ui

# State variables
header_text = ""
header_label = None
message_stage = 0  # 0: Welcome, 1: Where should we begin?, 2: Final state
first_message_sent = False


# Typing animation steps
def animate_typing():
    global header_text, message_stage

    if message_stage == 0:
        full_text = "Welcome to CRE-Suite"
    elif message_stage == 1:
        full_text = "Where should we begin?"
    else:
        header_label.text = "CRE-Suite"
        return  # stop animation

    if len(header_text) < len(full_text):
        header_text += full_text[len(header_text)]
        header_label.text = header_text
    else:
        message_stage += 1
        header_text = ""


# Send logic
def handle_send():
    global first_message_sent
    text = input_box.value.strip()
    if not text:
        return

    # Stop typing animation after first message
    if not first_message_sent:
        first_message_sent = True
        header_label.text = "CRE-Suite"
        typing_timer.pause()

    with chat_column:
        ui.label(text).classes("self-start bg-gray-100 rounded-md p-3")
    input_box.value = ""
    chat_area.scroll_to(percent=1e6)

    with chat_column:
        ui.label(text).classes("self-end bg-blue-100 rounded-md p-3")
    chat_area.scroll_to(percent=1e6)


# Layout
with ui.row().classes("w-full min-h-screen items-center justify-center bg-white"):
    with ui.column().classes("w-full max-w-3xl h-[90vh] justify-between"):
        # Chat card
        with ui.card().classes(
            "w-full flex flex-col flex-grow shadow-sm rounded-xl bg-white"
        ):
            # Animated Header
            header_label = ui.label("").classes(
                "text-2xl text-center text-gray-800 my-4"
            )

            # Scrollable chat area
            with ui.scroll_area().classes(
                "flex-grow overflow-auto px-4 pb-2"
            ) as chat_area:
                chat_column = ui.column().classes("w-full space-y-3")

            # Input + tools area
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

# Typing animation timer (every 100 ms)
typing_timer = ui.timer(interval=0.1, callback=animate_typing)

# Stop animation on Enter
input_box.on(
    "keydown",
    lambda e: handle_send()
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

ui.run()
