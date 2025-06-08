import os
import openai
from dotenv import load_dotenv
load_dotenv()

API_KEY = os.environ.get('OPENAI_API_KEY')
openai.api_key = API_KEY
