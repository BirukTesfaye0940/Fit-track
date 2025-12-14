from fastapi import FastAPI
from routers.demo import router as demo_router

app = FastAPI()

app.include_router(demo_router)

@app.get("/")
async def root():
  return {"message": "FitTrack API is alive"}