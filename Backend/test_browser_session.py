from app.tools.browser_session import BrowserSession


session = BrowserSession()

test_url = (
    "http://127.0.0.1:8080/"
    "test_browser_page.html"
)


print("=== START SESSION ===")

page = session.start()

print("Session active:", session.is_active())


print("\n=== OPEN PAGE ===")

page_data = session.open(
    test_url
)

print(page_data)


print("\n=== FILL INPUT ===")

page.locator(
    "#name"
).fill(
    "AI Buddy"
)

print("Input filled successfully.")


print("\n=== CLICK BUTTON ===")

page.locator(
    "#submitBtn"
).click()

print("Button clicked successfully.")


print("\n=== READ RESULT ===")

result = page.locator(
    "#result"
).inner_text()

print("Result:", result)


print("\n=== CLOSE SESSION ===")

session.close()

print("Session active:", session.is_active())