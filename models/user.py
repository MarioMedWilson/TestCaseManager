from sqlalchemy import Table, Column, Integer, String

from config.db import meta

# Users table
users = Table(
    'users',
    meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('username', String, unique=True, nullable=False),
    Column('password', String, nullable=False)
)
