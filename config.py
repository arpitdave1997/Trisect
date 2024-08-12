import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    ENV = os.getenv('ENV')
    DEBUG_FLAG = True if ENV == 'debug' else False

    PORT = int(os.getenv('PORT') or '8000')

    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')