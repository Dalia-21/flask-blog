from datetime import datetime
from app import db

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String())
    title = db.Column(db.String())
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return '<Title: {}>\nPost {}'.format(self.title, self.body)
