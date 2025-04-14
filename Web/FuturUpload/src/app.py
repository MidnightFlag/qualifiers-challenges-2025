from flask import Flask
from config import Config
from models import init_db
from flask_session import Session
from routes.views import views_blueprint
from routes.api import auth_api, files_api, folders_api


app = Flask(__name__)
app.config.from_object(Config)

Session(app)

init_db()

app.register_blueprint(views_blueprint)
app.register_blueprint(auth_api)
app.register_blueprint(files_api)
app.register_blueprint(folders_api)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, threaded=True)
