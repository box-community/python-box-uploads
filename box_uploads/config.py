"""app config."""


class Settings:
    """Settings class for pytest."""

    def __init__(self, jwt_config_path: str = None, as_user_id: str = None):
        self.jwt_config_path = jwt_config_path
        self.as_user_id = as_user_id
        self.login_service_user = None
        self.login_as_user = None
        self.sample_folder_base_dir = "samples/folder_to_upload"
        self.min_file_size_for_chunked_upload = 1024 * 1024 * 1024

    def __repr__(self):
        return f"Settings({self.__dict__})"
