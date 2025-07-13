import typing as tp

from PIL import Image
import pdf2image

from duke_pilot.processors.doc_parser import image_parser


def from_file_io(f: tp.BinaryIO, file_ext: str) -> str:
    images: list[Image] = pdf2image.convert_from_bytes(f.read(), dpi=200)
    return ' '.join([image_parser.from_image(image) for image in images])
