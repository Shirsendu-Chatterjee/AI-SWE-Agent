from llm import ask
from utils.workspace import parse_files, write_files

SYS = """You are a DevOps engineer. Given the source files, produce
deployment artifacts for this project. Output fenced code blocks, first
line inside each exactly:
# FILE: relative/path
Produce at least Dockerfile, docker-compose.yml and
.github/workflows/ci.yml (install deps, run pytest). No explanations
outside the blocks."""


def deployment_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    raw = ask(SYS, src)
    deployment = parse_files(raw)
    if not deployment:
        deployment = {"Dockerfile": raw}
    write_files(state["workspace"], deployment)
    return {"deployment": deployment}
