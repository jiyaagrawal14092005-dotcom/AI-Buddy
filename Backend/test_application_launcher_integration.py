import requests


URL = "http://127.0.0.1:8000/api/chat"


def send_command(message: str, user_id: int = 1):
    response = requests.post(
        URL,
        json={
            "message": message,
            "user_id": user_id
        },
        timeout=30
    )

    print("\nHTTP STATUS:")
    print(response.status_code)

    print("\nRESPONSE:")
    print(response.json())

    return response


print("=== AI BUDDY APPLICATION LAUNCHER INTEGRATION TEST ===")

print("\n=== TEST 1: OPEN CALCULATOR ===")

send_command(
    "Open calculator"
)


print("\n" + "=" * 70)

print("\n=== TEST 2: OPEN NOTEPAD ===")

send_command(
    "Open notepad"
)