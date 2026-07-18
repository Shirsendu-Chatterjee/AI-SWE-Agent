from langgraph.graph import StateGraph, END
from state import State
from agents.planner import plan_node
from agents.coder import code_node
from agents.tester import test_node
from agents.reviewer import review_node
from agents.security import security_node
from agents.performance import performance_node
from agents.documentation import documentation_node
from agents.deployment import deployment_node

MAX_ITER = 3  # cap on coder re-runs across tester/reviewer/security gates


def after_tester(state: State):
    if not state["tests_passed"] and state["iteration"] < MAX_ITER:
        return "coder"
    return "reviewer"


def after_reviewer(state: State):
    if not state["approved"] and state["iteration"] < MAX_ITER:
        return "coder"
    return "security"


def after_security(state: State):
    if not state["security_ok"] and state["iteration"] < MAX_ITER:
        return "coder"
    return "performance"


def build_graph():
    g = StateGraph(State)
    g.add_node("planner", plan_node)
    g.add_node("coder", code_node)
    g.add_node("tester", test_node)
    g.add_node("reviewer", review_node)
    g.add_node("security", security_node)
    g.add_node("performance", performance_node)
    g.add_node("documentation", documentation_node)
    g.add_node("deployment", deployment_node)

    g.set_entry_point("planner")
    g.add_edge("planner", "coder")
    g.add_edge("coder", "tester")
    g.add_conditional_edges("tester", after_tester, {"coder": "coder", "reviewer": "reviewer"})
    g.add_conditional_edges("reviewer", after_reviewer, {"coder": "coder", "security": "security"})
    g.add_conditional_edges("security", after_security, {"coder": "coder", "performance": "performance"})
    g.add_edge("performance", "documentation")
    g.add_edge("documentation", "deployment")
    g.add_edge("deployment", END)

    return g.compile()
