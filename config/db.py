from sqlalchemy import create_engine, MetaData
from sqlalchemy import inspect

# Database connection
db = create_engine('sqlite:///db.sqlite3')
meta = MetaData()

conn = db.connect()
