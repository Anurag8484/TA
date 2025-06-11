# # # app/engine/llm.py

# import os
# import requests
# from dotenv import load_dotenv

# load_dotenv()  # Load variables from .env

# AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
# AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")  # Read from .env


# # load_dotenv()
# # AIPROXY_TOKEN = os.getenv("AIPROXY_TOKEN")  # Move this after load
# # print("✅ AIPROXY_TOKEN:", AIPROXY_TOKEN)



# # def ask_llm(system_prompt: str, user_prompt: str) -> str:
# #     if not AIPROXY_TOKEN:
# #         raise EnvironmentError("Missing AIPROXY_TOKEN in .env")

# #     headers = {
# #         "Content-Type": "application/json",
# #         "Authorization": f"Bearer {AIPROXY_TOKEN}"
# #     }

# #     payload = {
# #         "model": "gpt-4o-mini",
# #         "messages": [
# #             {"role": "system", "content": system_prompt},
# #             {"role": "user", "content": user_prompt}
# #         ]
# #     }

# #     response = requests.post(AIPROXY_URL, headers=headers, json=payload)
# #     response.raise_for_status()
# #     return response.json()["choices"][0]["message"]["content"]
# def ask_llm(system_prompt: str, user_prompt: str) -> str:
#     if not AIPROXY_TOKEN:
#         raise EnvironmentError("Missing AIPROXY_TOKEN in .env")

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

#     response = requests.post(AIPROXY_URL, headers=headers, json=payload)

#     try:
#         response.raise_for_status()
#         data = response.json()
#         # Debug log
#         print("🔍 LLM response JSON:", data)

#         return data["choices"][0]["message"]["content"]
#     except requests.exceptions.HTTPError as e:
#         print("❌ HTTP Error:", e)
#         print("🔍 Response content:", response.text)
#         raise
#     except KeyError as e:
#         print("❌ Unexpected response structure:", response.json())
#         raise ValueError(f"Unexpected LLM response structure: missing {e}")

import os
import requests

from dotenv import load_dotenv
load_dotenv(dotenv_path=".env", override=True)  # Force reload


AIPROXY_URL = "https://aiproxy.sanand.workers.dev/openai/v1/chat/completions"
AIPROXY_TOKEN = os.getenv("OPENAI_API_KEY")


def ask_llm(system_prompt: str, user_prompt: str) -> str:
    if not AIPROXY_TOKEN:
        raise EnvironmentError("❌ Missing AIPROXY_TOKEN in .env")

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

    print("📤 Sending to AI Proxy:", payload)

    response = requests.post(AIPROXY_URL, headers=headers, json=payload)

    try:
        response.raise_for_status()
        data = response.json()
        print("✅ LLM raw response:", data)
        print("✅ AIPROXY_TOKEN found:", bool(AIPROXY_TOKEN))
        return data["choices"][0]["message"]["content"]
    except Exception as e:
        print("❌ LLM Error:", e)
        print("❌ Full response text:", response.text)
        raise
