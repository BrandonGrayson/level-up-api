from fastapi import APIRouter
from .. import schemas, utils
from ..main import cur, conn

router = APIRouter()

@router.get("/projects")
async def getAllProjects():
    cur.execute(""" SELECT * FROM projects """)
    projects = cur.fetchall()
    return {'data': projects}

@router.post("/projects")
async def addProject(new_project: schemas.NewProject):
    cur.execute(""" INSERT INTO projects (title, description, open_positions, link_to_repo) VALUES (%s, %s, %s, %s) RETURNING * """, (new_project.title, new_project.description, new_project.open_positions, new_project.link_to_repo)) 
    project_details = cur.fetchone()
    conn.commit()
    return {"new_project": project_details}