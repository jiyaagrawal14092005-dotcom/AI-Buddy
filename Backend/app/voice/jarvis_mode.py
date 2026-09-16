import asyncio
import io
import wave

import numpy as np
import sounddevice as sd
from sqlalchemy.orm import Session

from app.voice.voice_manager import VoiceManager
from app.agent.brain import AIBrain


class JarvisMode:

    def __init__(
        self,
        wake_word: str = "ai buddy",
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

        if not isinstance(
            chunk_seconds,
            int
        ) or chunk_seconds <= 0:

            raise ValueError(
                "Chunk duration must be a positive integer."
            )

        self.wake_word = wake_word
        self.user_id = user_id
        self.chunk_seconds = chunk_seconds

        self.sample_rate = 16000
        self.channels = 1
        self.dtype = "int16"

        self.voice_manager = VoiceManager(
            wake_word
        )

        self.ai_brain = AIBrain()

        self.active = False
        self.listening = False

        self._stop_event = asyncio.Event()
        self._loop_task = None

        self.history = []

    def set_user_id(
        self,
        user_id: int
    ) -> None:

        if not isinstance(
            user_id,
            int
        ) or user_id <= 0:

            raise ValueError(
                "User ID must be a positive integer."
            )

        self.user_id = user_id

    def _record_chunk(self) -> bytes:

        frames = []

        def callback(
            indata,
            frames_count,
            time,
            status
        ):

            if status:

                print(
                    f"Jarvis audio status: {status}"
                )

            frames.append(
                indata.copy()
            )

        recording = sd.rec(
            int(
                self.sample_rate
                * self.chunk_seconds
            ),
            samplerate=self.sample_rate,
            channels=self.channels,
            dtype=self.dtype
        )

        sd.wait()

        if recording is None:

            return b""

        frames.append(
            np.asarray(
                recording
            )
        )

        audio_array = np.concatenate(
            frames,
            axis=0
        )

        audio_bytes = (
            audio_array
            .astype(
                np.int16
            )
            .tobytes()
        )

        wav_buffer = io.BytesIO()

        with wave.open(
            wav_buffer,
            "wb"
        ) as wav_file:

            wav_file.setnchannels(
                self.channels
            )

            wav_file.setsampwidth(
                2
            )

            wav_file.setframerate(
                self.sample_rate
            )

            wav_file.writeframes(
                audio_bytes
            )

        return wav_buffer.getvalue()

    async def _listen_once(
        self,
        db: Session
    ) -> dict:

        if self.user_id is None:

            return {
                "success": False,
                "message": (
                    "User ID is required for Jarvis mode."
                )
            }

        self.listening = True

        try:

            audio_data = await asyncio.to_thread(
                self._record_chunk
            )

            if not audio_data:

                return {
                    "success": False,
                    "text": "",
                    "message": (
                        "No audio data was recorded."
                    )
                }

            speech_result = (
                self.voice_manager.speech_to_text.transcribe(
                    audio_data
                )
            )

            if not speech_result.get(
                "success",
                False
            ):

                return {
                    "success": False,
                    "text": "",
                    "message": (
                        speech_result.get(
                            "message",
                            "Speech could not be recognized."
                        )
                    )
                }

            text = speech_result.get(
                "text",
                ""
            ).strip()

            if not text:

                return {
                    "success": False,
                    "text": "",
                    "message": (
                        "No speech was detected."
                    )
                }

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
                    "text": text
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

            if not wake_word_detected:

                return {
                    "success": True,
                    "executed": False,
                    "wake_word_detected": False,
                    "text": text,
                    "command": None,
                    "message": (
                        "Wake word not detected. "
                        "Command ignored."
                    )
                }

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
                    "message": (
                        "Wake word detected but "
                        "no command was provided."
                    )
                }

            brain_result = await self.ai_brain.respond(
                command_text,
                self.user_id,
                db
            )

            response_text = brain_result.get(
                "message",
                ""
            )

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
            ):

                voice_response = (
                    self.voice_manager.speak(
                        response_text
                    )
                )

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

        except Exception as error:

            return {
                "success": False,
                "executed": False,
                "message": (
                    f"Jarvis listening error: {error}"
                )
            }

        finally:

            self.listening = False

    async def _run_loop(
        self,
        db: Session
    ) -> None:

        while self.active:

            if self._stop_event.is_set():

                break

            result = await self._listen_once(
                db
            )

            if not self.active:

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

        if not isinstance(
            user_id,
            int
        ) or user_id <= 0:

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

        self._stop_event = asyncio.Event()

        self._loop_task = asyncio.create_task(
            self._run_loop(
                db
            )
        )

        return {
            "success": True,
            "active": True,
            "listening": False,
            "wake_word": self.wake_word,
            "message": (
                "Jarvis mode started. "
                "AI Buddy is listening for the wake word."
            )
        }

    async def stop(self) -> dict:

        if not self.active:

            return {
                "success": False,
                "active": False,
                "message": (
                    "Jarvis mode is not active."
                )
            }

        self.active = False

        self._stop_event.set()

        if self._loop_task is not None:

            try:

                await asyncio.wait_for(
                    self._loop_task,
                    timeout=6
                )

            except asyncio.TimeoutError:

                self._loop_task.cancel()

                try:

                    await self._loop_task

                except asyncio.CancelledError:

                    pass

            except Exception:

                pass

        self._loop_task = None
        self.listening = False

        return {
            "success": True,
            "active": False,
            "listening": False,
            "message": (
                "Jarvis mode stopped."
            )
        }

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

    def get_history(self) -> list:

        return list(
            self.history
        )

    def clear_history(self) -> None:

        self.history.clear()

    def is_active(self) -> bool:

        return self.active

    def is_listening(self) -> bool:

        return self.listening

    def get_status(self) -> dict:

        return {
            "name": "jarvis_mode",
            "active": self.active,
            "listening": self.listening,
            "user_id": self.user_id,
            "wake_word": self.wake_word,
            "chunk_seconds": self.chunk_seconds,
            "sample_rate": self.sample_rate,
            "channels": self.channels,
            "history_count": len(
                self.history
            )
        }