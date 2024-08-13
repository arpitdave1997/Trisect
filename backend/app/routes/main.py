from fastapi import APIRouter, WebSocket
from fastapi.responses import RedirectResponse
from app.database.supabase import Supabase

mainRouter = APIRouter(tags=['Main APIs'])

dbClient = Supabase.initialize()

@mainRouter.get('/')
def main():
    return RedirectResponse(url = '/docs')