from fastapi import FastAPI
from AImanager import AImanager
from pprint import pprint
from router import router


app = FastAPI(
    title="ITMO_mega_school_task_3",
    version="0.0.1",
    docs_url="/docs",
    redoc_url="/docs/redoc",
)

try:
    app.include_router(router)
except Exception as e:
    pprint(e)