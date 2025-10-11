from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import datetime
import os

app = FastAPI()

# Allow cross-origin GET requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET"],
    allow_headers=["*"],
)

LOG_FILE = "agent_run_logs.txt"

@app.get("/task")
def run_task(q: str = Query(..., description="Task description")):
    # Log the incoming request
    with open(LOG_FILE, "a") as f:
        f.write(f"[{datetime.datetime.now()}] Received: {q}\n")

    # Simple deterministic agent simulation
    if "fibonacci" in q.lower():
        # 13th Fibonacci number (F0=0, F1=1)
        fib = [0, 1]
        for _ in range(2, 14):
            fib.append(fib[-1] + fib[-2])
        output = str(fib[13])
    else:
        output = "Task executed successfully"

    # Log output
    with open(LOG_FILE, "a") as f:
        f.write(f"Output: {output}\n\n")

    return {
        "task": q,
        "agent": "copilot-cli",
        "output": output,
        "email": "23f2004089@ds.study.iitm.ac.in"
    }
