from flask import Flask, render_template, request, redirect, url_for, jsonify, make_response
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import hashlib
from bot import visit
import os, jwt, websocket, threading
import mysql.connector

app = Flask(__name__)
app.config['SECRET_KEY'] = "gGcDZuHhigkF4mDicdE9UFhD7THd3ktD3yrt5AyqK93pGA84tvPdFZPsJu2JcTPU"

WEBSOCKET_PASSWORD = os.getenv('WEBSOCKET_PASSWORD')
user = os.getenv('MYSQL_USER')
password = os.getenv('MYSQL_PASSWORD')
database = os.getenv('MYSQL_DATABASE')
host = os.getenv('MYSQL_HOST')

limiter = Limiter(get_remote_address, app=app)

def create_jwt(username, is_admin):
    if is_admin:
        token = jwt.encode({
            'username': username,
            'is_admin': True,
        }, app.config['SECRET_KEY'], algorithm='HS256')
    else:
        token = jwt.encode({
            'username': username,
            'is_admin': False,
        }, app.config['SECRET_KEY'], algorithm='HS256')
    return token

def decode_jwt():
    token = request.cookies.get('token')
    if not token:
        return None
    try:
        decoded = jwt.decode(token, app.config['SECRET_KEY'], algorithms=['HS256'])
        return decoded
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

def call_db():
    db = mysql.connector.connect(host=host,user=user,password=password,database=database)

    cursor = db.cursor()

    return cursor, db

@app.errorhandler(429)
def ratelimit_handler(e):
    return jsonify({"error": "You have done too many reports. Please wait a few minutes"}), 429

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/report',methods=['GET'])
@limiter.limit("3 per minutes")
def report():
    thread = threading.Thread(target=visit, args=("http://127.0.0.1", "/panel",))
    thread.start()
    response = {"report": "Your report has been sent to the administrators. We will review the 5 latest messages from the chat."}
    return jsonify(response)

@app.route('/panel', methods=['GET', 'POST'])
def panel():
    decoded_token = decode_jwt()
    if decoded_token:
        cursor, db = call_db()
        cursor.execute("SELECT date, username, message FROM messages ORDER BY message_id DESC LIMIT 5;")
        logs = cursor.fetchall()
        db.close()
        return render_template('panel.html', logs=logs)
    return redirect(url_for('login'))
    
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '').strip()
        if username and password:
            cursor, db = call_db()
            cursor.execute("SELECT username, is_admin FROM website_users WHERE username = %s AND password = %s", (username, hashlib.md5(password.encode()).hexdigest()))
            user = cursor.fetchall()
            db.close()
            if user:
                token = create_jwt(user[0][0], user[0][1])
                response = make_response(redirect(url_for('panel')))
                response.set_cookie('token', token, httponly=True)
                return response
            return render_template('login.html', error=True)     
        else:
            return render_template('login.html', error=True)
    return render_template('login.html', error=False)

@app.route('/send_minecraft_cmd', methods=['POST'])
def send_minecraft_cmd():
    decoded_token = decode_jwt()
    if decoded_token:
        is_admin = decoded_token.get('is_admin')
        if is_admin:
            try:
                cmd = request.form.get('cmd')
                if not cmd:
                    return jsonify({'output': 'No command provided'}), 400
                ws = websocket.WebSocket()
                ws.connect("ws://mc-mctf:3000")
                ws.send(WEBSOCKET_PASSWORD+":"+cmd)          
                ws.close()
                return jsonify({'output': 'Command sent'})         
            except Exception as e:
                return jsonify({'output': 'An error occurred: ' + str(e)})
    return jsonify({'output': 'You are not authenticated'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=False)  
