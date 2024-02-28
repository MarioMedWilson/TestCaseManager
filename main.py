from contextlib import asynccontextmanager

from fastapi import FastAPI
from routes.user import user
from models.user import users
from models.testCase import test_cases
from models.executionResult import execution_results
from config.db import db, meta, inspect





# @app.on_event("startup")
# async def startup():
#   meta.create_all(bind=db)

@asynccontextmanager
async def lifespan(app: FastAPI):
  if not inspect(db).get_table_names():
    meta.create_all(bind=db, checkfirst=False)
    print("Database created")
  else:
    print("Database already exists")
  print(inspect(db).get_table_names())
  yield

app = FastAPI(lifespan=lifespan)

app.include_router(user, prefix='/user', tags=['user'])
