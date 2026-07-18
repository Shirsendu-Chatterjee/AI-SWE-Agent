from typing import TypedDict


class State(TypedDict):
    requirement: str      # original user requirement
    run_id: str            # unique id for this run
    workspace: str         # dir on disk where generated files live

    plan: str              # planner output

    files: dict            # filename -> source code content
    test_files: dict       # filename -> test code content
    tests_passed: bool
    test_output: str       # captured pytest stdout/stderr
    test_time: float       # seconds, rough perf signal

    review: str
    approved: bool

    security_report: str
    security_ok: bool

    performance_report: str

    docs: dict             # filename -> generated doc content
    deployment: dict       # filename -> generated deployment file content

    iteration: int         # how many times the coder has (re)run
