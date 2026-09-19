import asyncio

from app.agent.brain import AIBrain
from app.database.connection import SessionLocal
from app.voice.text_to_speech import TextToSpeech


async def main():
    db = SessionLocal()

    try:
        print("=" * 60)
        print("GEMINI/FALLBACK → TTS TEST")
        print("=" * 60)

        # -----------------------------------------
        # STEP 1: Create Brain
        # -----------------------------------------
        print("\n[1] Initializing AI Brain...")

        brain = AIBrain()

        print("✅ AI Brain initialized.")

        # -----------------------------------------
        # STEP 2: Ask Gemini/Fallback
        # -----------------------------------------
        print("\n[2] Asking AI Buddy:")
        print("What is Python?")

        result = brain.respond(
            "What is Python?",
            1,
            db
        )

        print("\nBrain result:")
        print(result)

        if not isinstance(result, dict):
            print("\n❌ Brain returned an invalid result.")
            return

        # -----------------------------------------
        # STEP 3: Extract actual answer
        # -----------------------------------------
        action_result = result.get("action_result")

        answer = ""

        if isinstance(action_result, dict):
            answer = action_result.get("answer", "")

        if not answer:
            answer = result.get("answer", "")

        if not answer:
            answer = result.get("message", "")

        if not isinstance(answer, str):
            answer = str(answer)

        answer = answer.strip()

        print("\n" + "=" * 60)
        print("GENERATED ANSWER")
        print("=" * 60)

        print(answer)

        if not answer:
            print("\n❌ No AI answer was generated.")
            return

        # -----------------------------------------
        # STEP 4: Initialize TTS
        # -----------------------------------------
        print("\n" + "=" * 60)
        print("[3] Starting Text-to-Speech")
        print("=" * 60)

        tts = TextToSpeech()

        if not tts.is_available():
            print("\n❌ TTS is not available.")
            print(tts.get_status())
            return

        print("✅ TTS is available.")

        # -----------------------------------------
        # STEP 5: Speak actual AI answer
        # -----------------------------------------
        print("\n[4] AI Buddy is speaking...")
        print("Please listen to the complete answer.")

        tts_result = await asyncio.to_thread(
            tts.speak,
            answer
        )

        print("\n" + "=" * 60)
        print("TTS RESULT")
        print("=" * 60)

        print(tts_result)

        # -----------------------------------------
        # FINAL VERIFICATION
        # -----------------------------------------
        print("\n" + "=" * 60)
        print("FINAL VERIFICATION")
        print("=" * 60)

        if tts_result.get("success"):
            print("✅ Gemini/Fallback generated an answer.")
            print("✅ TextToSpeech received the actual answer.")
            print("✅ AI Buddy spoke the generated answer.")
            print("\n🎉 GEMINI → TTS PIPELINE VERIFIED.")
        else:
            print("❌ TTS failed to speak the generated answer.")

    except Exception as error:
        print("\n❌ TEST ERROR:")
        print(repr(error))

    finally:
        db.close()
        print("\nTest finished.")


if __name__ == "__main__":
    asyncio.run(main())