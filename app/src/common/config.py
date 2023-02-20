import os

from dotenv import load_dotenv


class EnvConfig:
    def __init__(self):
        load_dotenv('.env')
        self.db_name: str = os.getenv('db_name')
        self.db_user: str = os.getenv('db_user')
        self.db_password: str = os.getenv('db_password')
        self.db_host: str = os.getenv('db_host')
        self.db_port: str = os.getenv('db_port')

