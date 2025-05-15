from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Literal, Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from run import run_simulation
from typing import List, Literal, Optional
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Or specify your frontend origin if known
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ScheduleRequest(BaseModel):
    algorithm: Literal["fcfs", "sstf", "scan", "c-scan", "look", "c-look"]
    requests: List[int]
    initial: int
    final: int

class MemoryRequest(BaseModel):
    algorithm: Literal[
        "lru", "optimal", "second chance", "fifo", "sstf", "arb", "scan", "c-scan", "look", "c-look"
    ]
    requests: List[int]
    initial: int
    final: Optional[int] = None  # Final is optional for non-disk algorithms


app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("Simulate.html", {"request": request})


@app.post("/run-scheduling")
def run_scheduling(data: ScheduleRequest):
    alg = data.algorithm
    inp = data.requests
    ini = data.initial
    final = data.final
    output = run_simulation(alg, inp, ini, final)

    frame_states = output.get("cylinders", [])
    faults = output.pop("seek_time", 0)

    return {"seek_time": faults, "cylinders": frame_states}

@app.post("/run-memory")
def run_memory_scheduling(data: MemoryRequest):
    output = run_simulation(data.algorithm, data.requests, data.initial, data.final)

    return {
        "frame_states": output.get("frame_states", output.get("cylinders", [])),
        "logs": output.get("logs", []),
        "faults": output.get("faults", output.get("seek_time", 0)),
    }


# python -m uvicorn main:app --reload --port 8001