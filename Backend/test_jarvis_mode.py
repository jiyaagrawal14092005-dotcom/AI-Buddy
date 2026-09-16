from app.voice.jarvis_mode import JarvisMode


jarvis = JarvisMode(
    wake_word="ai buddy",
    user_id=1,
    chunk_seconds=2
)


print("JARVIS INITIALIZED")
print()

print(
    "ACTIVE:",
    jarvis.is_active()
)

print(
    "LISTENING:",
    jarvis.is_listening()
)

print()

print(
    "STATUS:"
)

print(
    jarvis.get_status()
)