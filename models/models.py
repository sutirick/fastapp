from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON
import datetime

metadata=MetaData()

roles = Table(
    'roles',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name',String, nullable=False),
    Column('permissons', JSON),
)

users=Table(
    'users',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('email', String, nullable=False),
    Column('username', String, nullable=False),
    Column('password', String, nullable=False),
    Column('registerd_at', TIMESTAMP, default=datetime.datetime.utcnow),
    Column('role_id', Integer, ForeignKey('roles.id')),

)

