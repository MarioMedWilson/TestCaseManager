from pydantic import BaseModel

class ExecutionResult(BaseModel):
  test_case_id: int
  test_asset: str
  result: str
