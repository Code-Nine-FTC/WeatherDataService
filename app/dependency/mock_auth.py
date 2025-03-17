from fastapi import Depends, HTTPException
from pydantic import BaseModel

class MockUser(BaseModel):
    id: int = 1
    role: str = "admin"
    name: str = "mock user"
    

async def get_current_user_mock():
    return MockUser()