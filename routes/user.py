from fastapi import APIRouter, HTTPException, Response, status
from fastapi.responses import JSONResponse
from sqlalchemy.exc import IntegrityError
from config.db import conn
from schemas.user import User, UserLogin
from models.user import users

user = APIRouter()

@user.get("/")
async def read_users():
    query = users.select()
    result = conn.execute(query).fetchall()
    arr = []
    for row in result:
        arr.append({
            "id": row[0],
            "name": row[1],
            "username": row[2],
            "password": row[3]
        })

    return arr


@user.post("/")
async def create_user(user: User, response: Response):
    query = users.insert().values(
        name=user.name,
        username=user.username,
        password=user.password
    )
    print(query)
    try:
        conn.execute(query)
        return {"status": "success", "message": "User created successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail=f"Failed to create user. Reason: {str(e)}")

@user.post("/login")
async def login_user(user: UserLogin, response: Response):
    if not user.password:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Password is required"}

    query = users.select().where(users.c.username == user.username).where(users.c.password == user.password)
    result = conn.execute(query).fetchone()
    if result:
        return {"status": "success", "message": "User logged in successfully"}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return HTTPException(status_code=400, detail="Invalid username or password")

