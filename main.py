from fastapi import FastAPI

app = FastAPI()


@app.post("/add-project")
async def getAll():
    return {"project": "some project data"}