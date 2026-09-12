from pathlib import Path

from app.tools.base_tool import BaseTool


class FileTool(BaseTool):

    def __init__(self):

        super().__init__(
            name="file",
            description=(
                "Prepare basic file operations such as "
                "create, read, update, and delete."
            )
        )

    def _validate_path(
        self,
        file_path: str
    ) -> str:

        if not isinstance(
            file_path,
            str
        ):
            raise TypeError(
                "File path must be a string."
            )

        file_path = file_path.strip()

        if not file_path:
            raise ValueError(
                "File path cannot be empty."
            )

        return file_path

    def _validate_operation(
        self,
        operation: str
    ) -> str:

        if not isinstance(
            operation,
            str
        ):
            raise TypeError(
                "Operation must be a string."
            )

        operation = operation.strip().lower()

        allowed_operations = {
            "create",
            "read",
            "update",
            "delete"
        }

        if operation not in allowed_operations:
            raise ValueError(
                "Unsupported file operation. "
                "Use create, read, update, or delete."
            )

        return operation

    def prepare_operation(
        self,
        operation: str,
        file_path: str,
        content: str = ""
    ) -> dict:

        operation = self._validate_operation(
            operation
        )

        file_path = self._validate_path(
            file_path
        )

        if not isinstance(
            content,
            str
        ):
            raise TypeError(
                "File content must be a string."
            )

        return {
            "operation": operation,
            "file_path": str(
                Path(file_path)
            ),
            "content": content
        }

    def execute(
        self,
        parameters: dict | None = None
    ) -> dict:

        if parameters is None:
            parameters = {}

        if not isinstance(
            parameters,
            dict
        ):
            return {
                "success": False,
                "message": (
                    "File parameters must be a dictionary."
                )
            }

        operation = parameters.get(
            "operation",
            ""
        )

        file_path = parameters.get(
            "file_path",
            parameters.get(
                "path",
                ""
            )
        )

        content = parameters.get(
            "content",
            ""
        )

        try:

            operation_data = self.prepare_operation(
                operation,
                file_path,
                content
            )

        except (
            TypeError,
            ValueError
        ) as e:

            return {
                "success": False,
                "message": str(e)
            }

        return {
            "success": True,
            "status": "prepared",
            "file": operation_data,
            "message": (
                "File operation prepared successfully."
            )
        }

    def is_available(self) -> bool:
        return True