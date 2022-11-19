from fastapi import FastAPI, status, HTTPException
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
from . import schemas, utils

origins = ['http://localhost:3000']

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods=["*"],
    allow_headers=["*"]
)

try: 
    conn = psycopg2.connect(host=settings.database_hostname, database=settings.database_name, user=settings.database_username, password=settings.database_password, cursor_factory=RealDictCursor)
    cur = conn.cursor()
    print("database connection successful")

except Exception as error: 
    print("connection to database failed")
    print("Error", error)

@app.get("/projects")
async def getAllProjects():
    cur.execute(""" SELECT * FROM projects """)
    projects = cur.fetchall()
    return {'data': projects}

@app.post("/projects")
async def addProject(new_project: schemas.NewProject):
    cur.execute(""" INSERT INTO projects (title, description, open_positions, link_to_repo) VALUES (%s, %s, %s, %s) RETURNING * """, (new_project.title, new_project.description, new_project.open_positions, new_project.link_to_repo)) 
    project_details = cur.fetchone()
    conn.commit()
    return {"new_project": project_details}

@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
async def newUser(user: schemas.UserCreate):

    hashed_password = utils.hashPassword(user.password)
    user.password = hashed_password

    cur.execute(""" INSERT INTO users (email, password) VALUES (%s, %s) RETURNING * """, (user.email, user.password))
    user_details = cur.fetchone()
    conn.commit()

    return user_details 

@app.get("/users/{id}", response_model=schemas.UserOut)
async def getUser(id: int, ):
    cur.execute(""" SELECT * FROM users WHERE id = %s """, (str(id),))

    project = cur.fetchone()
    
    if not project:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"user with id: {id} does not exist")
    
    return project

    