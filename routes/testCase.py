from fastapi import APIRouter, Response, status, Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.exc import IntegrityError
from config.db import conn
from models.testCase import test_cases
from schemas.testCase import TestCase
from utils.tokenVrifiy import verify_jwt_token

testCase = APIRouter()

@testCase.get("/")
async def read_testCases():
    query = test_cases.select()
    result = conn.execute(query).fetchall()
    arr = []
    for row in result:
        arr.append({
            "id": row[0],
            "name": row[1],
            "description": row[2],
            "user_id": row[3]
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
    
