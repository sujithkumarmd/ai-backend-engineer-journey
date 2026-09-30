import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://api.openai.com/v1/responses"
headers = {
    "Authorization": f"Bearer {os.getenv('OPENAI_API_KEY')}",
    "Content-Type": "application/json",
}
body = {
    "model": "gpt-6-luna",
    "input": "Name one planet. Answer in one word.",
}

http_response = requests.post(url, headers=headers, json=body, timeout=60)
print("HTTP status:", http_response.status_code)
if http_response.status_code != 200:
    raise SystemExit(http_response.text)

data = http_response.json()
print(json.dumps(data, indent=2))

# Find the reply by hand: output → "message" item → content → "output_text" part
reply_parts = []
for item in data["output"]:
    if item["type"] == "message":
        for part in item["content"]:
            if part["type"] == "output_text":
                reply_parts.append(part["text"])

print("\nReply extracted by hand:", "".join(reply_parts))
