""" tests for the creation of local test folders structure."""
from box_uploads.sample_folders import check_sample_folders, remove_local_sample_folder
from tests.conftest import get_settings

settings = get_settings()


def test_check_sample_folders_from_none():
    """tetst check_sample_folders() while not having any folder at all"""

    remove_local_sample_folder(settings.sample_folder_base_dir)
    sample_folders = check_sample_folders(settings.sample_folder_base_dir)

    assert sample_folders == settings.sample_folder_base_dir
