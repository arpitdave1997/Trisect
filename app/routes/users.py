from fastapi import APIRouter, Request, Response, status
from app.common.enums import ResponseStatusCodes
from app.common.helpers import UsersHelper
from app.database.supabase import Supabase

usersRouter = APIRouter(tags=['Users APIs'])

dbClient = Supabase.initialize()

@usersRouter.get('/users/details')
def registerUser(request: Request, response: Response):
    try:
        ipAddress = request.client.host
        userFlag, userObject = UsersHelper.fetchUserInfo(ipAddress)
        if not userFlag:
            userObject = UsersHelper.createUser(ipAddress)

        return userObject
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'status': ResponseStatusCodes.FAILURE,
            'message': str(e)
        }

@usersRouter.post('/users/activity/{userId}')
def updateSessionActivity(userId: str, response: Response):
    try:
        userFlag = UsersHelper.updateUserActivity(userId)
        if not userFlag:
            raise Exception()
        
        return {
            'status': 'success'
        }
    except Exception as e:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            'status': 'error',
            'message': str(e)
        }