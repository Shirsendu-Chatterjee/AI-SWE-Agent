from llm import ask

SYS = """You are a performance engineer. Given source code and how long its
test suite took to run, identify likely latency/memory/CPU hotspots
(N+1 queries, unbounded loops, missing indexes/caching, blocking I/O) and
suggest concrete optimizations. Keep it under 200 words."""


def performance_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    prompt = f"Test suite runtime: {state['test_time']:.2f}s\n\nCode:\n{src}"
    report = ask(SYS, prompt)
    return {"performance_report": report}
