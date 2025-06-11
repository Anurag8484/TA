from app.engine.answer_engine import generate_answer

response = generate_answer("How are GA5 marks calculated?", k=3)

print("💬 Answer:\n", response["answer"], "\n")
print("🔗 Links:")
for link in response["links"]:
    print(f"- {link['text']} → {link['url']}")
