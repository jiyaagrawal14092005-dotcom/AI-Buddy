import json
import os


class MemoryStorage:

    def __init__(
        self,
        file_path: str = "memory.json"
    ):

        if not isinstance(file_path, str):
            raise TypeError(
                "File path must be text."
            )

        file_path = file_path.strip()

        if not file_path:
            raise ValueError(
                "File path cannot be empty."
            )

        self.file_path = file_path

    # ---------------------------------
    # SAVE MEMORY DATA
    # ---------------------------------

    def save(
        self,
        data: dict
    ) -> dict:

        if not isinstance(data, dict):
            return {
                "success": False,
                "message": "Memory data must be a dictionary."
            }

        try:

            directory = os.path.dirname(
                os.path.abspath(
                    self.file_path
                )
            )

            if directory:
                os.makedirs(
                    directory,
                    exist_ok=True
                )

            with open(
                self.file_path,
                "w",
                encoding="utf-8"
            ) as file:

                json.dump(
                    data,
                    file,
                    indent=4,
                    ensure_ascii=False
                )

            return {
                "success": True,
                "message": "Memory stored successfully."
            }

        except (
            OSError,
            TypeError,
            ValueError
        ) as error:

            return {
                "success": False,
                "message": str(error)
            }

    # ---------------------------------
    # LOAD MEMORY DATA
    # ---------------------------------

    def load(self) -> dict:

        if not os.path.exists(
            self.file_path
        ):
            return {}

        try:

            with open(
                self.file_path,
                "r",
                encoding="utf-8"
            ) as file:

                data = json.load(file)

            if not isinstance(data, dict):
                return {}

            return data

        except (
            OSError,
            json.JSONDecodeError,
            TypeError,
            ValueError
        ):
            return {}

    # ---------------------------------
    # CHECK FILE EXISTS
    # ---------------------------------

    def exists(self) -> bool:

        return os.path.isfile(
            self.file_path
        )

    # ---------------------------------
    # DELETE MEMORY STORAGE
    # ---------------------------------

    def delete(self) -> dict:

        if not os.path.exists(
            self.file_path
        ):
            return {
                "success": True,
                "message": (
                    "Memory storage was already empty."
                )
            }

        try:

            os.remove(
                self.file_path
            )

            return {
                "success": True,
                "message": "Memory storage deleted."
            }

        except OSError as error:

            return {
                "success": False,
                "message": str(error)
            }

    # ---------------------------------
    # GET FILE PATH
    # ---------------------------------

    def get_file_path(self) -> str:

        return self.file_path