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
        model = genai.GenerativeModel("gemini-2.5-flash")  # free & fast
        prompt = f"""
        The following message was flagged as phishing.
        Explain in around two sentences why it is most likely a phishing message as well as what it is targeting out of the user.
        Provide a 1-2 sentence suggestion on what the recipient should do next.
        Direct all messages as if you are speaking directly to the recipient of the email

        Message:
        \"\"\"{text}\"\"\"
        """
        response = model.generate_content(prompt)
        return response.text.strip() if response.text else "No explanation generated."
    except Exception as e:
        return f"Error contacting Gemini API: {e}"

# --- Example usage ---
if __name__ == "__main__":
    sample_text = """Quick Quiz - What is the hottest thing in Costa Rica

Answer - the real estate market

You have got to check out this view!!!!



http://www.campaignmccain.net/quick_quiz/reserva.html





To decline from future promotions of this offer,
see the following:
http://www.campaignmccain.net/quick_quiz/unsb.html

or mail:

Costa Reserva
421 Leroy Drive
Corona, CA 92879
kZcPLdYZaYW_bCWULGaeJQW\\8fXIc[XYcS9UC




DesertDeals is proud to being you hand selected offerings. 
However, to be excluded please visit 
http://www.campaignmccain.net/unsub.jsp?=producttestpanel@gvc.ceas-challenge.cc
or write us at ADOBE ONE 40 E Chicago Avenue #240 Chicago, IL 
60611
"""
    explanation = explain_phishing(sample_text)
    print("Explanation:\n", explanation)
