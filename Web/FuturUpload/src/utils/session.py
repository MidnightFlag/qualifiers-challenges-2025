import os
import hashlib

from flask import session
from models import get_user_by_id

def get_current_user():
    user_id = session.get("user_id")
    return get_user_by_id(user_id) if user_id else None