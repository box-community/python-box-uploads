""" Creation of sample files for testing."""

from enum import Enum
import os


class SizeUnits(Enum):
    """File sizes"""

    B = 1
    KB = 1024
    MB = 1024**2
    GB = 1024**3


def create_test_file(size_str: str, file_name: str) -> str:
    """create a test file"""

    size_bytes = int(size_str[:-2]) * SizeUnits[size_str[-2:]].value

    with open(file_name, "wb") as fout:
        while size_bytes > 0:
            wrote = min(size_bytes, 1024)  # chunk
            fout.write(os.urandom(wrote))
            size_bytes -= wrote
        result = fout.name
    return result


def check_test_file(size_str: str, file_name: str) -> bool:
    """check a test file exists and is the correct size"""
    if not os.path.isfile(file_name):
        return False
    size_bytes = int(size_str[:-2]) * SizeUnits[size_str[-2:]].value
    file_size = os.path.getsize(file_name)

    return file_size == size_bytes
