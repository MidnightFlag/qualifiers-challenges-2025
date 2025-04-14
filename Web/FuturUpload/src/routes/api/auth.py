import os
import uuid

from config import Config
from models import get_user_by_username, create_user
from flask import Blueprint, request, session, redirect, render_template, flash


auth_api = Blueprint('auth_api', __name__)

@auth_api.route('/api/login', methods=['POST'])
def api_login():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Missing parameters.', 'error')
        return redirect('/')
        
    user = get_user_by_username(username)
    if user and user[2] == password:
        session['user_id'] = user[0]
        session['username'] = user[1]
        return redirect('/home')
    flash('Invalid credentials.', 'error')
    return redirect('/')

@auth_api.route('/api/register', methods=['POST'])
def api_register():
    username = request.form.get('username')
    password = request.form.get('password')
    if not username or not password:
        flash('Missing parameters.', 'error')
        return redirect('/')

    if get_user_by_username(username):
        flash('Username already exists.', 'error')
        return redirect('/')

    rootfolder = str(uuid.uuid4())
    os.makedirs(os.path.join(Config.UPLOAD_FOLDER, rootfolder), exist_ok=True)
    create_user(username, password, rootfolder)

    user = get_user_by_username(username)
    session['user_id'] = user[0]
    session['username'] = user[1]
    return redirect('/home')

@auth_api.route('/logout', methods=['POST'])
def logout():
    session.clear()
    return redirect('/login')