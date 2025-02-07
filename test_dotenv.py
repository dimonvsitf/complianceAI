from dotenv import load_dotenv
import os

print("Testing python-dotenv...")
load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
print(f"OPENAI_API_KEY found: {'Yes' if api_key else 'No'}")
if api_key:
    print(f"API key starts with: {api_key[:5]}...")
