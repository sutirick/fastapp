from fastapi import APIRouter, Depends


router=APIRouter(prefix='/report', tags=['Tasks'])

@router.get('/dashboard')
def  get_dashboard_report(user=Depends):
    pass