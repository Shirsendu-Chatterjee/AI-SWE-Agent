# AI Software Engineering Agent (Agentic SDLC Platform)

An autonomous, multi-agent software engineering platform built with **LangGraph** and designed around **Clean Architecture** principles. This system simulates an enterprise "Smart Squad[span_0](start_span)"[span_0](end_span) to execute the end-to-end Software Development Life Cycle (SDLC)[span_1](start_span)[span_1](end_span)—transforming technical requirements into fully tested, audited, and containerized microservices[span_2](start_span)[span_2](end_span).

---

## 🏗️ Architecture & Workflow

The platform leverages a centralized **Supervisor Agent** to coordinate specialized sub-agents through a stateful graph topology:

* **Planner Agent:** Ingests requirements, designs entity schemas, and outputs structured JSON roadmaps.
* **Coding Agent:** Generates production-ready backend implementations adhering to repository architectural rules.
* **Test Agent ("Test-First" Gate):** Generates and runs `PyTest` suites[span_3](start_span)[span_3](end_span). If validation fails, it triggers an automated self-healing loop back to the Coder[span_4](start_span)[span_4](end_span).
* **Code Review Agent (Forensics):** Audits multi-file generation loops to eliminate hallucinations and ensure SOLID compliance[span_5](start_span)[span_5](end_span).
* **Security & Performance Agents:** Scans for vulnerabilities and monitors metrics using Prometheus and Grafana telemetry[span_6](start_span)[span_6](end_span).

---

## 🛠️ Tech Stack

* **Orchestration:** Python 3.12, LangGraph, LangChain, Pydantic
* **LLM Engine:** Multi-provider abstraction (OpenAI, Anthropic, Gemini, Ollama)
* **Backend:** FastAPI, SQLAlchemy, PostgreSQL, Redis, Alembic
* **DevOps & Infra:** Docker, Docker Compose, GitHub Actions, Prometheus, Grafana[span_7](start_span)[span_7](end_span)

---

## 🚀 Getting Started

### Installation & Setup

1. **Clone & Navigate:**
   ```bash
   git clone [https://github.com/Shirsendu-Chatterjee/AI-SWE-Agent.git](https://github.com/Shirsendu-Chatterjee/AI-SWE-Agent.git)
   cd AI-SWE-Agent
