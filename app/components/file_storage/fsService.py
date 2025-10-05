from time import time
import flask, os, hashlib
from backend.app.components.file_storage.fsConfig import *
from backend.app.app import db
from backend.app.database.models import FileBlob

def fs_post(file):
    """
    method for uploading files into file storage
    """
    data = file.read()
    file_hash = hashlib.sha256(data+bytes(str(time()), 'utf-8')).hexdigest()

    # Build file path using the hash as filename
    save_path = os.path.join(BLOBS_DIR, file_hash)


    # Save file if it doesn't already exist
    os.makedirs(BLOBS_DIR, exist_ok=True)
    if not os.path.exists(save_path):
        with open(save_path, 'wb+') as f:
            f.write(data)

    fblob = FileBlob(file_hash=file_hash, file_path=save_path)
    db.session.add(fblob)
    db.session.commit()
    return file_hash

def fs_get(file_hash):
    fblob = FileBlob.query.get(file_hash)
    if not fblob:
        return

    file_path = fblob.file_path

    if os.path.isfile(file_path):
        return file_path