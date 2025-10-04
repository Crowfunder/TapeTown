from flask import Blueprint, request, current_app,send_file, g, render_template, flash, redirect, url_for, jsonify, Response, session
import hashlib, os
from app.components.file_storage.fsConfig import *
from app.components.file_storage.fsService import *

bp = Blueprint('bp_fstorage', __name__, url_prefix="/api/files")
os.makedirs(BLOBS_DIR, exist_ok=True)


@bp.route(ENDPOINT_FILES, methods=['GET'])
def file_get():
    file_hash = request.args.get(DOWNLOAD_URL_PARAM)
    file_path = fs_get(file_hash)
    if not file_path:
        return 'file not found', 404

    return send_file(file_path, as_attachment=True)


@bp.route(ENDPOINT_FILES, methods=['POST'])
def file_post():
    if 'file' not in request.files:
        return {'error': 'No file part in the request'}, 400

    file = request.files['file']
    if file.filename == '':
        return {'error': 'No selected file'}, 400

    # Read file content
    data = file.read()
    file_hash = hashlib.sha256(data).hexdigest()

    # Build file path using the hash as filename
    save_path = os.path.join(BLOBS_DIR, file_hash)

    # Save file if it doesn't already exist
    if not os.path.exists(save_path):
        with open(save_path, 'wb') as f:
            f.write(data)

    return {'message': 'File saved successfully', 'sha256': file_hash}, 200