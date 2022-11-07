from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

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

class NewProject(BaseModel):
    title: str
    description: str
    open_positions: list
    link_to_repo: str

@app.get("/projects")
async def getAllProjects():
    cur.execute(""" SELECT * FROM projects """)
    projects = cur.fetchall()
    print(projects)
    return {'data': projects}

@app.post("/projects")
async def addProject(new_project: NewProject):
    print(new_project)
    cur.execute(""" INSERT INTO projects (title, description, open_positions, link_to_repo) VALUES (%s, %s, %s, %s) RETURNING * """, (new_project.title, new_project.description, new_project.open_positions, new_project.link_to_repo)) 
    project_details = cur.fetchone()
    conn.commit()
    return {"new_project": project_details}