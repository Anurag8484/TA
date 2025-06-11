import os
import requests
from app.engine.retriever import get_top_chunks
from app.engine.llm import ask_llm

AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")
COMPLETION_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
MODEL = "gpt-4o-mini"

HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json"
}


def build_prompt(query: str, context_chunks: list) -> str:
    context_text = "\n\n".join(chunk["text"] for chunk in context_chunks)
    return f"""You are a helpful teaching assistant for a college course. Use the following context to answer the question.

Context:
{context_text}

Question: {query}
Answer:"""


def generate_answer(query: str) -> dict:
    top_chunks = get_top_chunks(query, k=3)

    context = "\n\n".join(chunk["text"] for chunk in top_chunks)
    system_prompt = (
        "You are a helpful teaching assistant for the Tools in Data Science (TDS) course. "
        "Use only the context provided. If unsure, say you don't know. "
        "Always link back to the original source when possible."
    )

    user_prompt = f"Context:\n{context}\n\nQuestion: {query}"

    # 🧠 Call the LLM
    answer = ask_llm(system_prompt, user_prompt)

    # 🔗 Include traceable links
    links = [
        {"url": chunk["source"], "text": chunk.get("title", "Source")}
        for chunk in top_chunks if "source" in chunk
    ]
    # app/engine/answer_engine.py




    # 🐞 Debug logs

    return {"answer": answer.strip(), "links": links}
