from fastapi import APIRouter
from fastapi import status
from schemas.demo import DemoItem
import asyncio
import time
from fastapi import Depends

router = APIRouter(prefix="/demo", tags=["demo"])

@router.get("/hello/{name}")
async def greet_user(name: str):
  return {"message": f"Hello, {name}! Welcome to fittrack."}
  
@router.get("/items")
async def list_items(limit: int = 10, skip: int = 0):
  return {"limit": limit, "skip": skip, "items": ["dumbbell", "barbell", "plate", "bench", "tire", "medicine ball", "jump rope"]}

@router.post("/create", response_model=DemoItem, status_code=status.HTTP_201_CREATED)
async def create_item(item: DemoItem):
  return item

@router.get("/sync-wait")
def sync_wait():
    time.sleep(2)
    return {"type": "sync", "message": "Finished blocking wait"}

@router.get("/async-wait")
async def async_wait():
    await asyncio.sleep(2)
    return {"type": "async", "message": "Finished non-blocking wait"}

def get_current_user():
  return {"id": 1, "username": "admin"}

@router.get("/me")
async def read_me(user=Depends(get_current_user)):
  return user

def pagination_params(limit: int = 10, skip: int = 0):
  return {"limit": limit, "skip": skip}

@router.get("/deep-items")
async def list_items_deps(params=Depends(pagination_params)):
  return params 

def get_resource():
    print("Acquire resource")
    try:
        yield "RESOURCE"
    finally:
        print("Release resource")

@router.get("/resource")
async def use_resource(res=Depends(get_resource)):
    return {"resource": res}