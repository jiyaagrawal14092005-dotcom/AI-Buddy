from app.tools.email_tool import EmailTool


email_tool = EmailTool()


print("=== EMAIL TOOL INFO ===")

print(
    email_tool.get_info()
)


print("\n=== VALID EMAIL ===")

print(
    email_tool.execute({
        "recipient": "test@example.com",
        "subject": "AI Buddy Test",
        "message": "This is a test email action."
    })
)


print("\n=== EMAIL USING 'email' FIELD ===")

print(
    email_tool.execute({
        "email": "user@example.com",
        "subject": "AI Buddy",
        "message": "Testing email tool."
    })
)


print("\n=== INVALID EMAIL ===")

print(
    email_tool.execute({
        "recipient": "invalid-email",
        "subject": "Test",
        "message": "Testing invalid email."
    })
)


print("\n=== EMPTY SUBJECT ===")

print(
    email_tool.execute({
        "recipient": "test@example.com",
        "subject": "",
        "message": "Testing empty subject."
    })
)


print("\n=== EMPTY MESSAGE ===")

print(
    email_tool.execute({
        "recipient": "test@example.com",
        "subject": "Test",
        "message": ""
    })
)


print("\n=== EMAIL AVAILABILITY ===")

print(
    email_tool.is_available()
)