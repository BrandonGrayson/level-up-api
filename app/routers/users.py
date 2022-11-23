from fastapi import APIRouter, HTTPException
from fastapi import status
from ..main import cur, conn
from .. import schemas, utils

router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def newUser(user: schemas.UserCreate):

    hashed_password = utils.hashPassword(user.password)
    user.password = hashed_password

    cur.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (user.email, user.password))
    user_details = cur.fetchone()
    conn.commit()

    return user_details 

@router.get("/users/{id}", response_model=schemas.UserOut)
async def getUser(id: int, ):
    cur.execute(""" SELECT * FROM users WHERE id = %s """, (str(id),))

    project = cur.fetchone()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return project