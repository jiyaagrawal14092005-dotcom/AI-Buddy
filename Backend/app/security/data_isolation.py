class DataIsolationManager:

    def __init__(self):

        self.user_data = {}

    def create_user_store(
        self,
        user_id: str
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if user_id not in self.user_data:

            self.user_data[user_id] = {}

        return {
            "success": True,
            "user_id": user_id,
            "message": "User data store created successfully."
        }

    def save_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str,
        data
    ) -> dict:

        if not user_id:
            return {
                "success": False,
                "message": "User ID is required."
            }

        if not data_type:
            return {
                "success": False,
                "message": "Data type is required."
            }

        if not data_id:
            return {
                "success": False,
                "message": "Data ID is required."
            }

        if user_id not in self.user_data:
            self.user_data[user_id] = {}

        if data_type not in self.user_data[user_id]:
            self.user_data[user_id][data_type] = {}

        self.user_data[user_id][data_type][data_id] = data

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "message": "Data saved securely for the user."
        }

    def get_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> dict:

        user_store = self.user_data.get(user_id)

        if not user_store:
            return {
                "success": False,
                "message": "User data store not found."
            }

        type_store = user_store.get(data_type)

        if not type_store:
            return {
                "success": False,
                "message": "Data type not found."
            }

        if data_id not in type_store:
            return {
                "success": False,
                "message": "Data not found."
            }

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data_id": data_id,
            "data": type_store[data_id]
        }

    def get_all_data(
        self,
        user_id: str,
        data_type: str
    ) -> dict:

        user_store = self.user_data.get(user_id)

        if not user_store:
            return {
                "success": False,
                "message": "User data store not found."
            }

        data = user_store.get(
            data_type,
            {}
        )

        return {
            "success": True,
            "user_id": user_id,
            "data_type": data_type,
            "data": data.copy()
        }

    def user_owns_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> bool:

        user_store = self.user_data.get(user_id)

        if not user_store:
            return False

        type_store = user_store.get(data_type)

        if not type_store:
            return False

        return data_id in type_store

    def delete_data(
        self,
        user_id: str,
        data_type: str,
        data_id: str
    ) -> dict:

        if not self.user_owns_data(
            user_id,
            data_type,
            data_id
        ):
            return {
                "success": False,
                "message": "Data does not belong to this user."
            }

        del self.user_data[user_id][data_type][data_id]

        return {
            "success": True,
            "user_id": user_id,
            "data_id": data_id,
            "message": "User data deleted successfully."
        }

    def clear_user_data(
        self,
        user_id: str
    ) -> dict:

        if user_id not in self.user_data:
            return {
                "success": False,
                "message": "User data store not found."
            }

        self.user_data[user_id].clear()

        return {
            "success": True,
            "user_id": user_id,
            "message": "All user data cleared successfully."
        }

    def get_user_data_types(
        self,
        user_id: str
    ) -> list:

        user_store = self.user_data.get(
            user_id,
            {}
        )

        return list(user_store.keys())