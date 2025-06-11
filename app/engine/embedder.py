import json
import os
import time
import requests
from tqdm import tqdm

AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")  # Set this in your environment

HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json"
}


def get_embedding(text):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]


def embed_corpus(in_path="app/data/processed/corpus.jsonl", out_path="app/data/processed/corpus_with_embeddings.jsonl"):
    with open(in_path, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f]

    out_file = open(out_path, "w", encoding="utf-8")
    for entry in tqdm(entries, desc="Embedding chunks"):
        try:
            embedding = get_embedding(entry["text"])
            entry["embedding"] = embedding
            out_file.write(json.dumps(entry) + "\n")
            time.sleep(0.6)  # to stay within rate limits
        except Exception as e:
            print("❌ Error embedding:", entry["text"][:50], str(e))
            continue
    out_file.close()
    print(f"✅ Saved embeddings to: {out_path}")
import json
import os
import time
import requests
from tqdm import tqdm

AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")  # Set this in your environment

HEADERS = {
    "Authorization": f"Bearer {AIPROXY_TOKEN}",
    "Content-Type": "application/json"
}


def get_embedding(text):
    url = "https://aiproxy.sanand.workers.dev/openai/v1/embeddings"
    data = {
        "model": "text-embedding-3-small",
        "input": [text]
    }
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    return r.json()["data"][0]["embedding"]


def embed_corpus(in_path="app/data/processed/corpus.jsonl", out_path="app/data/processed/corpus_with_embeddings.jsonl"):
    with open(in_path, "r", encoding="utf-8") as f:
        entries = [json.loads(line) for line in f]

    out_file = open(out_path, "w", encoding="utf-8")
    for entry in tqdm(entries, desc="Embedding chunks"):
        try:
            embedding = get_embedding(entry["text"])
            entry["embedding"] = embedding
            out_file.write(json.dumps(entry) + "\n")
            time.sleep(0.6)  # to stay within rate limits
        except Exception as e:
            print("❌ Error embedding:", entry["text"][:50], str(e))
            continue
    out_file.close()
    print(f"✅ Saved embeddings to: {out_path}")

if __name__ == "__main__":
    embed_corpus()
