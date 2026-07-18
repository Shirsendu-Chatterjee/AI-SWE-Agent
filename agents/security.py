from llm import ask
from utils.workspace import static_scan

SYS = """You are an application security engineer. Given source code and a
list of static-analysis findings, check for SQL injection, command
injection, XSS, CSRF, hardcoded secrets/keys, and unsafe dependencies.
Write a short security report referencing specific files/lines. End with
exactly one line: "VERDICT: SECURE" or "VERDICT: VULNERABLE"."""


def security_node(state):
    src = "\n\n".join(f"# FILE: {n}\n{c}" for n, c in state["files"].items())
    static_findings = static_scan(state["files"])
    prompt = f"Static scan findings:\n{static_findings}\n\nCode:\n{src}"
    report = ask(SYS, prompt)
    ok = "SECURE" in report.strip().upper().splitlines()[-1]
    return {"security_report": report, "security_ok": ok}
