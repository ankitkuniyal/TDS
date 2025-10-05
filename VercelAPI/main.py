from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import numpy as np
import json

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["POST"],
    allow_headers=["*"],
)

@app.post("/")
async def analyze_latency(request: Request):
    data = await request.json()
    regions = data.get("regions", [])
    threshold = data.get("threshold_ms", 0)

    # Load sample telemetry bundle
    df = pd.read_csv("telemetry.csv")  # Suppose your data file is included in the repo

    results = {}

    for region in regions:
        region_df = df[df["region"] == region]
        if region_df.empty:
            continue

        avg_latency = region_df["latency_ms"].mean()
        p95_latency = np.percentile(region_df["latency_ms"], 95)
        avg_uptime = region_df["uptime"].mean()
        breaches = (region_df["latency_ms"] > threshold).sum()

        results[region] = {
            "avg_latency": round(avg_latency, 2),
            "p95_latency": round(p95_latency, 2),
            "avg_uptime": round(avg_uptime, 2),
            "breaches": int(breaches)
        }

    return results
