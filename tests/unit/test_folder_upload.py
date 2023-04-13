"""tests for box folder upload"""
import os
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
    box_base_folder = folder_upload(
        client,
        box_test_folder,
        sample_folders,
        settings.min_file_size_for_chunked_upload,
    )

    # check if the first level of box folder is correct
    box_item_list = [item.name for item in box_base_folder.get_items()]

    is_upload_ok = True
    for local_item in os.listdir(sample_folders):
        is_upload_ok = is_upload_ok and local_item in box_item_list

    assert is_upload_ok

    # uploading an existing folder should create a new version and not give an error

    # test upload folder a second time
    box_base_folder = folder_upload(
        client,
        box_test_folder,
        sample_folders,
        settings.min_file_size_for_chunked_upload,
    )

    # check if the first level of box folder is correct
    box_item_list = [item.name for item in box_base_folder.get_items()]

    is_upload_ok = True
    for local_item in os.listdir(sample_folders):
        is_upload_ok = is_upload_ok and local_item in box_item_list

    assert is_upload_ok
