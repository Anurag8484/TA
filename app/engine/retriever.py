import json
import os
import requests
import numpy as np
from typing import List

AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")
EMBEDDING_MODEL = "text-embedding-3-small"
EMBEDDING_URL = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
EMBEDDED_CORPUS_PATH = "app/data/processed/corpus_with_embeddings.jsonl"

HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json"
}


def cosine_similarity(a: List[float], b: List[float]) -> float:
    a, b = np.array(a), np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def get_query_embedding(text: str) -> List[float]:
    response = requests.post(
        EMBEDDING_URL,
        headers=HEADERS,
        json={"model": EMBEDDING_MODEL, "input": [text]}
    )
    response.raise_for_status()
    return response.json()["data"][0]["embedding"]


def get_top_chunks(query: str, k: int = 5) -> List[dict]:
    query_emb = get_query_embedding(query)

    chunks = []
    with open(EMBEDDED_CORPUS_PATH, "r", encoding="utf-8") as f:
        for line in f:
            item = json.loads(line)
            sim = cosine_similarity(query_emb, item["embedding"])
            item["similarity"] = sim
            chunks.append(item)

    sorted_chunks = sorted(chunks, key=lambda x: x["similarity"], reverse=True)
    return sorted_chunks[:k]
