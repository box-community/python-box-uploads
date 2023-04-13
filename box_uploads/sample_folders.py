""" create sample folder in box """
import randomfiletree
import os
from box_uploads.config import Settings
import shutil


def check_sample_folders(sample_folder_base_dir: str) -> str:
    """verify if sample folders exist and creates them if not"""
    if not os.path.exists(sample_folder_base_dir):
        os.makedirs(sample_folder_base_dir)
        randomfiletree.iterative_gaussian_tree(
            sample_folder_base_dir, nfiles=2.0, nfolders=0.5, maxdepth=3, repeat=4
        )

    return sample_folder_base_dir


def remove_local_sample_folder(sample_folder_base_dir: str):
    """remove a local folder in the samples folder and all its content"""
    shutil.rmtree(sample_folder_base_dir, ignore_errors=True)
