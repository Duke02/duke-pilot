import fastapi

from duke_pilot.api import parser, docstore, chat

app: fastapi.FastAPI = fastapi.FastAPI(root_path='/api/v1')
app.include_router(parser.router, tags=["parser"])
app.include_router(docstore.router, tags=["docstore"])
app.include_router(chat.router, tags=["chat"])
