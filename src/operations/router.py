import time

from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.database import get_async_session
from src.operations.models import operation
from src.operations.schemas import OperationCreate

from fastapi_cache.decorator import cache

router= APIRouter(
    prefix='/operations',
    tags=['Operations']
)

@router.get('/')
async def get_specific_operations(operation_type:str, session:AsyncSession = Depends(get_async_session)):
    try:
        query = select(operation).where(operation.c.type == operation_type)
        result = await session.execute(query)
        return{
            'status':'success',
            'data': result.all(),
            'details': None,
        }
    #дополнительный вариант обработки ошибок, когда мы хотим отправлять код пользователю 
    except ZeroDivisionError:
        raise HTTPException(status_code = 500,detail = {
            'status':'error',
            'data': None,
            'details': 'Деление на ноль',
        })
    except:
        return{
            'status':'error',
            'data': None,
            'details': None,

        }

#ORM - object relational model
#SQL Injection

@router.post('/')
async def add_specific_operations(new_operation: OperationCreate, session:AsyncSession = Depends(get_async_session)):
    stmt = insert(operation).values(**new_operation.dict())
    await session.execute(stmt)
    await session.commit()
    return {'status': 'success'}


#redis cashing endpoint !EXAMPLE!
@router.get('/long_operation')
@cache(expire=30)
def get_log_op():
    time.sleep(2)
    return "Данные которые долго расчитывались, теперь хранятся в редис 30 секунд"