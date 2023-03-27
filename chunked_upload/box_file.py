""" handles file uploads to box"""
import os
import time
from typing import Tuple

from boxsdk import Client
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.config import API


def file_upload(client: Client, file_path: str, folder_id: str) -> Tuple[File, float]:
    """upload a file to box"""

    start = time.time()
    file_name = os.path.basename(file_path)
    file = client.folder(folder_id).upload(file_path, file_name)
    end = time.time()

    return file, end - start


def get_folder_by_id(client: Client, folder_id: str) -> Folder:
    """get a folder by id"""
    return client.folder(folder_id).get()


def file_upload_chunked(
    client: Client, file_path: str, folder_id: str, upload_threads: int
) -> Tuple[File, float]:
    """upload a file to box"""

    API.CHUNK_UPLOAD_THREADS = upload_threads

    folder = get_folder_by_id(client, folder_id)
    file_name = os.path.basename(file_path)

    start = time.time()

    uploader = folder.get_chunked_uploader(file_path, file_name)
    file = uploader.start()

    end = time.time()
    return file, end - start
