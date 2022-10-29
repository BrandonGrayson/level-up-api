from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

origins = ['http://localhost']

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
    cursor = conn.cursor()
    print("database connection successful")

except Exception as error: 
    print("connection to database failed")
    print("Error", error)



class Project(BaseModel):
    title: str
    description: str
    open_positions: list
    link_to_repo: str

@app.post("/projects")
async def getAll(project: Project):
    
    return {"project": project}