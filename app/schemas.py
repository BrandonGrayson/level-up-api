from pydantic import EmailStr
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr