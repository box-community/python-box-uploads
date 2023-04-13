"""main app demo"""
import logging

from box_uploads.box_client import box_client_get, box_client_as_user_get
from box_uploads.config import Settings
from box_uploads.sample_folders import check_sample_folders
from box_uploads.box_folder import folder_upload

logging.basicConfig(
    level=logging.WARNING,
    filename="upload_demo.log",
    filemode="w",
    format="%(name)s - %(levelname)s - %(message)s",
)


def get_settings() -> Settings:
    """get settings"""

    settings = Settings(".jwt.config.json", "18622116055")
    settings.login_service_user = "UI-Elements-Sample"
    settings.login_as_user = "barduinor@gmail.com"

    return settings


def main():
    """main app demo"""
    settings = get_settings()

    # check if sample folder exist and create them if not
    sample_folder = check_sample_folders(settings.sample_folder_base_dir)

    # get a client
    service_client = box_client_get(settings.jwt_config_path)

    # get a client as user
    client = box_client_as_user_get(service_client, settings.as_user_id)

    # create a demo upload folder in root if not exists
    item = [
        item
        for item in client.folder("0").get_items()
        if (item.name == "Upload demo" and item.type == "folder")
    ]
    if len(item) == 0:
        demo_folder = client.folder("0").create_subfolder("Upload demo")
    else:
        demo_folder = item[0].get()

    print("Box Python SDK - Upload Folder Demo")
    print("=" * 40)
    print(f" Uploading folder {sample_folder}")
    print("-" * 40)
    folder_upload(client, demo_folder, settings.sample_folder_base_dir)


if __name__ == "__main__":
    main()
    print("=" * 40)
    print("All done")
