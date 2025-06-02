from app.extensions import db
from datetime import datetime
import os

class Image(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.String(50))  # Для связи с Firebase UID

    def get_path(self):
        return os.path.join('uploads', self.filename)
    
    def get_url(self, request):
        return f"{request.host_url}api/images/{self.id}"