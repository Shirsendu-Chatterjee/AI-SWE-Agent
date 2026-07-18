import os
from openai import OpenAI

from dotenv import load_dotenv
from langchain_openrouter import ChatOpenRouter

load_dotenv()

LLM = ChatOpenRouter(
    model="nvidia/nemotron-3-ultra-550b-a55b:free",
    temperature=0,
)


def ask(system: str, user: str) -> str:
    response = LLM.invoke("Explain vectorless RAG.")
    return response.content
