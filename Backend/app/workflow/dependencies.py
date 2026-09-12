class DependencyManager:

    def __init__(self):
        self.dependencies = {}

    # ---------------------------------
    # VALIDATE STEP ID
    # ---------------------------------

    def _validate_step_id(
        self,
        step_id: int
    ) -> bool:

        return (
            isinstance(step_id, int)
            and not isinstance(step_id, bool)
            and step_id >= 0
        )

    # ---------------------------------
    # ADD DEPENDENCY
    # ---------------------------------

    def add_dependency(
        self,
        step_id: int,
        depends_on: int
    ) -> dict:

        if not self._validate_step_id(step_id):
            return {
                "success": False,
                "message": "Step ID must be a non-negative integer."
            }

        if not self._validate_step_id(depends_on):
            return {
                "success": False,
                "message": (
                    "Dependency step ID must be "
                    "a non-negative integer."
                )
            }

        if step_id == depends_on:
            return {
                "success": False,
                "message": "A step cannot depend on itself."
            }

        # Check whether adding this dependency
        # would create a circular dependency.
        current = depends_on
        visited = set()

        while current in self.dependencies:

            if current in visited:
                break

            visited.add(current)

            if self.dependencies[current] == step_id:
                return {
                    "success": False,
                    "message": (
                        "Dependency would create "
                        "a circular dependency."
                    )
                }

            current = self.dependencies[current]

        self.dependencies[step_id] = depends_on

        return {
            "success": True,
            "step_id": step_id,
            "depends_on": depends_on,
            "message": (
                f"Step {step_id} depends on "
                f"step {depends_on}."
            )
        }

    # ---------------------------------
    # GET DEPENDENCY
    # ---------------------------------

    def get_dependency(
        self,
        step_id: int
    ):

        if not self._validate_step_id(step_id):
            return None

        return self.dependencies.get(step_id)

    # ---------------------------------
    # CHECK WHETHER STEP CAN RUN
    # ---------------------------------

    def can_execute(
        self,
        step_id: int,
        completed_steps: list
    ) -> bool:

        if not self._validate_step_id(step_id):
            return False

        if not isinstance(completed_steps, list):
            return False

        dependency = self.get_dependency(step_id)

        # No dependency
        if dependency is None:
            return True

        # Dependency must be completed
        return dependency in completed_steps

    # ---------------------------------
    # REMOVE DEPENDENCY
    # ---------------------------------

    def remove_dependency(
        self,
        step_id: int
    ) -> dict:

        if not self._validate_step_id(step_id):
            return {
                "success": False,
                "message": "Invalid step ID."
            }

        if step_id not in self.dependencies:
            return {
                "success": False,
                "message": "Dependency not found."
            }

        del self.dependencies[step_id]

        return {
            "success": True,
            "step_id": step_id,
            "message": "Dependency removed successfully."
        }

    # ---------------------------------
    # GET ALL DEPENDENCIES
    # ---------------------------------

    def get_all(self) -> dict:

        return self.dependencies.copy()

    # ---------------------------------
    # CLEAR ALL DEPENDENCIES
    # ---------------------------------

    def clear(self) -> dict:

        self.dependencies.clear()

        return {
            "success": True,
            "message": "All dependencies cleared successfully."
        }