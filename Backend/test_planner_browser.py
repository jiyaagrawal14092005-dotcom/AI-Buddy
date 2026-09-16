from app.agent.planner import Planner


planner = Planner()


print("=== PLANNER BROWSER TEST ===")


# =================================
# TEST 1: OPEN
# =================================

print("\n=== TEST 1: OPEN ===")

open_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "open",
        "url": "https://example.com"
    }
}

open_plan = planner.create_plan(open_intent)

print(open_plan)


# =================================
# TEST 2: FILL
# =================================

print("\n=== TEST 2: FILL ===")

fill_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "fill",
        "url": "http://127.0.0.1:8080/test_browser_page.html",
        "selector": "#name",
        "value": "AI Buddy"
    }
}

fill_plan = planner.create_plan(fill_intent)

print(fill_plan)


# =================================
# TEST 3: CLICK
# =================================

print("\n=== TEST 3: CLICK ===")

click_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "click",
        "url": "http://127.0.0.1:8080/test_browser_page.html",
        "selector": "#submitBtn"
    }
}

click_plan = planner.create_plan(click_intent)

print(click_plan)


# =================================
# TEST 4: READ
# =================================

print("\n=== TEST 4: READ ===")

read_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "read",
        "url": "http://127.0.0.1:8080/test_browser_page.html",
        "selector": "#result"
    }
}

read_plan = planner.create_plan(read_intent)

print(read_plan)


# =================================
# TEST 5: CLOSE
# =================================

print("\n=== TEST 5: CLOSE ===")

close_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "close"
    }
}

close_plan = planner.create_plan(close_intent)

print(close_plan)


# =================================
# TEST 6: INVALID ACTION
# =================================

print("\n=== TEST 6: INVALID ACTION ===")

invalid_intent = {
    "intent": "BROWSE_WEB",
    "parameters": {
        "action": "delete",
        "url": "https://example.com"
    }
}

invalid_plan = planner.create_plan(invalid_intent)

print(invalid_plan)


# =================================
# FINAL VERIFICATION
# =================================

print("\n=== FINAL VERIFICATION ===")

tests_passed = 0
tests_total = 6


if (
    open_plan["success"] is True
    and open_plan["tool"] == "browser"
):
    tests_passed += 1


if (
    fill_plan["success"] is True
    and fill_plan["tool"] == "browser"
):
    tests_passed += 1


if (
    click_plan["success"] is True
    and click_plan["tool"] == "browser"
):
    tests_passed += 1


if (
    read_plan["success"] is True
    and read_plan["tool"] == "browser"
):
    tests_passed += 1


if (
    close_plan["success"] is True
    and close_plan["tool"] == "browser"
):
    tests_passed += 1


if (
    invalid_plan["success"] is False
):
    tests_passed += 1


print(
    f"TESTS PASSED: {tests_passed}/{tests_total}"
)


if tests_passed == tests_total:

    print("PLANNER BROWSER TEST: PASS")

else:

    print("PLANNER BROWSER TEST: FAIL")