import os
import json
from pathlib import Path


def chunk_text(text, chunk_size=500, overlap=50):
    words = text.split()
    chunks = []
    start = 0
    while start < len(words):
        end = min(start + chunk_size, len(words))
        chunks.append(" ".join(words[start:end]))
        start += chunk_size - overlap
    return chunks


def clean_and_chunk_markdown(md_dir, source_type):
    data = []
    for path in Path(md_dir).glob("*.md"):
        with open(path, "r", encoding="utf-8") as f:
            content = f.read()

        chunks = chunk_text(content)
        for chunk in chunks:
            source = extract_first_url(
                chunk) if source_type == "discourse" else str(path.name)
            data.append({
                "text": chunk.strip(),
                "source": source,
                "source_type": source_type
            })
    return data


def extract_first_url(text):
    import re
    match = re.search(r"https?://[^\s)\]]+", text)
    return match.group(0) if match else "unknown"


def build_corpus(github_dir, discourse_dir, output_file):
    all_data = []
    all_data.extend(clean_and_chunk_markdown(github_dir, "github"))
    all_data.extend(clean_and_chunk_markdown(discourse_dir, "discourse"))

    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        for entry in all_data:
            json.dump(entry, f, ensure_ascii=False)
            f.write("\n")
    print(f"✅ Corpus saved to: {output_file} with {len(all_data)} chunks.")


if __name__ == "__main__":
    build_corpus(
        github_dir="app/data/raw/github",
        discourse_dir="app/data/raw/discourse_md",
        output_file="app/data/processed/corpus.jsonl"
    )
