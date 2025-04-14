import os
import shutil

from config import Config
from utils.session import get_current_user
from flask import Blueprint, request, jsonify

folders_api = Blueprint('folders_api', __name__)

@folders_api.route('/api/folder/create', methods=['POST'])
def create_folder():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    folder = request.form.get('folder', '').strip()
    if not folder or '..' in folder or folder.startswith('/'):
        return jsonify({'status': 'error', 'message': 'Invalid folder name'})

    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_path = os.path.normpath(os.path.join(base_path, folder))

    if not full_path.startswith(base_path):
        return jsonify({'status': 'error', 'message': 'Forbidden path'})

    if os.path.exists(full_path):
        return jsonify({'status': 'error', 'message': 'Folder already exists'})

    os.makedirs(full_path)
    return jsonify({'status': 'ok'})

@folders_api.route('/api/folder/list', methods=['POST'])
def list_folder():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    folder = request.form.get('folder', '').strip()
    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_path = os.path.normpath(os.path.join(base_path, folder))

    if not full_path.startswith(base_path) or not os.path.exists(full_path):
        return jsonify({'status': 'error', 'message': 'Invalid folder path'})

    folders, files = [], []
    for item in os.listdir(full_path):
        full_item = os.path.join(full_path, item)
        if os.path.isdir(full_item):
            folders.append(item)
        elif os.path.isfile(full_item):
            files.append(item)

    return jsonify({'status': 'ok', 'folders': folders, 'files': files})

@folders_api.route('/api/folder/delete', methods=['POST'])
def delete_folder():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    folder = request.form.get('folder', '').strip()
    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_path = os.path.normpath(os.path.join(base_path, folder))

    if not full_path.startswith(base_path) or not os.path.isdir(full_path):
        return jsonify({'status': 'error', 'message': 'Invalid folder path'})

    shutil.rmtree(full_path)
    return jsonify({'status': 'ok'})