""" handles file uploads to box"""
import os
import time
from typing import Tuple

from boxsdk import Client
from boxsdk.object.file import File


def file_upload(client: Client, file_path: str, folder_id: str) -> Tuple[File, float]:
    """upload a file to box"""

    start = time.time()
    with open(file_path, "rb") as file:
        file_name = os.path.basename(file_path)

        file = client.folder(folder_id).upload(file_path, file_name)

    end = time.time()
    return file, end - start
