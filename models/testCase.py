from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from config.db import meta
from models.user import users

# Test cases table
test_cases = Table(
    'test_cases',
    meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String, nullable=False),
    Column('description', String),
    Column('created_at', DateTime, server_default='CURRENT_TIMESTAMP'),
    # Column('user_id', Integer, ForeignKey('users.id')),
)

# Use replace_existing=True to avoid DuplicateColumnError
test_cases.append_column(Column('user_id', Integer, ForeignKey('users.id'), replace_existing=True))
test_cases.append_column(Column('created_by_user', String))  # Add additional columns as needed

# Define the relationship here
test_cases.append_constraint(
    ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_id')
)

# users.c.test_cases = relationship('test_cases', back_populates='users')
