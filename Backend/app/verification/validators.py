class Validator:

    def validate_required(
        self,
        data: dict,
        required_fields: list
    ) -> dict:

        # Validate data type
        if not isinstance(data, dict):
            return {
                "success": False,
                "valid": False,
                "message": "Data must be a dictionary."
            }

        # Validate required_fields
        if not isinstance(required_fields, list):
            return {
                "success": False,
                "valid": False,
                "message": "Required fields must be a list."
            }

        missing_fields = []

        for field in required_fields:

            if not isinstance(field, str):
                continue

            if field not in data:
                missing_fields.append(field)

            elif data[field] is None:
                missing_fields.append(field)

            elif isinstance(data[field], str) and not data[field].strip():
                missing_fields.append(field)

        if missing_fields:
            return {
                "success": True,
                "valid": False,
                "missing_fields": missing_fields,
                "message": "Required fields are missing."
            }

        return {
            "success": True,
            "valid": True,
            "missing_fields": [],
            "message": "All required fields are present."
        }

    def validate_result(
        self,
        result: dict
    ) -> dict:

        # Validate result type
        if not isinstance(result, dict):
            return {
                "success": False,
                "valid": False,
                "message": "Result must be a dictionary."
            }

        # Check success field
        if "success" not in result:
            return {
                "success": True,
                "valid": False,
                "message": "Result status is missing."
            }

        # success must be boolean
        if not isinstance(result["success"], bool):
            return {
                "success": True,
                "valid": False,
                "message": "Result success status must be boolean."
            }

        if result["success"] is True:
            return {
                "success": True,
                "valid": True,
                "message": "Result is valid."
            }

        return {
            "success": True,
            "valid": False,
            "message": "Result indicates failure."
        }

    def validate_intent(
        self,
        intent: dict
    ) -> dict:

        # Validate intent type
        if not isinstance(intent, dict):
            return {
                "success": False,
                "valid": False,
                "message": "Intent must be a dictionary."
            }

        required_fields = [
            "intent",
            "confidence",
            "parameters"
        ]

        required_validation = self.validate_required(
            intent,
            required_fields
        )

        if not required_validation["valid"]:
            return required_validation

        # Validate intent name
        if not isinstance(intent["intent"], str):
            return {
                "success": True,
                "valid": False,
                "message": "Intent name must be text."
            }

        if not intent["intent"].strip():
            return {
                "success": True,
                "valid": False,
                "message": "Intent name cannot be empty."
            }

        # Validate confidence
        confidence = intent["confidence"]

        if not isinstance(confidence, (int, float)):
            return {
                "success": True,
                "valid": False,
                "message": "Confidence must be a number."
            }

        if not 0 <= confidence <= 1:
            return {
                "success": True,
                "valid": False,
                "message": "Confidence must be between 0 and 1."
            }

        # Validate parameters
        if not isinstance(intent["parameters"], dict):
            return {
                "success": True,
                "valid": False,
                "message": "Intent parameters must be a dictionary."
            }

        return {
            "success": True,
            "valid": True,
            "message": "Intent is valid."
        }