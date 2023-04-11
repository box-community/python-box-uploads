"""tests for box folder upload"""
from boxsdk.object.folder import Folder

from box_uploads.box_client import box_client_as_user_get, box_client_get
from box_uploads.box_folder import folder_upload
from tests.conftest import get_settings

settings = get_settings()


def test_folder_upload(box_test_folder: Folder, sample_folders: str):
    """should upload a folder"""
    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)
    assert client is not None

    # test upload folder
    folder_upload(client, box_test_folder, sample_folders)
    assert False

    # # uploading an existing folder should create a new version and not give an error
    # folder, elapsed = folder_upload(client, sample_folders, box_test_folder.id)
    # assert folder is not None
    # assert elapsed > 0
