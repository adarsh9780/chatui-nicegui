# mock_api.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import random
import base64
import json
from plotly.utils import PlotlyJSONEncoder
import plotly.graph_objects as go
from ui.main import ui
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


@app.get("/mock_data")
async def get_mock_data(ticker: str):
    await asyncio.sleep(10)
    ticker = ticker.upper()

    # Simulate weekly price data
    dates = pd.date_range(end=pd.Timestamp.today(), periods=1000, freq="W")
    prices = [round(random.uniform(1, 1000), 2) for _ in range(len(dates))]
    df = pd.DataFrame({"date": dates, "price": prices, "symbol": ticker})
    df["date"] = df["date"].dt.strftime("%Y-%m-%d")

    explanation = f"### Data summary for `{ticker}`\nThis table shows simulated weekly price data."

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
