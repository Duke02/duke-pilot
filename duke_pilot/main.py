import fastapi

from duke_pilot.api import parser, docstore, chat
from duke_pilot.utils.log_utils import DukeLogger

logger: DukeLogger = DukeLogger(__name__)

logger.info('Starting up API...', name=__name__)
app: fastapi.FastAPI = fastapi.FastAPI(root_path='/api/v1')
app.include_router(parser.router, tags=["parser"])
app.include_router(docstore.router, tags=["docstore"])
app.include_router(chat.router, tags=["chat"])

logger.info('Got API stood up!')
