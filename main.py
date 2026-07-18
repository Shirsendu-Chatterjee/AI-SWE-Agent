import sys
import os
import uuid
from graph import build_graph

if __name__ == "__main__":
    requirement = " ".join(sys.argv[1:]) or "Create a REST API for a todo list."
    run_id = uuid.uuid4().hex[:8]
    workspace = os.path.join("workspaces", run_id)
    os.makedirs(workspace, exist_ok=True)

    app = build_graph()
    result = app.invoke({
        "requirement": requirement,
        "run_id": run_id,
        "workspace": workspace,
        "plan": "",
        "files": {},
        "test_files": {},
        "tests_passed": False,
        "test_output": "",
        "test_time": 0.0,
        "review": "",
        "approved": False,
        "security_report": "",
        "security_ok": False,
        "performance_report": "",
        "docs": {},
        "deployment": {},
        "iteration": 0,
    })

    print(f"\nrun_id: {run_id}  (files written to {workspace}/)\n")
    print("=== PLAN ===\n", result["plan"])
    print("\n=== TESTS PASSED ===", result["tests_passed"], f"({result['test_time']:.2f}s)")
    print("\n=== REVIEW VERDICT ===", "APPROVED" if result["approved"] else "REJECTED (max iterations hit)")
    print("\n=== SECURITY ===", "SECURE" if result["security_ok"] else "VULNERABLE (max iterations hit)")
    print("\n=== PERFORMANCE NOTES ===\n", result["performance_report"])
    print("\nfiles:", list(result["files"].keys()))
    print("tests:", list(result["test_files"].keys()))
    print("docs:", list(result["docs"].keys()))
    print("deployment:", list(result["deployment"].keys()))
    print(f"\niterations used: {result['iteration']}/{3}")
