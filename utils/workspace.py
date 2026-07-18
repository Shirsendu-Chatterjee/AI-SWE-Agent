import os
import re
import time
import subprocess

FILE_RE = re.compile(r"```[a-zA-Z0-9_+-]*\n# FILE:\s*(?P<name>\S+)\n(?P<body>.*?)```", re.DOTALL)

# crude static checks — a fast first pass before the LLM security review
SECURITY_PATTERNS = {
    "eval(": "use of eval()",
    "exec(": "use of exec()",
    "os.system(": "shell command via os.system",
    "shell=True": "subprocess with shell=True",
    "pickle.loads": "unsafe deserialization (pickle)",
    "% (": "possible string-formatted SQL query",
}
SECRET_RE = re.compile(r"(api[_-]?key|secret|password|token)\s*=\s*[\"'][^\"']{6,}[\"']", re.IGNORECASE)


def parse_files(text: str) -> dict:
    """Extract {filename: content} from ```lang\\n# FILE: path\\n<code>``` blocks."""
    files = {}
    for m in FILE_RE.finditer(text or ""):
        files[m.group("name").strip()] = m.group("body").strip() + "\n"
    return files


def write_files(base_dir: str, files: dict) -> None:
    for name, body in files.items():
        path = os.path.join(base_dir, name)
        os.makedirs(os.path.dirname(path) or ".", exist_ok=True)
        with open(path, "w") as f:
            f.write(body)


def run_pytest(base_dir: str, timeout: int = 60):
    start = time.time()
    try:
        proc = subprocess.run(
            ["python3", "-m", "pytest", base_dir, "-q"],
            capture_output=True, text=True, timeout=timeout, cwd=base_dir,
        )
        output = proc.stdout + "\n" + proc.stderr
        passed = proc.returncode == 0
    except subprocess.TimeoutExpired:
        output = f"tests timed out after {timeout}s"
        passed = False
    except FileNotFoundError as e:
        output = f"could not run pytest: {e}"
        passed = False
    elapsed = time.time() - start
    return passed, output, elapsed


def static_scan(files: dict) -> str:
    """Fast regex pass over generated source. Returned as plain text findings."""
    findings = []
    for name, body in files.items():
        for pattern, label in SECURITY_PATTERNS.items():
            if pattern in body:
                findings.append(f"{name}: {label}")
        for m in SECRET_RE.finditer(body):
            findings.append(f"{name}: possible hardcoded secret near '{m.group(1)}'")
    return "\n".join(findings) if findings else "no static issues found"
