import os
import uuid
from datetime import datetime

from PIL import Image
from flask import current_app
from werkzeug.utils import secure_filename


def allowed_file(filename: str) -> bool:
    ext = filename.rsplit(".", 1)[-1].lower()
    return ext in current_app.config["ALLOWED_EXTENSIONS"]


def save_item_image(file):
    if not file or not allowed_file(file.filename):
        return None

    now = datetime.now()
    subfolder = os.path.join(str(now.year), f"{now.month:02d}")
    save_dir = os.path.join(current_app.config["UPLOAD_FOLDER"], subfolder)
    os.makedirs(save_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower()
    file_name = f"{uuid.uuid4().hex}.{ext}"
    full_path = os.path.join(save_dir, file_name)

    img = Image.open(file)
    img = img.convert("RGB")
    img.thumbnail((1200, 1200), Image.LANCZOS)
    img.save(full_path, quality=85, optimize=True)

    file_size = os.path.getsize(full_path)
    file_path = f"/static/uploads/items/{subfolder}/{file_name}"

    return {
        "file_name": file_name,
        "file_path": file_path,
        "file_size": file_size,
    }


def delete_item_image(file_path: str) -> bool:
    abs_path = os.path.join(current_app.root_path, file_path.lstrip("/"))
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False


AVATAR_MAX_SIZE = 2 * 1024 * 1024
AVATAR_DIMENSION = (300, 300)


def save_avatar(file, user_id: int):
    if not file or not allowed_file(file.filename):
        return None
    if file.content_length and file.content_length > AVATAR_MAX_SIZE:
        return None

    save_dir = os.path.join(current_app.root_path, "static", "uploads", "avatars")
    os.makedirs(save_dir, exist_ok=True)

    filename = secure_filename(file.filename)
    ext = filename.rsplit(".", 1)[-1].lower()
    file_name = f"{user_id}.{ext}"
    full_path = os.path.join(save_dir, file_name)

    img = Image.open(file).convert("RGB")

    w, h = img.size
    side = min(w, h)
    left = (w - side) // 2
    top = (h - side) // 2
    img = img.crop((left, top, left + side, top + side))
    img = img.resize(AVATAR_DIMENSION, Image.LANCZOS)
    img.save(full_path, quality=90, optimize=True)

    file_path = f"/static/uploads/avatars/{file_name}"
    return {"file_name": file_name, "file_path": file_path}


def delete_avatar(file_path: str) -> bool:
    abs_path = os.path.join(current_app.root_path, file_path.lstrip("/"))
    if os.path.exists(abs_path):
        os.remove(abs_path)
        return True
    return False

