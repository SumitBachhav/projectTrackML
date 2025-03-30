import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
CORS_ORIGIN = os.getenv("CORS_ORIGIN")

if not MONGO_URI or not CORS_ORIGIN:
    raise ValueError("Missing environment variables")