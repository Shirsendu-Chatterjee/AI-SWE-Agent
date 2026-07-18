from llm import ask

SYS = """You are a strict senior code reviewer. Look for hallucinated APIs,
dead code, duplicate logic, code smells, SOLID violations, naming issues and
architectural problems. Write your findings like a real PR review. End your
response with exactly one line: "VERDICT: APPROVED" or "VERDICT: REJECTED"."""


def review_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    tests = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["test_files"].items())
    prompt = (
        f"Code:\n{src}\n\nTests:\n{tests}\n\n"
        f"Test run passed: {state['tests_passed']}\nPytest output:\n{state['test_output']}"
    )
    review = ask(SYS, prompt)
    approved = "APPROVED" in review.strip().upper().splitlines()[-1]
    return {"review": review, "approved": approved}
