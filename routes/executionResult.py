from fastapi import APIRouter, Response, status, Depends
from schemas.executionResult import ExecutionResult
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from config.db import conn
from models.executionResult import execution_results
from models.user import users
from models.testCase import test_cases
from utils.tokenVrifiy import verify_jwt_token


executionResult = APIRouter()

@executionResult.get("/")
async def read_executionResults():
    arr = []
    try:
      query = execution_results.select()
      result = conn.execute(query).fetchall()
      for row in result:
          user_id = row[4]
          user_query = users.select().where(users.c.id == user_id)
          user_result = conn.execute(user_query).fetchone()
          test_case_id = row[1]
          test_case_query = test_cases.select().where(test_cases.c.id == test_case_id)
          test_case_result = conn.execute(test_case_query).fetchone()
          test = {
              "id": test_case_result[0],
              "name": test_case_result[1],
              "description": test_case_result[2]
          }
          user = {
              "id": user_result[0],
              "name": user_result[1],
              "username": user_result[2]
          }
          arr.append({
              "id": row[0],
              "test_case_id": test,
              "test_asset": row[2],
              "result": row[3],
              "user_id": user
          })
      return arr
    except Exception as e:
      return {"status": "error", "message": str(e)}

@executionResult.post("/")
async def create_executionResult(executionResult: ExecutionResult, response: Response, token: str = Depends(OAuth2PasswordBearer(tokenUrl="access_token"))):
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
    except:
        return {"status": "error", "message": "Invalid token"}
    try:
      query = test_cases.select().where(test_cases.c.id == executionResult.test_case_id)
      result = conn.execute(query).fetchone()
      if not result:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Test case not found"}
    except Exception as e:
      response.status_code = status.HTTP_400_BAD_REQUEST
      return {"status": "error", "message": str(e)}
    
    query = execution_results.insert().values(
        test_case_id=executionResult.test_case_id,
        test_asset=executionResult.test_asset,
        result=executionResult.result,
        user_id=user_id
    )
    try:
        conn.execute(query)
        return {"status": "success", "message": "Execution result created successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Execution result already exists"}

@executionResult.get("/user")
async def read_user_executionResults(token: str = Depends(OAuth2PasswordBearer(tokenUrl="access_token"))):
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
    except:
        return {"status": "error", "message": "Invalid token"}
    arr = []
    query = execution_results.select().where(execution_results.c.user_id == user_id)
    result = conn.execute(query).fetchall()
    for row in result:
        test_case_id = row[1]
        test_case_query = test_cases.select().where(test_cases.c.id == test_case_id)
        test_case_result = conn.execute(test_case_query).fetchone()
        test = {
            "id": test_case_result[0],
            "name": test_case_result[1],
            "description": test_case_result[2]
        }
        arr.append({
            "id": row[0],
            "test_case_id": test,
            "test_asset": row[2],
            "result": row[3]
        })
    return arr