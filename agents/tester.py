from llm import ask
from utils.workspace import parse_files, write_files, run_pytest

SYS = """You are a QA engineer. Given source files, write pytest tests
(normal cases + edge cases). Output ONE OR MORE fenced code blocks; the
FIRST LINE INSIDE EACH BLOCK must be exactly:
# FILE: tests/test_whatever.py
Import the code under test using its module path as given. No explanations
outside code blocks."""


def test_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    raw = ask(SYS, src)
    test_files = parse_files(raw)
    if not test_files:
        test_files = {"tests/test_generated.py": raw}

    write_files(state["workspace"], test_files)
    passed, output, elapsed = run_pytest(state["workspace"])
    return {
        "test_files": test_files,
        "tests_passed": passed,
        "test_output": output,
        "test_time": elapsed,
    }
