from llm import ask
from utils.workspace import parse_files, write_files

SYS = """You are a technical writer. Given the requirement, plan, and source
files, write project documentation. Output fenced code blocks, first line
inside each exactly:
# FILE: relative/path.md
Produce at least README.md (setup + usage) and docs/API.md (endpoints/
functions, params, responses). No explanations outside the blocks."""


def documentation_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    prompt = f"Requirement:\n{state['requirement']}\n\nPlan:\n{state['plan']}\n\nCode:\n{src}"
    raw = ask(SYS, prompt)
    docs = parse_files(raw)
    if not docs:
        docs = {"README.md": raw}
    write_files(state["workspace"], docs)
    return {"docs": docs}
