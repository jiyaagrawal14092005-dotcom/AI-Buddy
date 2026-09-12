class AudioManager:

    def __init__(self):

        self.recording = False
        self.playing = False
        self.audio_data = None

    def start_recording(self) -> dict:

        if self.recording:
            return {
                "success": False,
                "recording": True,
                "message": "Audio recording is already active."
            }

        self.recording = True
        self.audio_data = None

        return {
            "success": True,
            "recording": True,
            "message": "Audio recording started."
        }

    def stop_recording(self) -> dict:

        if not self.recording:
            return {
                "success": False,
                "recording": False,
                "message": "Audio recording is not active."
            }

        self.recording = False

        return {
            "success": True,
            "recording": False,
            "audio_data": self.audio_data,
            "message": "Audio recording stopped."
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

        self.playing = True

        return {
            "success": True,
            "playing": True,
            "message": "Audio playback started."
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
            )
        }

    def reset(self) -> None:

        self.recording = False
        self.playing = False
        self.audio_data = None