from flask import Blueprint, request, jsonify, send_file
from werkzeug.utils import secure_filename
from .models import Image
from .extensions import db
import os

bp = Blueprint('api', __name__)

@bp.route('/images/upload', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        return jsonify(error="No file part"), 400
    
    file = request.files['file']
    user_id = request.form.get('user_id', '')
    
    if file.filename == '':
        return jsonify(error="No selected file"), 400
    
    if file:
        filename = secure_filename(file.filename)
        unique_filename = f"{user_id}_{os.urandom(8).hex()}_{filename}"
        file.save(os.path.join('uploads', unique_filename))
        
        new_image = Image(filename=unique_filename, user_id=user_id)
        db.session.add(new_image)
        db.session.commit()
        
        return jsonify(image_id=new_image.id), 201

@bp.route('/images/<int:image_id>', methods=['GET'])
def get_image(image_id):
    image = Image.query.get_or_404(image_id)
    return send_file(image.get_path())