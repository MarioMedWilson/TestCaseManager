from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from config.db import conn
from models.testCase import test_cases
from models.user import users
from schemas.testCase import TestCase
from utils.tokenVrifiy import verify_jwt_token

testCase = APIRouter()

@testCase.get("/")
async def read_testCases():
    query = test_cases.select()
    result = conn.execute(query).fetchall()
    arr = []
    for row in result:
        user_id = row[3]
        user_query = users.select().where(users.c.id == user_id)
        user_result = conn.execute(user_query).fetchone()
        user = {
            "id": user_result[0],
            "name": user_result[1],
            "username": user_result[2]
        }
        arr.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "user_id": user
        })
    return arr

@testCase.post("/")
async def create_testCase(testCase: TestCase, response: Response, token: str = Depends(OAuth2PasswordBearer(tokenUrl="access_token"))):
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
    except:
        return {"status": "error", "message": "Invalid token"}

    query = test_cases.insert().values(
        name=testCase.name,
        description=testCase.description,
        user_id=user_id
    )
    try:
        conn.execute(query)
        return {"status": "success", "message": "Test case created successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Test case already exists"}
    
@testCase.get("/{id}")
async def read_testCase(id: int):
    query = test_cases.select().where(test_cases.c.id == id)
    result = conn.execute(query).fetchone()
    try :
        return {
            "id": result[0],
            "name": result[1],
            "description": result[2],
            "user_id": result[3]
        }
    except:
        return {"status": "error", "message": "Test case not found"}

@testCase.put("/{id}")
async def update_testCase(id: int, testCase: TestCase, response: Response, token: str = Depends(OAuth2PasswordBearer(tokenUrl="access_token"))):
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
    except:
        return {"status": "error", "message": "Invalid token"}

    query = test_cases.update().where(test_cases.c.id == id).values(
        name=testCase.name,
        description=testCase.description,
        user_id=user_id
    )
    try:
        conn.execute(query)
        return {"status": "success", "message": "Test case updated successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Test case not found"}
    
@testCase.delete("/{id}")
async def delete_testCase(id: int, response: Response, token: str = Depends(OAuth2PasswordBearer(tokenUrl="access_token"))):
    try:
        payload = verify_jwt_token(token)
        user_id = payload.get("sub")
    except:
        return {"status": "error", "message": "Invalid token"}

    query = test_cases.delete().where((test_cases.c.id == id) & (test_cases.c.user_id == user_id))
    try:
        result = conn.execute(query)
        if result.rowcount <= 0:
            return {"status": "error", "message": "Test case not found or you are not authorized to delete this test case"}
        return {"status": "success", "message": "Test case deleted successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Test case not found or you are not authorized to delete this test case"}
