from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from app.database.supabase import Supabase

mainRouter = APIRouter(tags=['Main APIs'])

dbClient = Supabase.initialize()

@mainRouter.get('/')
def main():
    return RedirectResponse(url = '/docs')

@mainRouter.get('/get-ip')
async def get_ip(request: Request):
    client_ip = request.client.host
    return {"ip_address": client_ip}