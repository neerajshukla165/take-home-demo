import asyncpg
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# PostgreSQL connection pool
async def get_pool():
    return await asyncpg.create_pool(user= os.getenv("USER"), password= os.getenv("PASSWORD"),
                                     database= os.getenv("DATABASE"), host=os.getenv("HOST"))

