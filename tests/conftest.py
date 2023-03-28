""" pytest configuration file for tests."""

from time import time
import pytest
from box_uploads.config import Settings
from box_uploads.box_client import box_client_get, box_client_as_user_get
from box_uploads.sample_files import check_sample_files


def get_settings() -> Settings:
    """get settings"""

    settings = Settings(".jwt.config.json", "18622116055")
    settings.login_service_user = "UI-Elements-Sample"
    settings.login_as_user = "barduinor@gmail.com"

    return settings


@pytest.fixture(scope="module")
def sample_files():
    """create sample test files"""

    sample_local_files = check_sample_files()

    yield sample_local_files


@pytest.fixture(scope="module")
def box_test_folder():
    """create a test folder in box"""

    settings = get_settings()
    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)

    folder = client.folder("0").create_subfolder(
        "unit-testing-uploads-" + str(time()).replace(".", "-")
    )
    yield folder
    folder.delete()
