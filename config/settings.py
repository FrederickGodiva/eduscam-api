import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    MAX_TURNS = 5
    MODEL_NAME = "gpt-4o-mini"
    SCAM_TYPES = ["fake_prize", "online_loan", "fake_job", "phishing_link"]

settings = Settings()
