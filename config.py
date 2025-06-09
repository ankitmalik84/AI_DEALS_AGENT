import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Keys
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
HUGGINGFACE_TOKEN = os.getenv("HUGGINGFACE_TOKEN")
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")  # Added for Indian deal search

# Twilio Configuration
TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_FROM = os.getenv("TWILIO_FROM","+14155238886")
MY_PHONE_NUMBER = os.getenv("MY_PHONE_NUMBER","+918449035579")
TWILIO_CONTENT_SID = os.getenv("TWILIO_CONTENT_SID")  # For WhatsApp templates

# Pushover Configuration
PUSHOVER_USER = os.getenv("PUSHOVER_USER")
PUSHOVER_TOKEN = os.getenv("PUSHOVER_TOKEN")

# Configuration class to access all keys
class Config:
    @staticmethod
    def get_openai_key():
        if not OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY not found in environment variables. Please add it to your .env file.")
        return OPENAI_API_KEY
    
    @staticmethod
    def get_deepseek_key():
        return DEEPSEEK_API_KEY  # Simply return the key, which will be None if not set

    @staticmethod
    def get_huggingface_token():
        if not HUGGINGFACE_TOKEN:
            raise ValueError("HUGGINGFACE_TOKEN not found in environment variables. Please add it to your .env file.")
        return HUGGINGFACE_TOKEN

    @staticmethod
    def get_twilio_credentials():
        if not all([TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, TWILIO_FROM, MY_PHONE_NUMBER]):
            raise ValueError("One or more Twilio configuration values are missing in your .env file.")
        return {
            "account_sid": TWILIO_ACCOUNT_SID,
            "auth_token": TWILIO_AUTH_TOKEN,
            "from_number": TWILIO_FROM,
            "to_number": MY_PHONE_NUMBER,
            "content_sid": TWILIO_CONTENT_SID  # Added for WhatsApp templates
        }

    @staticmethod
    def get_pushover_credentials():
        if not all([PUSHOVER_USER, PUSHOVER_TOKEN]):
            raise ValueError("Pushover credentials are missing in your .env file.")
        return {
            "user": PUSHOVER_USER,
            "token": PUSHOVER_TOKEN
        } 