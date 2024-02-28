from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from routes.user import user
from routes.testCase import testCase
from routes.executionResult import executionResult
from models.user import users
from models.testCase import test_cases
from models.executionResult import execution_results
from config.db import db, meta, inspect

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
app.include_router(testCase, prefix='/testcase', tags=['testcase'])
app.include_router(executionResult, prefix='/executionresult', tags=['executionresult'])
