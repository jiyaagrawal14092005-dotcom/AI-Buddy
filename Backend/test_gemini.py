from dotenv import load_dotenv
from google import genai
import os

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    print("❌ API key nahi mili.")
    exit()

try:
    client = genai.Client(api_key=api_key)

    response = client.models.generate_content(
        model="gemini-3.7-flash",
        contents="Reply with only: Gemini API is working."
    )

    print("✅ API KEY VALID!")
    print("Gemini response:", response.text)

except Exception as e:
    print("❌ API KEY / API REQUEST ERROR")
    print(e)