from dotenv import load_dotenv
import os


load_dotenv()

class Settings:
    DB_USER = os.environ["DB_USER"]
    DB_PASS = os.environ["DB_PASS"]
    DB_HOST = os.environ["DB_HOST"]
    DB_PORT = os.environ["DB_PORT"]

    def async_refer_to_db(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/dormitory"

settings = Settings()