"""test for box upload file"""
from tests.conftest import get_settings
from box_uploads.box_client import box_client_get, box_client_as_user_get
from box_uploads.box_file import file_upload, file_upload_chunked

settings = get_settings()


def test_upload_file(box_test_folder, sample_files):
    """should upload a file"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)

    # test upload micro file (1 MB)
    file, elapsed = file_upload(client, sample_files["micro"][1], box_test_folder.id)
    assert file is not None
    assert elapsed > 0

    # uploading an existing file should create a new version and not give an error
    file, elapsed = file_upload(client, sample_files["micro"][1], box_test_folder.id)
    assert file is not None
    assert elapsed > 0


def test_upload_chunked(box_test_folder, sample_files):
    """should upload a chunked file"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)

    # test upload chunked
    file, elapsed = file_upload_chunked(
        client, sample_files["small"][1], box_test_folder.id
    )
    assert file is not None
    assert elapsed > 0
    print(f"Uploaded file {file.name} in {elapsed} seconds")

    # uploading an existing file should create a new version and not give an error
    file, elapsed = file_upload_chunked(
        client, sample_files["small"][1], box_test_folder.id
    )
    assert file is not None
    assert elapsed > 0
    print(f"Uploaded file {file.name} in {elapsed} seconds")
