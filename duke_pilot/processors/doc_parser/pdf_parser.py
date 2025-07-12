import typing as tp

from PIL import Image
import pdf2image

from duke_pilot.processors.doc_parser import image_parser


def from_file_io(f: tp.BinaryIO, file_ext: str) -> str:
    image: Image = pdf2image.convert_from_bytes(f.read(), dpi=200)
    return image_parser.from_image(image)
