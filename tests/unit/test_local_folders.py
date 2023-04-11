""" tests for the creation of local test folders structure."""
from box_uploads.sample_folders import check_sample_folders
from tests.conftest import get_settings

settings = get_settings()


def test_check_sample_folders():
    """tetst check_sample_folders()"""
    sample_folders = check_sample_folders(settings.sample_folder_base_dir)

    assert sample_folders == settings.sample_folder_base_dir
