from sqlalchemy import Table, Column, Integer, String, DateTime, ForeignKey, ForeignKeyConstraint
from sqlalchemy.orm import relationship
from config.db import meta
from models.user import users
from models.testCase import test_cases

# Execution results table
execution_results = Table(
    'execution_results',
    meta,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('test_case_id', Integer, ForeignKey('test_cases.id'), nullable=False),
    Column('test_asset', String, nullable=False),
    Column('result', String, nullable=False),
    Column('execution_time', DateTime, server_default='CURRENT_TIMESTAMP'),
    Column('user_id', Integer, ForeignKey('users.id'), nullable=False),
)

# execution_results.append_column(Column('user_id', Integer, ForeignKey('users.id'), replace_existing=True))
# execution_results.append_constraint(
#     ForeignKeyConstraint(['user_id'], ['users.id'], name='fk_user_id')
# )

# execution_results.c.users = relationship('users', back_populates='execution_results')
