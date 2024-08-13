from fastapi import APIRouter
from app.common.helpers import UsersHelper
from app.database.supabase import Supabase

usersRouter = APIRouter(tags=['Users APIs'])

dbClient = Supabase.initialize()

@usersRouter.post('/users/register/{deviceIdentifier}')
def registerUser(deviceIdentifier: str):
    try:
        userFlag, userObject = UsersHelper.fetchUserInfo(deviceIdentifier)
        if not userFlag:
            userObject = UsersHelper.createUser(deviceIdentifier)

        return userObject
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }

@usersRouter.post('/users/activity/{userId}')
def updateSessionActivity(userId: str):
    try:
        userFlag = UsersHelper.updateUserActivity(userId)
        if not userFlag:
            raise Exception()
        
        return {
            'status': 'success'
        }
    except Exception as e:
        return {
            'status': 'error',
            'message': str(e)
        }