import os

from dotenv import find_dotenv, load_dotenv

print("Key in environment before loading?", "OPENAI_API_KEY" in os.environ)

env_path = find_dotenv()
print(".env file found at:", env_path)

load_dotenv(env_path)

api_key = os.getenv("OPENAI_API_KEY")
if api_key is None:
    raise SystemExit("❌ OPENAI_API_KEY not found. Check AI-claude/.env")

print("Key in environment after loading? ", "OPENAI_API_KEY" in os.environ)
print("Key loaded:", api_key[:8] + "..." + api_key[-4:])
