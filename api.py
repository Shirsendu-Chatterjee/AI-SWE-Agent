import os
import uuid
import shutil
from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from graph import build_graph

app = FastAPI(title="AI Software Engineering Agent")
graph = build_graph()
RUNS: dict = {}  # run_id -> {"status": "running"|"done"|"error", ...}


class RunRequest(BaseModel):
    requirement: str


def _execute(run_id: str, requirement: str):
    workspace = os.path.join("workspaces", run_id)
    os.makedirs(workspace, exist_ok=True)
    try:
        result = graph.invoke({
            "requirement": requirement,
            "run_id": run_id,
            "workspace": workspace,
            "plan": "", "files": {}, "test_files": {},
            "tests_passed": False, "test_output": "", "test_time": 0.0,
            "review": "", "approved": False,
            "security_report": "", "security_ok": False,
            "performance_report": "", "docs": {}, "deployment": {},
            "iteration": 0,
        })
        RUNS[run_id] = {"status": "done", "result": result}
    except Exception as e:
        RUNS[run_id] = {"status": "error", "error": str(e)}


@app.post("/run")
def start_run(req: RunRequest, background_tasks: BackgroundTasks):
    run_id = uuid.uuid4().hex[:8]
    RUNS[run_id] = {"status": "running"}
    background_tasks.add_task(_execute, run_id, req.requirement)
    return {"run_id": run_id}


@app.get("/runs/{run_id}")
def get_run(run_id: str):
    return RUNS.get(run_id, {"status": "not_found"})


@app.get("/runs/{run_id}/download")
def download_run(run_id: str):
    workspace = os.path.join("workspaces", run_id)
    zip_path = shutil.make_archive(workspace, "zip", workspace)
    return FileResponse(zip_path, filename=f"{run_id}.zip")


# minimal dashboard, served as static files — no build step
app.mount("/", StaticFiles(directory="static", html=True), name="static")
