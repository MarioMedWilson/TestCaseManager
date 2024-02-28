import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")


def create_jwt_token(data: dict, expiration_minutes: int = 1):
    expiration = datetime.utcnow() + timedelta(minutes=expiration_minutes)
    token_data = {"exp": expiration, **data}
    token = jwt.encode(token_data, SECRET_KEY, algorithm="HS256")
    return token

