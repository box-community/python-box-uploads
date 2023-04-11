""" create sample folder in box """
import randomfiletree
import os
from box_uploads.config import Settings


def check_sample_folders(sample_folder_base_dir: str) -> str:
    """verify if sample folders exist and creates them if not"""
    if not os.path.exists(sample_folder_base_dir):
        os.makedirs(sample_folder_base_dir)
        randomfiletree.iterative_tree(sample_folder_base_dir, 3, 3, 3, 3)

    return sample_folder_base_dir


def create_local_sample_folder():
    """create a local folder in the samples folder"""
    pass


def remove_local_sample_folder(sample_folder_base_dir: str):
    """remove a local folder in the samples folder and all its content"""
    pass
