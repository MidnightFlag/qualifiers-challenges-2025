from flask import Blueprint, session, redirect, render_template
from models import get_user_by_id

views_blueprint = Blueprint('views', __name__)

@views_blueprint.route('/')
def index():
    if session.get('user_id'):
        return redirect('/home')
    return redirect('/login')

@views_blueprint.route('/login')
def login_view():
    return render_template('login.html')

@views_blueprint.route('/register')
def register_view():
    return render_template('register.html')

@views_blueprint.route('/home')
def home_view():
    user_id = session.get('user_id')
    if not user_id:
        return redirect('/login')
    user = get_user_by_id(user_id)
    return render_template('home.html', username=user[1])
