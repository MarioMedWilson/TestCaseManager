import os
from fastapi import APIRouter, Response, status
from sqlalchemy.exc import IntegrityError
from config.db import conn
from schemas.user import User, UserLogin
from models.user import users
import bcrypt
from utils.tokenGen import create_jwt_token

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
            "username": row[2]
        })
    return arr


@user.post("/siginup")
async def create_user(user: User, response: Response):
    hashed_password = bcrypt.hashpw(user.password.encode('utf-8'), bcrypt.gensalt())
    query = users.insert().values(
        name=user.name,
        username=user.username,
        password=hashed_password.decode('utf-8')
    )
    print(query)
    try:
        conn.execute(query)
        return {"status": "success", "message": "User created successfully"}
    except IntegrityError as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Username already exists"}

@user.post("/login")
async def login_user(user: UserLogin, response: Response):
    if not user.password:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Password is required"}

    query = users.select().where(users.c.username == user.username)
    result = conn.execute(query).fetchone()

    if result and bcrypt.checkpw(user.password.encode('utf-8'), result[3].encode('utf-8')):
      token = create_jwt_token({"sub": result[0]}, expiration_minutes=1)

      return {"status": "success", "message": "User logged in successfully", "access_token": token}
    else:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {"status": "error", "message": "Invalid username or password"}

