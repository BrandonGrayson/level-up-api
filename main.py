from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Project(BaseModel):
    title: str
    description: str
    open_positions: list
    link_to_repo: str



@app.post("/add-project")
async def getAll(project: Project):
    return {"project": project}