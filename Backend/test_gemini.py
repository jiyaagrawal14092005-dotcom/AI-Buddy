from dotenv import load_dotenv
from google import genai
import os


load_dotenv()


api_key = os.getenv("GEMINI_API_KEY")


if not api_key:
    print("❌ GEMINI_API_KEY is missing from .env")
    raise SystemExit(1)


try:
    client = genai.Client(
        api_key=api_key
    )

    response = client.models.generate_content(
        model="gemini-3.6-flash",
        contents="Reply with exactly: AI Buddy Gemini test successful."
    )

    print("✅ GEMINI API KEY IS WORKING")
    print("Model response:")
    print(response.text)

except Exception as error:
    print("❌ GEMINI API / REQUEST ERROR")
    print(error)