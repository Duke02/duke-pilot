from collections import defaultdict
import logging
from typing import BinaryIO
import typing as tp

from duke_pilot.processors.doc_parser import pdf_parser, image_parser, text_parser, doc_parser
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger(__name__)


class DocParser:
    @logger.log
    def __init__(self):
        self.parsers: dict[str, tp.Callable[[BinaryIO, str], str]] = defaultdict(lambda: text_parser.from_file_io)
        self.parsers['pdf'] = pdf_parser.from_file_io
        image_parsers: list[str] = ['jpeg', 'jpg', 'png', 'gif', 'bmp', 'webp', 'tiff']
        for ext in image_parsers:
            self.parsers[ext] = image_parser.from_file_io
        doc_parsers: list[str] = ['doc', 'docx', 'odt', 'ppt', 'pptx', 'odp', 'xlsx', 'xls', 'ods']
        for ext in doc_parsers:
            self.parsers[ext] = doc_parser.from_file_io
        self.parsers['txt'] = text_parser.from_file_io
        logger.info(f'Created DocParser', supported_file_exts=self.supported_file_extensions)

    def __str__(self) -> str:
        return f'DocParser(supported_file_extensions={self.supported_file_extensions})'

    @property
    def supported_file_extensions(self) -> set[str]:
        return set(self.parsers.keys())

    @logger.log
    def parse(self, f: BinaryIO, file_ext: str) -> str:
        parser_f: tp.Callable[[BinaryIO, str], str] = self.parsers[file_ext]
        return parser_f(f, file_ext)
