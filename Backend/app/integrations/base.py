from abc import ABC, abstractmethod


class BaseIntegration(ABC):

    def __init__(
        self,
        name: str,
        description: str
    ):

        if not isinstance(
            name,
            str
        ) or not name.strip():

            raise ValueError(
                "Integration name must be a non-empty string."
            )

        if not isinstance(
            description,
            str
        ) or not description.strip():

            raise ValueError(
                "Integration description must be a non-empty string."
            )

        self.name = name.strip()
        self.description = description.strip()

    def get_info(self) -> dict:
        return {
            "name": self.name,
            "description": self.description,
            "available": self.is_available()
        }

    def is_available(self) -> bool:
        return False

    @abstractmethod
    def connect(self) -> dict:
        pass

    @abstractmethod
    def disconnect(self) -> dict:
        pass

    @abstractmethod
    def execute(
        self,
        action: str,
        parameters: dict | None = None
    ) -> dict:
        pass