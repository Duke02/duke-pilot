from fastapi import APIRouter, UploadFile
from fastapi.responses import JSONResponse

from duke_pilot.api.models.parser import ParseResponse
from duke_pilot.processors.parser import DocParser

router: APIRouter = APIRouter(prefix='/parser', tags=['parser'])


def _get_parser() -> DocParser:
    if hasattr(_get_parser, 'parser'):
        return getattr(_get_parser, 'parser')
    parser: DocParser = DocParser()
    setattr(_get_parser, 'parser', parser)
    return parser


@router.post('/parse')
async def parse(file: UploadFile, force: bool = False) -> ParseResponse:
    """
    Parses the provided file and gives you the text.

    :param file: The file to parse.
    :param force: Force the parser to parse even if the parser doesn't think it supports the file type (set this to True if you're ingesting a file with code).

    :return: The parsed text.
    """
    parser = _get_parser()
    file_ext = file.filename.rsplit('.', maxsplit=1)[0]
    if not force and file_ext not in parser.supported_file_extensions:
        return ParseResponse(successful=False, error='File extension not supported.', file_ext_used=file_ext, text=None)
    text_parsed: str = parser.parse(file.file, file_ext)
    return ParseResponse(successful=True, text=text_parsed, error=None, file_ext_used=file_ext)
