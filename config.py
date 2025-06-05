import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SERPAPI_KEY = os.getenv('SERPAPI_KEY')
    OPENAI_KEY = os.getenv('OPENAI_KEY')