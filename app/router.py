from fastapi import FastAPI, Request, APIRouter
from AImanager import AImanager
from db_utils import MongoDB
from contracts import Data
from pprint import pprint


router = APIRouter(tags=["task"])

ai_manager = AImanager("./events.json")

@router.post("/process")
async def process(data: Data):
    string = data.string
    pprint(string)
    try:
        result = await ai_manager.process(string)
        return {"result": result}
    except Exception as e:
        pprint(e)
        return {"result": e}