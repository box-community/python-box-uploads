""" handles folder uploads to box"""

import pathlib

from boxsdk import BoxAPIException, Client

from boxsdk.object.folder import Folder

from box_uploads.box_file import file_upload, file_upload_chunked


def create_box_folder(
    client: Client, folder_name: str, parent_folder: Folder
) -> Folder:
    """create a folder in box"""

    try:
        folder = parent_folder.create_subfolder(folder_name)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            folder_id = err.context_info["conflicts"][0]["id"]
            folder = client.folder(folder_id).get()
        else:
            raise err

    return folder


def folder_upload(
    client: Client,
    box_base_folder: Folder,
    local_folder_path: str,
    min_file_size: int = 1024 * 1024 * 20,
) -> Folder:
    """upload a folder to box"""

    local_folder = pathlib.Path(local_folder_path)

    for item in local_folder.iterdir():
        if item.is_dir():
            new_box_folder = create_box_folder(client, item.name, box_base_folder)
            print(f" Folder {item}")
            folder_upload(client, new_box_folder, item)
        else:
            if item.stat().st_size < min_file_size:
                file_upload(client, item, box_base_folder.id)
            else:
                file_upload_chunked(client, item, box_base_folder.id)
            print(f" \tUploaded  {item}")

    return box_base_folder
