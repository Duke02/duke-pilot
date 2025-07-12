from typing import BinaryIO


def from_file_io(f: BinaryIO, file_ext: str) -> str:
    return f.read().decode('utf-8')
