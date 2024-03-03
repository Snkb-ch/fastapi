from fastapi import FastAPI, BackgroundTasks, APIRouter

router = APIRouter(

)
from background import background_task

@router.post("/start-background-task/")
async def start_background_task(background_tasks: BackgroundTasks, name: str, wait: int = 60):
    background_tasks.add_task(background_task, name, wait)
    return {"message": f"Task {name} has been started! Will complete in {wait} seconds."}