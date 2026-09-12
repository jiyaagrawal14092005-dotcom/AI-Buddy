import io
import wave

import sounddevice as sd


class AudioManager:

    def __init__(self):

        self.recording = False
        self.playing = False
        self.audio_data = None

        self.sample_rate = 16000
        self.channels = 1
        self.dtype = "int16"

        self._recorded_frames = []

    def start_recording(self) -> dict:

        if self.recording:
            return {
                "success": False,
                "recording": True,
                "message": "Audio recording is already active."
            }

        try:

            self._recorded_frames = []

            def callback(
                indata,
                frames,
                time,
                status
            ):

                if status:
                    print(
                        f"Audio recording status: {status}"
                    )

                self._recorded_frames.append(
                    indata.copy()
                )

            self._stream = sd.InputStream(
                samplerate=self.sample_rate,
                channels=self.channels,
                dtype=self.dtype,
                callback=callback
            )

            self._stream.start()

            self.recording = True
            self.audio_data = None

            return {
                "success": True,
                "recording": True,
                "message": "Audio recording started."
            }

        except Exception as error:

            self.recording = False
            self._recorded_frames = []

            return {
                "success": False,
                "recording": False,
                "message": (
                    f"Unable to start audio recording: {error}"
                )
            }

    def stop_recording(self) -> dict:

        if not self.recording:
            return {
                "success": False,
                "recording": False,
                "message": "Audio recording is not active."
            }

        try:

            self._stream.stop()
            self._stream.close()

            self.recording = False

            if not self._recorded_frames:

                self.audio_data = None

                return {
                    "success": False,
                    "recording": False,
                    "audio_data": None,
                    "message": "No audio was recorded."
                }

            audio_frames = b"".join(
                frame.tobytes()
                for frame in self._recorded_frames
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
                    audio_frames
                )

            self.audio_data = wav_buffer.getvalue()

            self._recorded_frames = []

            return {
                "success": True,
                "recording": False,
                "audio_data": self.audio_data,
                "message": "Audio recording stopped successfully."
            }

        except Exception as error:

            self.recording = False
            self._recorded_frames = []

            return {
                "success": False,
                "recording": False,
                "audio_data": None,
                "message": (
                    f"Unable to stop audio recording: {error}"
                )
            }

    def set_audio_data(
        self,
        audio_data
    ) -> dict:

        if audio_data is None:
            return {
                "success": False,
                "message": "Audio data cannot be None."
            }

        self.audio_data = audio_data

        return {
            "success": True,
            "message": "Audio data stored successfully."
        }

    def get_audio_data(self):

        return self.audio_data

    def clear_audio_data(self) -> None:

        self.audio_data = None

    def start_playback(self) -> dict:

        if self.playing:
            return {
                "success": False,
                "playing": True,
                "message": "Audio playback is already active."
            }

        if self.audio_data is None:
            return {
                "success": False,
                "playing": False,
                "message": "No audio data is available for playback."
            }

        try:

            self.playing = True

            return {
                "success": True,
                "playing": True,
                "message": "Audio playback started."
            }

        except Exception as error:

            self.playing = False

            return {
                "success": False,
                "playing": False,
                "message": (
                    f"Unable to start audio playback: {error}"
                )
            }

    def stop_playback(self) -> dict:

        if not self.playing:
            return {
                "success": False,
                "playing": False,
                "message": "Audio playback is not active."
            }

        self.playing = False

        return {
            "success": True,
            "playing": False,
            "message": "Audio playback stopped."
        }

    def is_recording(self) -> bool:

        return self.recording

    def is_playing(self) -> bool:

        return self.playing

    def get_status(self) -> dict:

        return {
            "recording": self.recording,
            "playing": self.playing,
            "has_audio_data": (
                self.audio_data is not None
            ),
            "sample_rate": self.sample_rate,
            "channels": self.channels
        }

    def reset(self) -> None:

        if self.recording:

            try:
                self._stream.stop()
                self._stream.close()
            except Exception:
                pass

        self.recording = False
        self.playing = False
        self.audio_data = None
        self._recorded_frames = []