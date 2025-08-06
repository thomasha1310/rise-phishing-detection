import os
from dotenv import load_dotenv
from google import genai

# Load environment variables from .env
load_dotenv()

# Retrieve API key
api_key = os.getenv('GEMINI_API_KEY')
if not api_key:
    raise RuntimeError("Missing GEMINI_API_KEY in .env file")

client = genai.Client(api_key=api_key)

response = client.models.generate_content(
    model="gemini-2.5-flash",
    contents="Explain how AI works in one sentence."
)

print(response.text)