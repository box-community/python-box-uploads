""" handles file uploads to box"""
import hashlib
import os
import time
from typing import Tuple

from boxsdk import BoxAPIException, Client
from boxsdk.object.file import File
from boxsdk.object.folder import Folder
from boxsdk.object.upload_session import UploadSession
from boxsdk.config import API


def get_folder_by_id(client: Client, folder_id: str) -> Folder:
    """get a folder by id"""
    return client.folder(folder_id).get()


def get_file_by_id(client: Client, file_id: str) -> File:
    """get a file by id"""
    return client.file(file_id).get()


def folder_get_upload_session(
    client: Client, folder_id: str, file_name: str, file_size: int
) -> UploadSession:
    """get a file by id"""
    return client.folder(folder_id).create_upload_session(file_size, file_name)


def file_get_upload_session(
    client: Client, file_id: str, file_name: str, file_size: int
) -> UploadSession:
    """get a file by id"""
    return client.file(file_id).create_upload_session(file_size, file_name)


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

    try:
        file = uploader.start()
    except BoxAPIException as err:
        if err.code == "upload_session_not_found":
            file = uploader.resume()
        else:
            raise err

    end = time.time()
    return file, end - start


def file_upload_manual(
    client: Client, file_path: str, folder_id: str
) -> Tuple[File, float]:
    """manually upload a file to box"""

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

    if file_id is not None:
        file = get_file_by_id(client, file_id)
        upload_session = file_get_upload_session(client, file.id, file_name, file_size)
    else:
        upload_session = folder_get_upload_session(
            client, folder.id, file_name, file_size
        )

    # file_stream = open(file_path, "rb")

    start = time.time()

    file_sha1 = hashlib.sha1()
    parts = []

    with open(file_path, "rb") as file_stream:
        for part_num in range(upload_session.total_parts):
            copied_length = 0
            chunk = b""
            while copied_length < upload_session.part_size:
                bytes_read = file_stream.read(upload_session.part_size - copied_length)
                if bytes_read is None:
                    continue
                if len(bytes_read) == 0:
                    break
                chunk += bytes_read
                copied_length += len(bytes_read)

            uploaded_part = upload_session.upload_part_bytes(
                chunk, part_num * upload_session.part_size, file_size
            )
            print("\tUploading [", end="")
            print("#" * int((part_num + 1)), end="")
            print(" " * (upload_session.total_parts - int(part_num + 1)), end="")
            print("]", end="\r" if part_num + 1 < upload_session.total_parts else "")
            parts.append(uploaded_part)
            file_sha1.update(chunk)

    # file_stream.close()

    content_sha1 = file_sha1.digest()
    uploaded_file = upload_session.commit(content_sha1=content_sha1, parts=parts)

    end = time.time()

    return uploaded_file, end - start
