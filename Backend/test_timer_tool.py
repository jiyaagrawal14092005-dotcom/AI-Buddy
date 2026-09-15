from app.tools.timer import TimerTool


timer_tool = TimerTool()


print("=== CREATE AND START TIMER ===")

result = timer_tool.set_timer(5)

print(result)


print("\n=== ACTIVE TIMER COUNT ===")

print(
    timer_tool.get_active_count()
)


print("\nWaiting for timer to complete...")

import time

time.sleep(6)


print("\n=== TIMER STATUS AFTER COMPLETION ===")

print(
    timer_tool.get_timer_status(
        result["timer_id"]
    )
)


print("\n=== ACTIVE TIMER COUNT AFTER COMPLETION ===")

print(
    timer_tool.get_active_count()
)