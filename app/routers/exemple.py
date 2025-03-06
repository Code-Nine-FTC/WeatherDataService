from fastapi import APIRouter

router = APIRouter(tags=["example"], prefix="/example")

@router.get("/")
def hello_world():
    return {"msg": "Hello World"}