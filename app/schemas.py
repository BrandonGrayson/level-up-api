from pydantic import EmailStr
from pydantic import BaseModel

class UserCreate(BaseModel):
    email: EmailStr
    password: str