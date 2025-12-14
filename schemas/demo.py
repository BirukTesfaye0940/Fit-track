from pydantic import BaseModel

class DemoItem(BaseModel):
  name: str
  value: int