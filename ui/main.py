from nicegui import ui
import asyncio
import os

EXPORT_DIR = "export"
os.makedirs(EXPORT_DIR, exist_ok=True)

typing_indicator = None
ASSISTANT_TEXT = "Hello! My name is Chatty. I can't help you. Sorry :)"


def handle_file_upload(file):
    save_path = os.path.join(EXPORT_DIR, file.name)
    with open(save_path, "wb") as f:
        f.write(file.content.read())
    ui.notify(f"Uploaded to {save_path}")


async def handle_send():
    message = input_box.value.strip()
    if not message:
        return
    input_box.value = ""

    # User message (right-aligned)
    with chatbox:
        with ui.row().classes("w-full justify-end"):
            with ui.element().classes("max-w-lg"):
                ui.markdown(message).classes(
                    "bg-blue-100 text-blue-900 px-4 py-2 rounded-xl text-sm"
                )
    chatbox.scroll_to(percent=1e6)

    global typing_indicator
    try:
        # Typing animation (left-aligned)
        with chatbox:
            typing_indicator = ui.row().classes(
                "w-full justify-start items-center gap-2"
            )
            with typing_indicator:
                ui.spinner(size="sm")
                ui.label("Assistant is typing...").classes("text-sm text-gray-500")
        chatbox.scroll_to(percent=1e6)

        await asyncio.sleep(1.5)
        typing_indicator.delete()

        # Assistant message (left-aligned)
        with chatbox:
            with ui.row().classes("w-full justify-start"):
                with ui.element().classes("max-w-lg"):
                    ui.markdown(ASSISTANT_TEXT).classes(
                        "bg-gray-100 text-gray-800 px-4 py-2 rounded-xl text-sm"
                    )
        chatbox.scroll_to(percent=1e6)

    except Exception as e:
        if typing_indicator:
            typing_indicator.delete()
        with chatbox:
            with ui.row().classes("w-full justify-start"):
                with ui.element().classes("max-w-lg"):
                    ui.markdown(f"**Assistant (Error):** {e}").classes(
                        "bg-red-100 text-red-800 px-4 py-2 rounded-xl text-sm"
                    )


# --- API KEY DIALOG ---
api_dialog = ui.dialog().classes("w-full max-w-md")

with api_dialog:
    with ui.card().classes("w-full"):
        ui.label("🔐 API Configuration").classes("text-lg font-semibold mb-2")

        with ui.tabs().classes("w-full") as tabs:
            tab_gemini = ui.tab("Google Gemini")
            tab_openai = ui.tab("OpenAI")

        with ui.tab_panels(tabs, value=tab_openai).classes("w-full"):
            with ui.tab_panel(tab_gemini):
                ui.input("Enter your Google Gemini API key").props(
                    "type=password"
                ).classes("w-full")

            with ui.tab_panel(tab_openai):
                ui.input("Enter your OpenAI API key").props("type=password").classes(
                    "w-full"
                )

        ui.label(
            "Privacy Notice: Your API keys are stored locally in your browser and never shared."
        ).classes("text-xs text-gray-600 mt-4")

        with ui.row().classes("justify-end mt-4"):
            ui.button("Cancel", on_click=api_dialog.close).props("flat color=gray")
            ui.button(
                "Save Configuration",
                on_click=lambda: ui.notify("Configuration Saved ✅"),
            ).props("color=primary")


# --- DB SELECTION DIALOG ---
db_dialog = ui.dialog().classes("w-full max-w-md")

with db_dialog:
    with ui.card().classes("w-full"):
        ui.label("📁 Select Database and Schema Directory").classes(
            "text-lg font-semibold mb-4"
        )

        db_path_label = ui.label("No database selected").classes(
            "text-sm text-gray-600"
        )
        schema_path_label = ui.label("No schema selected").classes(
            "text-sm text-gray-600"
        )

        def handle_db_upload(file):
            db_path_label.text = f"📦 DB selected: {file.name}"
            # Optionally save path or file content

        def handle_schema_upload(file):
            schema_path_label.text = f"📘 Schema selected: {file.name}"

        ui.upload(on_upload=handle_db_upload, label="Upload .db file").classes("w-full")
        ui.upload(on_upload=handle_schema_upload, label="Upload .json schema").classes(
            "w-full mt-2"
        )

        with ui.row().classes("justify-end mt-4"):
            ui.button("Cancel", on_click=db_dialog.close).props("flat color=gray")
            ui.button("Connect", on_click=lambda: ui.notify("Paths saved ✅")).props(
                "color=primary"
            )


# --- UI Layout ---
with ui.column().classes("w-screen h-screen bg-gray-50 text-black"):
    # Header
    with ui.row().classes(
        "w-full bg-white shadow-md px-6 py-3 justify-between items-center"
    ):
        ui.label("💬 Chat Assistant").classes("text-xl font-semibold")
        with ui.row().classes("gap-3"):
            ui.button("View Schema").props("outline")
            ui.button("View Data").props("outline")
            ui.button("Select DB", on_click=db_dialog.open).props("outline")
            ui.button("Set API Key", on_click=api_dialog.open).props("outline")

    # Main Section
    with ui.row().classes("flex-1 w-full h-full p-4 gap-4"):
        # Chat Column
        with ui.column().classes("flex-1 h-full w-full"):
            with ui.card().classes(
                "flex flex-col h-full w-full rounded-2xl shadow-sm bg-white"
            ):
                global chatbox
                chatbox = ui.scroll_area().classes(
                    "w-full flex-1 p-4 space-y-4 overflow-y-auto"
                )

                # 🧠 Compact input + send row
                with ui.column().classes("w-full border-t border-gray-200 p-3 gap-1"):
                    with ui.row().classes("w-full items-center gap-2"):
                        global input_box
                        input_box = (
                            ui.input(
                                placeholder="Talk to your data... (e.g., 'Show me all customers from New York')"
                            )
                            .props("borderless")
                            .classes(
                                "flex-grow bg-gray-100 text-sm px-4 h-[50px] rounded-full leading-none"
                            )
                        )

                        (
                            ui.button(icon="send")
                            .props("color=primary flat")
                            .classes(
                                "rounded-full h-[40px] w-[40px] flex items-center justify-center"
                            )
                            .on("click", lambda: asyncio.create_task(handle_send()))
                        )

                    # Hint below the row
                    ui.label("Press Enter to send, Shift+Enter for new line").classes(
                        "text-xs text-gray-500 ml-1"
                    )

        # Right Panel
        with ui.card().classes("flex-1 h-full p-4 rounded-2xl shadow-sm bg-white"):
            ui.label("📊 Insights / Tools").classes("text-lg font-semibold")
            ui.separator()
            ui.label("You can add helpful tools or summaries here.")

# Send on Enter
input_box.on(
    "keydown",
    lambda e: asyncio.create_task(handle_send())
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

ui.run()
