from fastapi import FastAPI, HTTPException
from pathlib import Path
import os
from task_handler import TaskHandler

app = FastAPI()
task_handler = TaskHandler()

@app.post("/run")
async def run_task(task: str):
    try:
        result = await task_handler.execute(task)
        return {"status": "success", "result": result}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/read")
async def read_file(path: str):
    try:
        file_path = Path(path)
        if not file_path.is_file():
            raise HTTPException(status_code=404)
        
        content = file_path.read_text()
        return content
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
