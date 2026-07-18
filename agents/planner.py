from llm import ask

SYS = """You are a software planner. Given a requirement, produce a concrete
implementation plan covering: entities/data model, endpoints or functions,
auth (if relevant), and edge cases. Keep it under 250 words, no fluff."""


def plan_node(state):
    plan = ask(SYS, state["requirement"])
    return {"plan": plan}
