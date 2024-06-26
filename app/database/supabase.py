import os
from config import Config
from supabase import create_client, Client

class Supabase:

    @staticmethod
    def initialize():
        url: str = Config.SUPABASE_URL
        key: str = Config.SUPABASE_KEY
        
        client: Client = create_client(url, key)

        return client