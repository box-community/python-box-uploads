"""main app demo"""
import logging
from box_uploads.box_client import box_client_get, box_client_as_user_get
from box_uploads.box_file import file_upload, file_upload_chunked
from box_uploads.config import Settings
from box_uploads.curses_print import stdscr_get, stdscr_print, stdscr_end
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

    stdscr = stdscr_get()
    stdscr_print(stdscr, 0, 0, "Box Python SDK - Upload Demo")

    sample_file = sample_files["micro"][1]
    line = 2
    stdscr_print(stdscr, line, 0, "Normal upload file micro")
    stdscr_print(stdscr, line + 1, 0, "Uploading file " + sample_file + " ...")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    stdscr_print(
        stdscr,
        line + 1,
        0,
        "Uploaded file " + sample_file + " in " + str(round(elapsed, 1)) + " seconds",
    )

    line += 3

    sample_file = sample_files["small"][1]
    stdscr_print(stdscr, line, 0, "Normal upload file small")
    stdscr_print(stdscr, line + 1, 0, "Uploading file " + sample_file + " ...")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    stdscr_print(
        stdscr,
        line + 1,
        0,
        "Uploaded file " + sample_file + " in " + str(round(elapsed, 1)) + " seconds",
    )

    line += 2

    stdscr_print(stdscr, line, 0, "Chunked upload file small, 2 threads")
    stdscr_print(stdscr, line + 1, 0, "Uploading file " + sample_file + " ...")
    _, elapsed = file_upload_chunked(client, sample_file, demo_folder.id, 2)
    stdscr_print(
        stdscr,
        line + 1,
        0,
        "Uploaded file " + sample_file + " in " + str(round(elapsed, 1)) + " seconds",
    )

    line += 3
    sample_file = sample_files["medium"][1]
    stdscr_print(stdscr, line, 0, "Normal upload file medium")
    stdscr_print(stdscr, line + 1, 0, "Uploading file " + sample_file + " ...")
    _, elapsed = file_upload(client, sample_file, demo_folder.id)
    stdscr_print(
        stdscr,
        line + 1,
        0,
        "Uploaded file " + sample_file + " in " + str(round(elapsed, 1)) + " seconds",
    )

    line += 2
    stdscr_print(stdscr, line, 0, "Chunked upload file medium, 3 threads")
    stdscr_print(stdscr, line + 1, 0, "Uploading file " + sample_file + " ...")
    _, elapsed = file_upload_chunked(client, sample_file, demo_folder.id, 3)
    stdscr_print(
        stdscr,
        line + 1,
        0,
        "Uploaded file " + sample_file + " in " + str(round(elapsed, 1)) + " seconds",
    )

    line += 3
    stdscr_end(stdscr, line)


if __name__ == "__main__":
    main()
