from pydantic import EmailStr
from pydantic import BaseModel
from datetime import datetime

class NewProject(BaseModel):
    title: str
    description: str
    open_positions: list
    link_to_repo: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime