import logging
import typing as tp

from fastapi import APIRouter, UploadFile, status
from fastapi.responses import JSONResponse, Response

from duke_pilot.api.models.parser import ParseResponse
from duke_pilot.processors.parser import DocParser
from duke_pilot.utils.log_utils import DukeLogger


logger: DukeLogger = DukeLogger()

router: APIRouter = APIRouter(prefix='/parser', tags=['parser'])


@logger.log
def _get_parser() -> DocParser:
    if hasattr(_get_parser, 'parser'):
        return getattr(_get_parser, 'parser')
    parser: DocParser = DocParser()
    setattr(_get_parser, 'parser', parser)
    return parser


@router.post('/parse', status_code=status.HTTP_200_OK)
async def parse(file: UploadFile, force: bool = False, response: Response = Response()) -> ParseResponse:
    """
    Parses the provided file and gives you the text.

    :param file: The file to parse.
    :param force: Force the parser to parse even if the parser doesn't think it supports the file type (set this to True if you're ingesting a file with code).

    :return: The parsed text.
    """
    logger.info(f'Parsing {file.filename}...', force_parse=force)
    parser = _get_parser()
    file_ext = file.filename.split('.')[-1]
    if not force and file_ext not in parser.supported_file_extensions:
        logger.error(f'File extension {file_ext} is not supported.')
        response.status_code = status.HTTP_406_NOT_ACCEPTABLE
        return ParseResponse(successful=False, error='File extension not supported.', file_ext_used=file_ext, text=None)
    try:
        text_parsed: str = parser.parse(file.file, file_ext)
    except Exception as e:
        logger.error(f'Failed to parse {file.filename} (Got Exception="{e}").')
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return ParseResponse(successful=False, error=str(e), file_ext_used=file_ext, text=None)
    logger.info('Parsed document successfully!')
    response.status_code = status.HTTP_200_OK
    return ParseResponse(successful=True, text=text_parsed, error=None, file_ext_used=file_ext)
