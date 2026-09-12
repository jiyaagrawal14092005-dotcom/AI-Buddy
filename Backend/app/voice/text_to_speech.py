import os
import sys
import threading


# ---------------------------------------------------------
# Windows / pywin32 DLL configuration
# ---------------------------------------------------------

if sys.platform == "win32":
    try:
        venv_dir = os.path.dirname(
            os.path.dirname(os.path.abspath(sys.executable))
        )

        pywin32_system32 = os.path.join(
            venv_dir,
            "Lib",
            "site-packages",
            "pywin32_system32"
        )

        if os.path.isdir(pywin32_system32):
            if hasattr(os, "add_dll_directory"):
                os.add_dll_directory(pywin32_system32)

            os.environ["PATH"] = (
                pywin32_system32
                + os.pathsep
                + os.environ.get("PATH", "")
            )

    except Exception as error:
        print("PYWIN32 DLL PATH ERROR:", repr(error))


import pyttsx3


class TextToSpeech:

    def __init__(self):
        self.name = "text_to_speech"
        self.available = False
        self.engine = None
        self.error = None

        # Prevent multiple TTS operations from running together.
        self._lock = threading.Lock()

    # ---------------------------------------------------------
    # Engine availability
    # ---------------------------------------------------------

    def is_available(self) -> bool:

        try:

            if sys.platform == "win32":
                import pywintypes
                import pythoncom

                # Initialize COM for the current thread.
                pythoncom.CoInitialize()

                try:
                    engine = pyttsx3.init(
                        driverName="sapi5"
                    )

                    self.available = True
                    self.error = None

                    try:
                        engine.stop()
                    except Exception:
                        pass

                    del engine

                    return True

                finally:
                    pythoncom.CoUninitialize()

            engine = pyttsx3.init()

            self.available = True
            self.error = None

            try:
                engine.stop()
            except Exception:
                pass

            del engine

            return True

        except Exception as error:

            self.available = False
            self.error = str(error)

            print(
                "TTS AVAILABILITY ERROR:",
                repr(error)
            )

            return False

    # ---------------------------------------------------------
    # Speech synthesis
    # ---------------------------------------------------------

    def synthesize(
        self,
        text: str
    ) -> dict:

        if not isinstance(text, str):

            return {
                "success": False,
                "audio": None,
                "text": text,
                "status": "failed",
                "message": "Text must be a string."
            }

        text = text.strip()

        if not text:

            return {
                "success": False,
                "audio": None,
                "text": text,
                "status": "failed",
                "message": "Text cannot be empty."
            }

        with self._lock:

            engine = None
            com_initialized = False

            try:

                # -------------------------------------------------
                # Windows SAPI5
                # -------------------------------------------------

                if sys.platform == "win32":

                    import pywintypes
                    import pythoncom

                    # IMPORTANT:
                    # FastAPI sync endpoints can execute inside
                    # different worker threads. COM must therefore
                    # be initialized in the current thread.
                    pythoncom.CoInitialize()
                    com_initialized = True

                    engine = pyttsx3.init(
                        driverName="sapi5"
                    )

                # -------------------------------------------------
                # Other platforms
                # -------------------------------------------------

                else:

                    engine = pyttsx3.init()

                # -------------------------------------------------
                # Configure voice
                # -------------------------------------------------

                try:

                    voices = engine.getProperty("voices")

                    if voices:

                        engine.setProperty(
                            "voice",
                            voices[0].id
                        )

                except Exception:
                    pass

                # Normal speech rate.
                try:

                    engine.setProperty(
                        "rate",
                        175
                    )

                except Exception:
                    pass

                # Normal volume.
                try:

                    engine.setProperty(
                        "volume",
                        1.0
                    )

                except Exception:
                    pass

                self.engine = engine
                self.available = True
                self.error = None

                # -------------------------------------------------
                # Speak
                # -------------------------------------------------

                engine.say(text)

                engine.runAndWait()

                # Stop engine after speaking.
                try:
                    engine.stop()
                except Exception:
                    pass

                return {
                    "success": True,
                    "audio": None,
                    "text": text,
                    "status": "spoken",
                    "message": "Text spoken successfully."
                }

            except Exception as error:

                self.available = False
                self.error = str(error)

                print(
                    "TTS SYNTHESIS ERROR:",
                    repr(error)
                )

                return {
                    "success": False,
                    "audio": None,
                    "text": text,
                    "status": "failed",
                    "message": "Could not speak the text.",
                    "error": self.error
                }

            finally:

                # -------------------------------------------------
                # Release engine
                # -------------------------------------------------

                if engine is not None:

                    try:
                        engine.stop()
                    except Exception:
                        pass

                    try:
                        del engine
                    except Exception:
                        pass

                self.engine = None

                # -------------------------------------------------
                # Release COM
                # -------------------------------------------------

                if com_initialized:

                    try:
                        import pythoncom
                        pythoncom.CoUninitialize()
                    except Exception:
                        pass

    # ---------------------------------------------------------
    # Alias
    # ---------------------------------------------------------

    def speak(
        self,
        text: str
    ) -> dict:

        return self.synthesize(text)

    # ---------------------------------------------------------
    # Status
    # ---------------------------------------------------------

    def get_status(self) -> dict:

        available = self.is_available()

        return {
            "name": self.name,
            "available": available,
            "error": self.error
        }