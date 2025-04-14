import os
import base64
import mimetypes

from config import Config
from utils.session import get_current_user
from flask import Blueprint, request, jsonify, send_file

files_api = Blueprint('files_api', __name__)

@files_api.route('/api/files/upload', methods=['POST'])
def upload_file():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    folder = request.form.get('folder', '')
    filename = request.form.get('filename')
    content_b64 = request.form.get('content')

    if not filename or not content_b64:
        return jsonify({'status': 'error', 'message': 'Missing filename or content'})

    mimetype, _ = mimetypes.guess_type(filename)
    if mimetype not in ['image/png', 'image/jpeg']:
        return jsonify({'status': 'error', 'message': 'Invalid file type'})

    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_folder = os.path.normpath(os.path.join(base_path, folder))
    if not full_folder.startswith(base_path):
        return jsonify({'status': 'error', 'message': 'Invalid folder'})

    os.makedirs(full_folder, exist_ok=True)
    filepath = os.path.join(full_folder, filename)

    try:
        decoded = base64.b64decode(content_b64)
        if len(decoded) > 1_000_000:
            return jsonify({'status': 'error', 'message': 'File too large'})
        with open(filepath, 'wb') as f:
            f.write(decoded)
    except Exception as e:
        return jsonify({'status': 'error', 'message': f'Error writing file: {str(e)}'})

    return jsonify({'status': 'ok'})

@files_api.route('/api/files/delete', methods=['POST'])
def delete_file():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    filename = request.form.get('filename')
    folder = request.form.get('folder', '')
    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_path = os.path.normpath(os.path.join(base_path, folder, filename))

    if not full_path.startswith(base_path) or not os.path.isfile(full_path):
        return jsonify({'status': 'error', 'message': 'Invalid file path'})

    os.remove(full_path)
    return jsonify({'status': 'ok'})

@files_api.route('/api/files/download', methods=['POST'])
def download_file():
    user = get_current_user()
    if not user:
        return jsonify({'status': 'error', 'message': 'Not authenticated'})

    filename = request.form.get('filename')
    folder = request.form.get('folder', '')
    base_path = os.path.join(Config.UPLOAD_FOLDER, user[3])
    full_path = os.path.normpath(os.path.join(base_path, folder, filename))

    if not full_path.startswith(base_path) or not os.path.isfile(full_path):
        return jsonify({'status': 'error', 'message': 'Invalid file path'})

    return send_file(full_path, as_attachment=True, download_name=filename)