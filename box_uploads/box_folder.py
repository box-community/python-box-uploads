""" handles folder uploads to box"""
import hashlib
import pathlib
import time
from typing import Tuple

from boxsdk import BoxAPIException, Client
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.upload_session import UploadSession
from boxsdk.config import API

from box_uploads.box_file import file_upload


def create_box_folder(
    client: Client, folder_name: str, parent_folder: Folder
) -> Folder:
    """create a folder in box"""

    try:
        folder = parent_folder.create_subfolder(folder_name)
    except BoxAPIException as err:
        if err.status == 409:
            folder = client.folder(folder_name=folder_name, parent=parent_folder)
        else:
            raise err

    return folder


def folder_upload(
    client: Client, base_folder: Folder, local_folder_path: str
) -> Folder:
    """upload a folder to box"""

    local_folder = pathlib.Path(local_folder_path)

    for item in local_folder.iterdir():
        if item.is_dir():
            new_box_folder = create_box_folder(client, item.name, base_folder)
            folder_upload(client, new_box_folder, item)
        else:
            file_upload(client, item, base_folder.id)

    return base_folder
