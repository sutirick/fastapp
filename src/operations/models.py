from sqlalchemy import MetaData, Table, Column, Integer, String, TIMESTAMP, ForeignKey, JSON, Boolean

metadata=MetaData()

operation = Table(
    'operations',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('quantity',String, nullable=True),
    Column('figi' , String, nullable=True),
    Column('instrument_type', String, nullable=True),
    Column('date', TIMESTAMP, nullable=True),
    Column('type',String),
)