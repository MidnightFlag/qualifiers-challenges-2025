import os

class Config:
    SECRET_KEY = os.urandom(32).hex()
    SESSION_TYPE = "filesystem"
    SESSION_KEY_PREFIX = os.urandom(32).hex()
    SESSION_PERMANENT = False
    MAX_CONTENT_LENGTH = 2 * 1024 * 1024
    UPLOAD_FOLDER = os.path.abspath("user_files")
    DATABASE = ":memory:"