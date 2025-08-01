from nicegui import ui
import asyncio
import plotly.graph_objects as go
import base64
from pathlib import Path
import tempfile
import httpx
import re


# Global typing indicator
typing_label = None

ui.add_body_html("""
<style>
:root {
  --white-99: hsla(0, 0%, 99%, 1);
  --mountbatten-pink: hsla(327, 27%, 57%, 1);
  --dark-slate-gray: hsla(187, 22%, 33%, 1);
  --sepia: hsla(32, 100%, 18%, 1);
  --burnt-umber: hsla(7, 53%, 31%, 1);
}

html, body {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  background-color: var(--white-99);
  color: var(--dark-slate-gray);
  margin: 0;
  padding: 0;
  overflow: hidden !important;
}

.markdown-content {
  font-family: 'Inter', sans-serif;
  font-size: 16px;
  line-height: 1.35;
  padding: 0.05rem 0.2rem;
  margin: 0;
  white-space: pre-wrap;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
  font-weight: 600;
  margin: 0.4em 0 0.2em;
}

.markdown-content p {
  margin: 0.15em 0;
}

/* INLINE CODE */
.markdown-content :not(pre) > code {
  background-color: #f0f2f5;
  padding: 0px 3px;
  border-radius: 3px;
  font-size: 12.5px;
  font-family: "JetBrains Mono", monospace;
  color: #3a3a3a;
}

/* MULTILINE BLOCKS */
.markdown-content pre {
  background-color: #f7f7f8;
  padding: 0.4em 0.6em;
  border-radius: 5px;
  overflow-x: auto;
  font-size: 12.5px;
  font-family: "JetBrains Mono", monospace;
  line-height: 1.35;
  margin: 0.3em 0;
}

.markdown-content pre code {
  all: unset;
  font-family: "JetBrains Mono", monospace;
  font-size: 12.5px;
  color: #1a1a1a;
}
</style>
""")


def escape_markdown(text: str) -> str:
    return re.sub(r"(?<!\\)_", r"\\_", text)


# Function to simulate full output structure for any user input
async def generate_mock_output(user_input: str):
    url = "http://localhost:8000/chat/v2"
    payload = {"user_query": user_input}
    async with httpx.AsyncClient() as client:
        response = await client.post(
            url, json=payload, timeout=30, headers={"accept": "application/json"}
        )
        response.raise_for_status()
        output = response.json()
        return output


# Display structured output from JSON
def display_structured_output(output: dict):
    explanation = output.get("explanation")
    # explanation = f"```markdown\n{explanation}\n```"
    code = output.get("code")
    result_df = output.get("result_df", [])
    chart_output = output.get("chart_output")
    base64_output = output.get("base64_output")

    with chat_column:
        if explanation:
            ui.markdown(escape_markdown(explanation)).classes(
                "markdown-content self-start w-full"
            )
            # .classes("self-start p-3 text-gray-500 text-sm")

        # Create tabs & store their references
        with ui.tabs().classes("self-start w-full") as tabs:
            tab_chart = ui.tab("Chart")
            tab_table = ui.tab("Table")
            tab_code = ui.tab("Code")

        # Link panels to those tabs
        with ui.tab_panels(tabs, value=tab_chart).classes("self-start w-full"):
            with ui.tab_panel(tab_chart):
                if chart_output:
                    fig = go.Figure(chart_output)
                    ui.plotly(fig).classes("w-full")

            with ui.tab_panel(tab_table):
                if result_df:
                    ui.aggrid(
                        {
                            "columnDefs": [
                                {"headerName": k, "field": k}
                                for k in result_df[0].keys()
                            ],
                            "rowData": result_df,
                            "defaultColDef": {
                                "sortable": True,
                                "filter": True,
                                "resizable": True,
                                "floatingFilter": True,
                                "flex": 1,
                            },
                        },
                        theme="quartz",
                    ).classes("h-[400px] w-full")

                    if base64_output:
                        decoded = base64.b64decode(base64_output.encode())

                        def download_fn():
                            temp_path = Path(tempfile.gettempdir()) / "output.csv"
                            with open(temp_path, "wb") as f:
                                f.write(decoded)
                            ui.download(temp_path, filename="output.csv")

                        ui.button("Download Full Data", on_click=download_fn).classes(
                            "mt-2"
                        )

            with ui.tab_panel(tab_code):
                if code:
                    ui.code(code, language="python").classes("w-full")


# Unified input handler
async def handle_send():
    global typing_label
    user_input = input_box.value.strip()
    if not user_input:
        return

    input_box.value = ""

    # Display user input
    with chat_column:
        ui.markdown(f"**You:** {user_input}").classes(
            "self-end bg-gray-100 p-3 rounded-md max-w-[70%]"
        )

    chat_area.scroll_to(percent=1e6)

    # Show typing spinner
    with chat_column:
        typing_label = ui.row().classes("self-start items-center gap-2 p-3")
        with typing_label:
            ui.spinner(size="sm")
            ui.label("CRE-Suite is thinking...").classes("text-gray-500 text-sm")

    chat_area.scroll_to(percent=1e6)

    # Wait and get response
    await asyncio.sleep(0.3)  # simulate small delay
    output = await generate_mock_output(user_input)

    # Hide spinner only after response is processed
    typing_label.clear()

    # Show output
    display_structured_output(output)
    chat_area.scroll_to(percent=1e6)


# UI Layout
with ui.row().classes("w-screen h-screen overflow-hidden justify-center bg-white"):
    with ui.column().classes("w-full max-w-4xl h-full"):
        with ui.card().classes(
            "w-full h-full flex flex-col justify-between shadow-sm rounded-xl bg-white"
        ):
            ui.label("CRE-Suite").classes("text-2xl text-center pt-2").style(
                "font-family: 'Segoe UI', sans-serif; font-weight: 600; color: var(--mountbatten-pink);"
            )

            with ui.scroll_area().classes("flex-1 overflow-y-auto px-4") as chat_area:
                chat_column = ui.column().classes("w-full space-y-3")

            with ui.column().classes("w-full px-4 pb-2"):
                with ui.element("div").classes(
                    "w-full p-3 bg-gray-50 border border-gray-200 rounded-2xl shadow-inner flex flex-col gap-2"
                ):
                    input_box = (
                        ui.textarea(
                            placeholder="Type a stock ticker like 'AAPL', 'GOOGL', or anything..."
                        )
                        .props("auto-grow rows=1")
                        .classes(
                            "w-full text-base bg-transparent focus:outline-none resize-none"
                        )
                    )
                    with ui.row().classes("justify-between items-center"):
                        with ui.row().classes("gap-2"):
                            ui.button(
                                icon="schema",
                                on_click=lambda x: ui.notify("Clicked on View Schema"),
                            ).props("flat round dense").classes("text-black")
                            ui.button(
                                icon="add",
                                on_click=lambda x: ui.notify("Clicked on New Session"),
                            ).props("flat round dense").classes("text-black")
                        ui.button(icon="arrow_upward", on_click=handle_send).props(
                            "flat round dense"
                        ).classes("bg-black text-white")

                ui.markdown(
                    "CRE-Suite can make mistakes. Please **verify** important info."
                ).classes("text-sm text-gray-500 text-center mt-0")


input_box.on(
    "keydown",
    lambda e: handle_send()
    if e.args.get("key") == "Enter" and not e.args.get("shiftKey", False)
    else None,
)

if __name__ == "__main__":
    ui.run(port=8000)
