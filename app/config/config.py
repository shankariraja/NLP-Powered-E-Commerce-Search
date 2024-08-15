import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
GEMINI_API_URL = "https://api.gemini.com/v1/chat/completions"

DATABASE_PATH = 'walmart_products.db'