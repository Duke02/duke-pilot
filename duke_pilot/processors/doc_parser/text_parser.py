import logging
from typing import BinaryIO
import typing as tp

from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


@logger.log
def from_file_io(f: BinaryIO, file_ext: str) -> str:
    return f.read().decode('utf-8')
