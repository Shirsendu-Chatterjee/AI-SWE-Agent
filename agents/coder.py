from llm import ask
from utils.workspace import parse_files, write_files

SYS = """You are a senior software engineer. Write complete, runnable Python
code implementing the plan. Output ONE OR MORE fenced code blocks, and the
FIRST LINE INSIDE EACH BLOCK must be exactly:
# FILE: relative/path.py
Use a clean structure (e.g. app/main.py, app/models.py, app/routes.py,
requirements.txt). No explanations outside the code blocks. No placeholders,
no TODOs — every function must be fully implemented."""


def code_node(state):
    prompt = f"Plan:\n{state['plan']}\n\nRequirement:\n{state['requirement']}"

    if state.get("test_output") and not state.get("tests_passed", True):
        prompt += f"\n\nTests FAILED, fix the code. Pytest output:\n{state['test_output']}"
    if state.get("review") and not state.get("approved", True):
        prompt += f"\n\nCode review rejected the code, address this:\n{state['review']}"
    if state.get("security_report") and not state.get("security_ok", True):
        prompt += f"\n\nSecurity review found issues, fix them:\n{state['security_report']}"
    if state.get("files"):
        existing = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
        prompt += f"\n\nPrevious files (revise these, keep the same paths):\n{existing}"

    raw = ask(SYS, prompt)
    files = parse_files(raw)
    if not files:
        files = {"app/main.py": raw}

    write_files(state["workspace"], files)
    return {"files": files, "iteration": state.get("iteration", 0) + 1}
