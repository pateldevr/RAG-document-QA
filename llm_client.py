from google import genai
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure API key
client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))