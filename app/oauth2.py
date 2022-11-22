from jose import JWTError, jwt
from datetime import datetime, timedelta

SECRET_KEY = "09d2e39d095b57be27d5a4940ebcd6ec81e6bbcc5839d2c4b6f02207a15a84d0"

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.now() + timedelta(ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

