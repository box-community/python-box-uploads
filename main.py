"""main app demo"""
import logging

from box_uploads.box_client import box_client_get, box_client_as_user_get
from box_uploads.box_file import file_upload, file_upload_chunked, file_upload_manual
from box_uploads.config import Settings
from box_uploads.sample_files import check_sample_files

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

    # check if sample files exist and create them if not
    sample_files = check_sample_files()

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

    print("Box Python SDK - Upload Demo")
    print("=" * 40)

    sample_file = sample_files["micro"][1]
    print(f" Normal upload {sample_file}", end="\r")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    print(f" Normal upload {sample_file} in {str(round(elapsed, 1))} seconds.")

    print("-" * 40)

    sample_file = sample_files["small"][1]
    print(f" Normal upload {sample_file}", end="\r")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    print(f" Normal upload {sample_file} in {str(round(elapsed, 1))} seconds.")

    print(f" Chunked upload {sample_file}, 2 threads", end="\r")
    _, elapsed = file_upload_chunked(client, sample_file, demo_folder.id, 2)
    print(
        f" Chunked upload {sample_file}, 2 threads in {str(round(elapsed, 1))} seconds."
    )

    print("-" * 40)

    sample_file = sample_files["medium"][1]
    print(f" Normal upload {sample_file}", end="\r")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    print(f" Normal upload {sample_file} in {str(round(elapsed, 1))} seconds.")

    print(f" Chunked upload {sample_file}, 5 threads", end="\r")
    _, elapsed = file_upload_chunked(client, sample_file, demo_folder.id, 5)
    print(
        f" Chunked upload {sample_file}, 5 threads in {str(round(elapsed, 1))} seconds."
    )

    print("-" * 40)

    sample_file = sample_files["medium"][1]
    print(f" Manual upload {sample_file}")
    _, elapsed = file_upload_manual(client, sample_file, demo_folder.id)
    print(f" in {str(round(elapsed, 1))} seconds.")

    print("-" * 40)

    sample_file = sample_files["large"][1]
    print(f" Manual upload {sample_file}")
    _, elapsed = file_upload_manual(client, sample_file, demo_folder.id)
    print(f" in {str(round(elapsed, 1))} seconds.")

    print("=" * 40)
    print("All done")


if __name__ == "__main__":
    main()
