from getpass import getpass

import requests

api_key = getpass("Paste your OpenAI API key (input is hidden): ").strip()

masked = api_key[:8] + "..." + api_key[-4:]
print("Key received:", masked)

response = requests.get(
    "https://api.openai.com/v1/models",
    headers={"Authorization": f"Bearer {api_key}"},
    timeout=30,
)

print("Status code :", response.status_code)

if response.status_code == 200:
    model_ids = [model["id"] for model in response.json()["data"]]
    print("Key works ✅  models visible:", len(model_ids))
    print("A few of them:", sorted(model_ids)[:5])
else:
    print("Key rejected ❌ ", response.text[:200])
