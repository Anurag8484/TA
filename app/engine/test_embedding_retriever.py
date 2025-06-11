from app.engine.retriever import get_top_chunks

results = get_top_chunks("What is Project 1 about", k=3)

for r in results:
    print("🔗", r["source"])
    print(r["text"][:300])
    print("---")
