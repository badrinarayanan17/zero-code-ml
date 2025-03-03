import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'csv', 'xlsx', 'json', 'parquet'}
    MAX_FILE_SIZE = 1024 * 1024 * 100  # 100MB
    MAX_CONTENT_LENGTH = 1024 * 1024 * 100  # 100MB
    
    @staticmethod
    def init_app(app):
        # Create upload folder if not exists
        if not os.path.exists(Config.UPLOAD_FOLDER):
            os.makedirs(Config.UPLOAD_FOLDER)