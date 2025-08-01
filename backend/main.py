# mock_api.py
from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random
import base64
import json
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go
from ui.ui1 import ui
import asyncio

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping")
async def ping():
    return {"status": "ok"}


class ChatRequest(BaseModel):
    user_query: str


@app.post("/chat/v2")
async def get_mock_data(request: ChatRequest):
    await asyncio.sleep(5)
    ticker = request.user_query.upper()

    # Simulate weekly price data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=1000, freq="W")
    prices = [round(random.uniform(1, 1000), 2) for _ in range(len(dates))]
    df = pd.DataFrame({"date": dates, "price": prices, "symbol": ticker})
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    explanation = """
To make your NiceGUI markdown output match the **compact and elegant style like ChatGPT’s**, here’s an optimized CSS style based on the screenshot you shared:

---

### ✅ Updated CSS for `markdown-content`

```html
<style>
.markdown-content {
    font-family: "Inter", "Segoe UI", sans-serif;
    font-size: 14px;
    line-height: 1.5;
    color: #1f1f1f;
    padding: 0.2rem 0.4rem;
    white-space: pre-wrap;
}

.markdown-content h1,
.markdown-content h2,
.markdown-content h3 {
    font-weight: 600;
    margin: 0.8em 0 0.4em;
}

.markdown-content p {
    margin: 0.4em 0;
}

.markdown-content code {
    background-color: #f0f2f5;
    padding: 1px 5px;
    border-radius: 4px;
    font-size: 13px;
    font-family: "JetBrains Mono", monospace;
    color: #444;
}

.markdown-content pre {
    background-color: #f7f7f8;
    border-radius: 6px;
    padding: 0.8em 1em;
    overflow: auto;
    font-size: 13px;
    line-height: 1.4;
    margin: 0.6em 0;
}
</style>
```

---

### 🧩 Apply this to your app:

In your NiceGUI script:

```python
ui.add_head_html('''<style>...</style>''')  # insert CSS above
```

And for each markdown render:

```python
ui.markdown(escape_markdown(explanation)).classes("markdown-content self-start w-full")
```

---

### 🔧 Optional helper to escape underscores:

```python
import re

def escape_markdown(text: str) -> str:
    return re.sub(r'(?<!\\)_', r'\\_', text)
```

---

### ✅ Result:

* Text is clean and readable
* Code blocks are light-gray with small padding
* Inline code (`like_this`) is distinct but compact
* Spacing is subtle, similar to ChatGPT output style

Let me know if you want to theme it further (e.g. dark mode, colored headings, etc).

"""

    code = f"""
import pandas as pd
import random

dates = pd.date_range(end=pd.Timestamp.today(), periods=1000, freq='W')
prices = [round(random.uniform(1, 1000), 2) for _ in range(len(dates))]
df = pd.DataFrame({{'date': dates, 'price': prices, 'symbol': '{ticker}'}})
"""

    fig = go.Figure()
    fig.add_trace(
        go.Scatter(
            x=df["date"].tail(100),
            y=df["price"].tail(100),
            mode="lines+markers",
            name=ticker,
        )
    )
    fig.update_layout(
        template="plotly_white",
        title=f"Last 100 Weeks Price Trend - {ticker}",
        xaxis_title="Date",
        yaxis_title="Price (USD)",
        autosize=True,
    )
    chart_output = json.loads(json.dumps(fig, cls=PlotlyJSONEncoder))

    csv_bytes = df.to_csv(index=False).encode()
    base64_output = base64.b64encode(csv_bytes).decode()

    return {
        "explanation": explanation,
        "code": code,
        "result_df": df.head(100).to_dict("records"),
        "chart_output": chart_output,
        "base64_output": base64_output,
    }


ui.run_with(app, mount_path="/ui")
# uvicorn.run(app, host="0.0.0.0", port=9000)
# uvicorn mockapi:app --reload --port 9000
