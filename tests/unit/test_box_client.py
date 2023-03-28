"""unit tests for box client"""

from box_uploads.box_client import box_client_get, box_client_as_user_get
from tests.conftest import get_settings

settings = get_settings()


def test_box_client_get():
    """should return a box client"""

    client = box_client_get(settings.jwt_config_path)
    assert client is not None

    user = client.user().get()
    assert user is not None
    assert user.name == settings.login_service_user


def test_box_client_as_user_get():
    """should return a box client as user"""

    service_client = box_client_get(settings.jwt_config_path)
    assert service_client is not None

    client = box_client_as_user_get(service_client, settings.as_user_id)

    user = client.user().get()
    assert user is not None
    assert user.login == settings.login_as_user
