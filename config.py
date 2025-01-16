import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    STRIPE_KEY = os.getenv('STRIPE_KEY', 'your-stripe-test-key')
    MODEL_NAME = os.getenv('MODEL_NAME', 'llama3-8b-8192')
    EMBEDDING_MODEL = os.getenv('EMBEDDING_MODEL', 'BAAI/bge-small-en-v1.5')
    UPLOAD_FOLDER = os.getenv('UPLOAD_FOLDER', 'uploads')
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS = {'pdf', 'txt', 'md'}