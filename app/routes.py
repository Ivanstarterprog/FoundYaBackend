from flask import Blueprint, request, jsonify, send_from_directory, current_app
from werkzeug.utils import secure_filename
from .models import Image
from .extensions import db
from .utils import allowed_file
import os

bp = Blueprint('api', __name__)

@bp.route('/images/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify(error="Ты мне файл то дай, лээээ"), 400
    
    file = request.files['file']
    
    if file.filename == '':
        return jsonify(error="Лэээ, где файл?"), 400

    if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
        return jsonify(error="Лэээ, файл нельзя такой"), 400
    
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{os.urandom(8).hex()}_{filename}"
        upload_folder = current_app.config['UPLOAD_FOLDER']
        file.save(os.path.join(upload_folder, unique_filename))
        
        new_image = Image(filename=unique_filename) 
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify(
            image_id=new_image.id,
            url=f"/api/uploads/{unique_filename}"  # Возвращаем URL
        ), 201

@bp.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return jsonify(url=f"/api/uploads/{image.filename}")  # Возвращаем URL

@bp.route('/uploads/<filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory(
        current_app.config['UPLOAD_FOLDER'],
        filename
    )