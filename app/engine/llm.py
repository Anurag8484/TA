import os
import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=".env", override=True)  # Load .env with priority

AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")  # Note: this is still for AI Proxy


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    if not AIPROXY_TOKEN:
        raise EnvironmentError("❌ Missing OPENAI_API_KEY in .env")

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AIPROXY_TOKEN}"
    }

    payload = {
        "model": "gpt-4o-mini",
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    }

    response = requests.post(AIPROXY_URL, headers=headers, json=payload)

    try:
        response.raise_for_status()
        data = response.json()

        # ✅ Minimal but useful feedback
        content = data["choices"][0]["message"]["content"]
        cost = data.get("cost")
        if cost is not None:
            print(f"✅ LLM responded successfully. 💰 Cost: ${cost:.6f}")
        else:
            print("✅ LLM responded successfully.")

        return content

    except requests.exceptions.HTTPError as e:
        print("❌ HTTP Error:", e)
        print("🔍 Response content:", response.text)
        raise
    except KeyError as e:
        print("❌ Unexpected response structure. Missing key:", e)
        print("🔍 Full response:", response.json())
        raise

# import os
# import requests

# from dotenv import load_dotenv
# load_dotenv(dotenv_path=".env", override=True)  # Force reload


# AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
# AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")


# def ask_llm(system_prompt: str, user_prompt: str) -> str:
#     if not AIPROXY_TOKEN:
#         raise EnvironmentError("❌ Missing AIPROXY_TOKEN in .env")

#     headers = {
#         "Content-Type": "application/json",
#         "Authorization": f"Bearer {AIPROXY_TOKEN}"
#     }

#     payload = {
#         "model": "gpt-4o-mini",
#         "messages": [
#             {"role": "system", "content": system_prompt},
#             {"role": "user", "content": user_prompt}
#         ]
#     }

#     print("📤 Sending to AI Proxy:", payload)

#     response = requests.post(AIPROXY_URL, headers=headers, json=payload)

#     try:
#         response.raise_for_status()
#         data = response.json()
#         print("✅ LLM raw response:", data)
#         print("✅ AIPROXY_TOKEN found:", bool(AIPROXY_TOKEN))
#         return data["choices"][0]["message"]["content"]
#     except Exception as e:
#         print("❌ LLM Error:", e)
#         print("❌ Full response text:", response.text)
#         raise
