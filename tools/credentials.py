import os
import openai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.environ.get("API_KEY")
DEPLOYMENT_CHAT = os.environ.get("DEPLOYMENT_CHAT")
openai.api_key = API_KEY