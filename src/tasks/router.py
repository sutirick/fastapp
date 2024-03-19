from fastapi import APIRouter, Depends

#from auth.base_config import current_user

router=APIRouter(prefix='/report', tags=['Tasks'])

@router.get('/dashboard')
def get_dashboard_report():
    return {
        'status':'ok'
    }