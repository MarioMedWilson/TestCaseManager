from pydantic import BaseModel

class TestCase(BaseModel):
    name: str
    description: str

