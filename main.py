
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from endpoints import router as endpoints_router

from fastapi.responses import FileResponse
import os

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(endpoints_router)

# Serve index.html at root
@app.get("/")
async def root():
    return FileResponse(os.path.join("static", "index.html"), media_type="text/html")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)