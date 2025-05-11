from fastapi import FastAPI, Request
from pydantic import BaseModel
from typing import List, Literal, Union
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from run import run_simulation

app = FastAPI()


class ScheduleRequest(BaseModel):
    algorithm: Literal["fcfs", "sstf", "scan", "c-scan", "look", "c-look"]
    requests: List[int]
    initial: int
    final: int


app.mount("/static", StaticFiles(directory="static"), name="static")

# Point to templates directory
templates = Jinja2Templates(directory="templates")


# Route to render your HTML
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
