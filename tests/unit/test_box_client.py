"""unit tests for box client"""

from box.box_client import box_client_get, box_client_as_user_get


def test_box_client_get():
    """should return a box client"""

    client = box_client_get(".jwt.config.json")
    assert client is not None

    user = client.user().get()
    assert user is not None
    assert user.name == "UI-Elements-Sample"


def test_box_client_as_user_get():
    """should return a box client as user"""

    service_client = box_client_get(".jwt.config.json")
    assert service_client is not None

    client = box_client_as_user_get(service_client, "18622116055")

    user = client.user().get()
    assert user is not None
    assert user.login == "barduinor@gmail.com"

    # TODO: dinamically configure the test user
