"""handles client connections to box"""
from boxsdk import Client, JWTAuth


def box_client_get(jwt_config_file_path: str) -> Client:
    """get a box client"""

    auth = JWTAuth.from_settings_file(jwt_config_file_path)
    return Client(auth)


def box_client_as_user_get(service_client: Client, as_user_id: str) -> Client:
    """get a box client as user"""

    user = service_client.user(as_user_id)
    return service_client.as_user(user)
