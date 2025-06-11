from app.engine.llm import ask_llm

system_prompt = "You are a helpful assistant."
user_prompt = "What is 2 + 2?"

print(ask_llm(system_prompt, user_prompt))
