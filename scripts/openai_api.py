import os
import sys
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load .env from parent folder of scripts ---
env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
if not os.path.exists(env_path):
    print(f"Error: .env file not found at {env_path}")
    sys.exit(1)

load_dotenv(env_path)

# --- Get Gemini API Key ---
api_key = os.getenv("GEMINI_API_KEY")
if not api_key:
    print("Error: GEMINI_API_KEY not found in .env file.")
    sys.exit(1)

# --- Configure Gemini ---
genai.configure(api_key=api_key)

def explain_phishing(text: str) -> str:
    """
    Use Google's Gemini API to explain why the given message may be phishing.
    """
    try:
        model = genai.GenerativeModel("gemini-1.5-flash")  # free & fast
        prompt = f"""
        The following message was flagged as phishing.
        Explain in around two features why it is most likely a phishing message as well as what it is targeting out of the user.
        Suggest what the recipient should do next.

        Message:
        \"\"\"{text}\"\"\"
        """
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No explanation generated."
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

# --- Example usage ---
if __name__ == "__main__":
    sample_text = "Upgrade your sex and pleasures with these techniques http://www.brightmade.com"
    explanation = explain_phishing(sample_text)
    print("Explanation:\n", explanation)
