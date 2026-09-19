import asyncio
import queue
import threading

from sqlalchemy.orm import Session

from app.voice.voice_manager import VoiceManager
from app.voice.voice_command import VoiceCommand
from app.agent.brain import AIBrain


class JarvisMode:

    STOP_COMMANDS = {
        "stop",
        "stop listening",
        "stop jarvis",
        "jarvis stop",
        "zarvis stop",
        "exit",
        "quit",
        "goodbye"
    }

    def __init__(
        self,
        wake_word: str = "Zarvis",
        user_id: int | None = None,
        chunk_seconds: int = 4
    ):

        if not isinstance(
            wake_word,
            str
        ):
            raise TypeError(
                "Wake word must be a string."
            )

        wake_word = wake_word.strip()

        if not wake_word:
            raise ValueError(
                "Wake word cannot be empty."
            )

        if (
            user_id is not None
            and (
                not isinstance(
                    user_id,
                    int
                )
                or user_id <= 0
            )
        ):
            raise ValueError(
                "User ID must be a positive integer."
            )

        if (
            not isinstance(
                chunk_seconds,
                int
            )
            or chunk_seconds <= 0
        ):
            raise ValueError(
                "Chunk duration must be a positive integer."
            )

        self.wake_word = wake_word
        self.user_id = user_id
        self.chunk_seconds = chunk_seconds

        self.voice_manager = VoiceManager(
            wake_word
        )

        self.ai_brain = AIBrain()

        self.active = False
        self.listening = False
        self.speaking = False

        # Thread-safe stop signal.
        self._stop_event = threading.Event()

        self._loop_task = None

        # Recognized microphone text is transferred
        # from CommandListener thread to the async loop.
        self._command_queue = queue.Queue()

        self.history = []

    # ---------------------------------------------------------
    # USER ID
    # ---------------------------------------------------------

    def set_user_id(
        self,
        user_id: int
    ) -> None:

        if (
            not isinstance(
                user_id,
                int
            )
            or user_id <= 0
        ):
            raise ValueError(
                "User ID must be a positive integer."
            )

        self.user_id = user_id

    # ---------------------------------------------------------
    # COMMAND NORMALIZATION
    # ---------------------------------------------------------

    def _normalize_command(
        self,
        text: str
    ) -> str:

        if not isinstance(
            text,
            str
        ):
            return ""

        return " ".join(
            text.lower().strip().split()
        )

    # ---------------------------------------------------------
    # STOP COMMAND CHECK
    # ---------------------------------------------------------

    def _is_stop_command(
        self,
        text: str
    ) -> bool:

        normalized_text = (
            self._normalize_command(
                text
            )
        )

        if not normalized_text:
            return False

        # Direct stop commands.
        if normalized_text in self.STOP_COMMANDS:
            return True

        # Accept wake-word + stop.
        #
        # Examples:
        # "Zarvis stop"
        # "Jarvis stop"
        # "zarvis stop listening"
        # "jarvis stop jarvis"
        wake_word = self._normalize_command(
            self.wake_word
        )

        if wake_word:

            wake_word_prefix = (
                wake_word + " "
            )

            if normalized_text.startswith(
                wake_word_prefix
            ):

                command_after_wake_word = (
                    normalized_text[
                        len(wake_word_prefix):
                    ].strip()
                )

                if (
                    command_after_wake_word
                    in self.STOP_COMMANDS
                ):
                    return True

        return False

    # ---------------------------------------------------------
    # STOP CURRENT SPEECH
    # ---------------------------------------------------------

    def _stop_speech(self) -> None:

        try:

            self.voice_manager.text_to_speech.stop()

        except Exception as error:

            print(
                "JARVIS TTS STOP ERROR:",
                repr(error)
            )

        self.speaking = False

    # ---------------------------------------------------------
    # CLEAR COMMAND QUEUE
    # ---------------------------------------------------------

    def _clear_command_queue(self) -> None:

        while True:

            try:

                self._command_queue.get_nowait()

            except queue.Empty:

                break

            except Exception:

                break

    # ---------------------------------------------------------
    # REQUEST VOICE STOP
    # ---------------------------------------------------------

    def _request_voice_stop(
        self
    ) -> None:

        print(
            "Jarvis stop command detected."
        )

        # Stop accepting new commands immediately.
        self.active = False
        self.listening = False

        # Signal every running component.
        self._stop_event.set()

        # IMPORTANT:
        # Interrupt currently running TTS immediately.
        self._stop_speech()

        # Stop microphone capture.
        try:

            self.voice_manager.command_listener.stop_microphone()

        except Exception as error:

            print(
                "JARVIS MICROPHONE STOP ERROR:",
                repr(error)
            )

        # Remove commands that may have been
        # recognized before the stop command.
        self._clear_command_queue()

        # Wake the async command loop.
        try:

            self._command_queue.put_nowait(
                None
            )

        except Exception:

            pass

    # ---------------------------------------------------------
    # MICROPHONE CALLBACK
    # ---------------------------------------------------------

    def _on_microphone_text(
        self,
        text: str
    ) -> None:

        if not isinstance(
            text,
            str
        ):
            return

        text = text.strip()

        if not text:
            return

        print(
            f"Jarvis microphone heard: {text}"
        )

        # -----------------------------------------------------
        # STOP HAS HIGHEST PRIORITY
        # -----------------------------------------------------

        if self._is_stop_command(
            text
        ):

            self._request_voice_stop()

            return

        # -----------------------------------------------------
        # IGNORE ALL NON-STOP SPEECH AFTER STOP
        # -----------------------------------------------------

        if not self.active:
            return

        # -----------------------------------------------------
        # IMPORTANT:
        # While Jarvis is speaking, ignore ordinary recognized
        # speech so Jarvis does not accidentally process its
        # own voice as a new command.
        #
        # STOP COMMAND WAS CHECKED ABOVE, so Stop still works.
        # -----------------------------------------------------

        if self.speaking:
            return

        # -----------------------------------------------------
        # SEND COMMAND TO ASYNC LOOP
        # -----------------------------------------------------

        try:

            self._command_queue.put_nowait(
                text
            )

        except Exception as error:

            print(
                "JARVIS COMMAND QUEUE ERROR:",
                repr(error)
            )

    # ---------------------------------------------------------
    # GET NEXT MICROPHONE COMMAND
    # ---------------------------------------------------------

    async def _get_next_command(
        self
    ):

        while (
            self.active
            and not self._stop_event.is_set()
        ):

            try:

                command = await asyncio.to_thread(
                    self._command_queue.get
                )

                if command is None:

                    return None

                if not isinstance(
                    command,
                    str
                ):

                    continue

                command = command.strip()

                if not command:

                    continue

                return command

            except asyncio.CancelledError:

                raise

            except Exception as error:

                print(
                    "JARVIS COMMAND QUEUE READ ERROR:",
                    repr(error)
                )

                await asyncio.sleep(
                    0.1
                )

        return None

    # ---------------------------------------------------------
    # CREATE VOICE COMMAND
    # ---------------------------------------------------------

    def _create_voice_command(
        self,
        command_text: str
    ) -> dict:

        command = VoiceCommand()

        try:

            command.set_text(
                command_text
            )

            command.set_command(
                command_text
            )

            return command.to_dict()

        except (
            TypeError,
            ValueError
        ) as error:

            print(
                "JARVIS VOICE COMMAND ERROR:",
                repr(error)
            )

            return {}

    # ---------------------------------------------------------
    # PROCESS ONE JARVIS INPUT
    # ---------------------------------------------------------

    async def _process_command(
        self,
        text: str,
        db: Session
    ) -> dict:

        if self.user_id is None:

            return {
                "success": False,
                "executed": False,
                "message": (
                    "User ID is required for Jarvis mode."
                )
            }

        if db is None:

            return {
                "success": False,
                "executed": False,
                "message": (
                    "Database session is required."
                )
            }

        # -------------------------------------------------
        # DIRECT STOP CHECK
        # -------------------------------------------------

        if self._is_stop_command(
            text
        ):

            self._request_voice_stop()

            return {
                "success": True,
                "executed": False,
                "stopped": True,
                "wake_word_detected": False,
                "text": text,
                "command": None,
                "brain_input": "",
                "response": "",
                "voice_response": None,
                "message": (
                    "Jarvis mode stopped by voice command."
                )
            }

        # -------------------------------------------------
        # STOP EVENT CHECK
        # -------------------------------------------------

        if self._stop_event.is_set():

            return {
                "success": True,
                "executed": False,
                "stopped": True,
                "text": text,
                "command": None,
                "brain_input": "",
                "response": "",
                "voice_response": None,
                "message": (
                    "Jarvis was stopped before "
                    "processing the command."
                )
            }

        # -------------------------------------------------
        # LOCAL WAKE-WORD GATE
        # -------------------------------------------------

        voice_result = (
            self.voice_manager.process_text(
                text
            )
        )

        if not voice_result.get(
            "success",
            False
        ):

            return {
                **voice_result,
                "text": text,
                "executed": False
            }

        wake_word_detected = (
            voice_result.get(
                "wake_word_detected",
                False
            )
        )

        command_data = (
            voice_result.get(
                "command"
            )
        )

        # -------------------------------------------------
        # PRIVACY BLOCK
        # -------------------------------------------------

        if not wake_word_detected:

            return {
                "success": True,
                "executed": False,
                "wake_word_detected": False,
                "text": text,
                "command": None,
                "brain_input": "",
                "message": (
                    "Wake word not detected. "
                    "Command ignored before AI Brain."
                )
            }

        # -------------------------------------------------
        # COMMAND VALIDATION
        # -------------------------------------------------

        if not isinstance(
            command_data,
            dict
        ):

            return {
                "success": True,
                "executed": False,
                "wake_word_detected": True,
                "text": text,
                "command": None,
                "brain_input": "",
                "message": (
                    "Wake word detected but "
                    "no command was provided."
                )
            }

        command_text = (
            command_data.get(
                "text",
                ""
            ).strip()
        )

        if not command_text:

            return {
                "success": True,
                "executed": False,
                "wake_word_detected": True,
                "text": text,
                "command": command_data,
                "brain_input": "",
                "message": (
                    "Wake word detected but "
                    "no command was provided."
                )
            }

        # -------------------------------------------------
        # STOP CHECK BEFORE AI BRAIN
        # -------------------------------------------------

        if self._stop_event.is_set():

            return {
                "success": True,
                "executed": False,
                "stopped": True,
                "message": (
                    "Jarvis stopped before command execution."
                )
            }

        # -------------------------------------------------
        # AI BRAIN
        # -------------------------------------------------

        brain_result = self.ai_brain.respond(
            command_text,
            self.user_id,
            db
        )

        if not isinstance(
            brain_result,
            dict
        ):

            brain_result = {
                "success": False,
                "message": (
                    "AI Brain returned an invalid response."
                )
            }

        # -------------------------------------------------
        # EXTRACT ACTUAL AI ANSWER
        # -------------------------------------------------

        response_text = ""

        action_result = brain_result.get(
            "action_result"
        )

        if isinstance(
            action_result,
            dict
        ):

            answer = action_result.get(
                "answer"
            )

            if (
                isinstance(
                    answer,
                    str
                )
                and answer.strip()
            ):

                response_text = (
                    answer.strip()
                )

        # -------------------------------------------------
        # FALLBACK RESPONSE EXTRACTION
        # -------------------------------------------------

        if not response_text:

            direct_answer = brain_result.get(
                "answer"
            )

            if (
                isinstance(
                    direct_answer,
                    str
                )
                and direct_answer.strip()
            ):

                response_text = (
                    direct_answer.strip()
                )

        # -------------------------------------------------
        # FINAL MESSAGE FALLBACK
        # -------------------------------------------------

        if not response_text:

            brain_message = brain_result.get(
                "message",
                ""
            )

            if (
                isinstance(
                    brain_message,
                    str
                )
                and brain_message.strip()
            ):

                response_text = (
                    brain_message.strip()
                )

        # -------------------------------------------------
        # TEXT → SPEECH
        # -------------------------------------------------

        voice_response = None

        if (
            brain_result.get(
                "success",
                False
            )
            and isinstance(
                response_text,
                str
            )
            and response_text.strip()
            and not self._stop_event.is_set()
            and self.active
        ):

            self.speaking = True

            try:

                voice_response = (
                    self.voice_manager.speak(
                        response_text
                    )
                )

            finally:

                self.speaking = False

        # -------------------------------------------------
        # HISTORY
        # -------------------------------------------------

        history_item = {
            "text": text,
            "wake_word_detected": True,
            "command": command_data,
            "brain_input": command_text,
            "brain": brain_result,
            "response": response_text,
            "voice_response": voice_response
        }

        self.history.append(
            history_item
        )

        # -------------------------------------------------
        # RESPONSE
        # -------------------------------------------------

        return {
            "success": brain_result.get(
                "success",
                False
            ),
            "executed": True,
            "wake_word_detected": True,
            "text": text,
            "command": command_data,
            "brain_input": command_text,
            "brain": brain_result,
            "response": response_text,
            "voice_response": voice_response,
            "message": (
                "Jarvis command executed successfully."
                if brain_result.get(
                    "success",
                    False
                )
                else brain_result.get(
                    "message",
                    "Jarvis command failed."
                )
            )
        }

    # ---------------------------------------------------------
    # MAIN LOOP
    # ---------------------------------------------------------

    async def _run_loop(
        self,
        db: Session
    ) -> None:

        while (
            self.active
            and not self._stop_event.is_set()
        ):

            try:

                # Wait for CommandListener to recognize
                # the next piece of speech.
                text = await self._get_next_command()

                if (
                    text is None
                    or not self.active
                    or self._stop_event.is_set()
                ):

                    break

                # -------------------------------------------------
                # STOP CHECK
                # -------------------------------------------------

                if self._is_stop_command(
                    text
                ):

                    self._request_voice_stop()

                    break

                self.listening = True

                result = await self._process_command(
                    text,
                    db
                )

                self.listening = False

                if (
                    not self.active
                    or self._stop_event.is_set()
                ):

                    break

                if (
                    not result.get(
                        "success",
                        False
                    )
                    and result.get(
                        "message",
                        ""
                    )
                ):

                    print(
                        f"Jarvis: {result['message']}"
                    )

                await asyncio.sleep(0)

            except asyncio.CancelledError:

                break

            except Exception as error:

                self.listening = False

                print(
                    "JARVIS MAIN LOOP ERROR:",
                    repr(error)
                )

                await asyncio.sleep(
                    0.1
                )

    # ---------------------------------------------------------
    # START JARVIS
    # ---------------------------------------------------------

    async def start(
        self,
        user_id: int,
        db: Session
    ) -> dict:

        if self.active:

            return {
                "success": False,
                "active": True,
                "message": (
                    "Jarvis mode is already active."
                )
            }

        if (
            not isinstance(
                user_id,
                int
            )
            or user_id <= 0
        ):

            return {
                "success": False,
                "active": False,
                "message": (
                    "User ID must be a valid positive integer."
                )
            }

        if db is None:

            return {
                "success": False,
                "active": False,
                "message": (
                    "Database session is required."
                )
            }

        self.user_id = user_id

        self.active = True
        self.listening = False
        self.speaking = False

        self._stop_event.clear()

        # Clear old queued commands.
        self._clear_command_queue()

        # -------------------------------------------------
        # CONNECT COMMAND LISTENER CALLBACK
        # -------------------------------------------------

        callback_result = (
            self.voice_manager
            .command_listener
            .set_command_callback(
                self._on_microphone_text
            )
        )

        if not callback_result.get(
            "success",
            False
        ):

            self.active = False

            return {
                "success": False,
                "active": False,
                "listening": False,
                "speaking": False,
                "wake_word": self.wake_word,
                "message": (
                    "Unable to configure Jarvis microphone callback."
                ),
                "callback": callback_result
            }

        # -------------------------------------------------
        # START SINGLE MICROPHONE LISTENER
        # -------------------------------------------------

        listener_result = (
            self.voice_manager
            .command_listener
            .start_listening()
        )

        if not listener_result.get(
            "success",
            False
        ):

            self.active = False

            self.voice_manager.command_listener.set_command_callback(
                None
            )

            return {
                "success": False,
                "active": False,
                "listening": False,
                "speaking": False,
                "wake_word": self.wake_word,
                "message": (
                    "Unable to start Jarvis microphone listener."
                ),
                "listener": listener_result
            }

        # -------------------------------------------------
        # START ASYNC JARVIS PROCESSING LOOP
        # -------------------------------------------------

        self._loop_task = asyncio.create_task(
            self._run_loop(
                db
            )
        )

        return {
            "success": True,
            "active": True,
            "listening": True,
            "speaking": False,
            "wake_word": self.wake_word,
            "message": (
                "Jarvis mode started. "
                "AI Buddy is listening for the wake word."
            )
        }

    # ---------------------------------------------------------
    # STOP JARVIS
    # ---------------------------------------------------------

    async def stop(self) -> dict:

        if not self.active:

            self._stop_event.set()

            self._stop_speech()

            try:

                self.voice_manager.command_listener.stop_microphone()

            except Exception:
                pass

            try:

                self.voice_manager.command_listener.set_command_callback(
                    None
                )

            except Exception:
                pass

            self._clear_command_queue()

            return {
                "success": False,
                "active": False,
                "listening": False,
                "speaking": False,
                "message": (
                    "Jarvis mode is not active."
                )
            }

        self.active = False

        self.listening = False

        self._stop_event.set()

        # -------------------------------------------------
        # STOP CURRENT SPEECH
        # -------------------------------------------------

        self._stop_speech()

        # -------------------------------------------------
        # STOP MICROPHONE
        # -------------------------------------------------

        try:

            self.voice_manager.command_listener.stop_microphone()

        except Exception as error:

            print(
                "JARVIS MICROPHONE STOP ERROR:",
                repr(error)
            )

        # Disable callback after microphone shutdown.
        try:

            self.voice_manager.command_listener.set_command_callback(
                None
            )

        except Exception:
            pass

        # Remove pending commands.
        self._clear_command_queue()

        # Wake waiting async loop.
        try:

            self._command_queue.put_nowait(
                None
            )

        except Exception:
            pass

        # -------------------------------------------------
        # STOP ASYNC LOOP
        # -------------------------------------------------

        if self._loop_task is not None:

            if not self._loop_task.done():

                try:

                    await asyncio.wait_for(
                        asyncio.shield(
                            self._loop_task
                        ),
                        timeout=2
                    )

                except asyncio.TimeoutError:

                    if not self._loop_task.done():

                        self._loop_task.cancel()

                    try:

                        await self._loop_task

                    except asyncio.CancelledError:

                        pass

                except asyncio.CancelledError:

                    pass

                except Exception:

                    pass

        self._loop_task = None

        self.listening = False
        self.speaking = False

        return {
            "success": True,
            "active": False,
            "listening": False,
            "speaking": False,
            "message": (
                "Jarvis mode stopped."
            )
        }

    # ---------------------------------------------------------
    # TOGGLE
    # ---------------------------------------------------------

    async def toggle(
        self,
        user_id: int,
        db: Session
    ) -> dict:

        if self.active:

            return await self.stop()

        return await self.start(
            user_id,
            db
        )

    # ---------------------------------------------------------
    # HISTORY
    # ---------------------------------------------------------

    def get_history(self) -> list:

        return list(
            self.history
        )

    def clear_history(self) -> None:

        self.history.clear()

    # ---------------------------------------------------------
    # STATUS
    # ---------------------------------------------------------

    def is_active(self) -> bool:

        return self.active

    def is_listening(self) -> bool:

        return self.listening

    def get_status(self) -> dict:

        command_listener_status = (
            self.voice_manager
            .command_listener
            .get_status()
        )

        return {
            "name": "jarvis_mode",
            "active": self.active,
            "listening": self.listening,
            "speaking": self.speaking,
            "user_id": self.user_id,
            "wake_word": self.wake_word,
            "chunk_seconds": self.chunk_seconds,
            "command_listener": command_listener_status,
            "history_count": len(
                self.history
            )
        }