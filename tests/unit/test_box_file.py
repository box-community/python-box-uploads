"""test for box upload file"""
from boxsdk.object.folder import Folder

from box_uploads.box_client import box_client_as_user_get, box_client_get
from box_uploads.box_file import file_upload, file_upload_chunked, file_upload_manual
from tests.conftest import get_settings

settings = get_settings()


def test_upload_file(box_test_folder: Folder, sample_files: dict):
    """should upload a file"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)
    assert client is not None

    # test upload micro file (1 MB)
    file, elapsed = file_upload(client, sample_files["micro"][1], box_test_folder.id)
    assert file is not None
    assert elapsed > 0

    # uploading an existing file should create a new version and not give an error
    file, elapsed = file_upload(client, sample_files["micro"][1], box_test_folder.id)
    assert file is not None
    assert elapsed > 0


def test_upload_chunked(box_test_folder: Folder, sample_files: dict):
    """should upload a chunked file"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)
    assert client is not None

    # test upload chunked
    file, elapsed = file_upload_chunked(
        client, sample_files["small"][1], box_test_folder.id
    )
    assert file is not None
    assert elapsed > 0

    # uploading an existing file should create a new version and not give an error
    file, elapsed = file_upload_chunked(
        client, sample_files["small"][1], box_test_folder.id
    )
    assert file is not None
    assert elapsed > 0


def test_manual_upload(box_test_folder: Folder, sample_files: dict):
    """should upload a file manually"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)
    assert client is not None

    sample_file = sample_files["medium"][1]

    file, elapsed = file_upload_manual(client, sample_file, box_test_folder.id)
    assert file is not None
    assert elapsed > 0
