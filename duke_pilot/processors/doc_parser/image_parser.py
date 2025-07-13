import logging
import typing as tp

from PIL import Image
from pytesseract import image_to_string

from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


@logger.log
def from_file_io(f: tp.BinaryIO, file_ext: str) -> str:
    image: Image.Image = Image.open(f).convert('RGB')
    return from_image(image)


@logger.log
def from_image(img: Image) -> str:
    return image_to_string(img, lang='eng')
