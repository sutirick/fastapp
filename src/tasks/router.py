from fastapi_users import FastAPIUsers
from fastapi import APIRouter, BackgroundTasks, Depends
from src.auth.database import User
from src.auth.manager import get_user_manager
from src.tasks.tasks import send_email_report_dashboard, test_task
from src.auth.auth import auth_backend

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()

router=APIRouter(prefix='/report', tags=['Tasks'])

@router.get('/dashboard')
def get_dashboard_report(user=Depends(current_user)):
    send_email_report_dashboard.delay(user.username)
    return {
        "status": 200,
        "data": "Письмо отправлено",
        "details": None
    }


@router.get('/test')
def testing_test_task():
    test_task.delay()
    return{
        'status':'Ok'
    }