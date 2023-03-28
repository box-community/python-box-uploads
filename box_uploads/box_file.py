""" handles file uploads to box"""
import os
import time
from typing import Tuple

from boxsdk import BoxAPIException, Client
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.config import API


def file_upload(client: Client, file_path: str, folder_id: str) -> Tuple[File, float]:
    """upload a file to box"""

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    folder = get_folder_by_id(client, folder_id).get()
    file_id = None
    try:
        folder.preflight_check(file_size, file_name)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            file_id = err.context_info["conflicts"]["id"]
        else:
            raise err

    start = time.time()

    if file_id is not None:
        file = get_file_by_id(client, file_id)
        file = file.update_contents(file_path)
    else:
        file = client.folder(folder_id).upload(file_path, file_name)

    end = time.time()

    return file, end - start


def get_folder_by_id(client: Client, folder_id: str) -> Folder:
    """get a folder by id"""
    return client.folder(folder_id).get()


def get_file_by_id(client: Client, file_id: str) -> File:
    """get a file by id"""
    return client.file(file_id).get()


def file_upload_chunked(
    client: Client, file_path: str, folder_id: str, upload_threads: int = 5
) -> Tuple[File, float]:
    """upload a file to box"""

    API.CHUNK_UPLOAD_THREADS = upload_threads

    file_size = os.path.getsize(file_path)
    file_name = os.path.basename(file_path)

    folder = get_folder_by_id(client, folder_id)
    file_id = None

    try:
        folder.preflight_check(file_size, file_name)
    except BoxAPIException as err:
        if err.code == "item_name_in_use":
            file_id = err.context_info["conflicts"]["id"]
        else:
            raise err

    start = time.time()
    if file_id is not None:
        file = get_file_by_id(client, file_id)
        uploader = file.get_chunked_uploader(file_path, file_name)
    else:
        uploader = folder.get_chunked_uploader(file_path, file_name)
    file = uploader.start()

    end = time.time()
    return file, end - start
