from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    streak = db.Column(db.Integer, default=0)
    last_login = db.Column(db.DateTime, default=datetime.utcnow)

    # New fields
    progress = db.Column(db.Integer, default=0)
    xp = db.Column(db.Integer, default=0)
    badges = db.Column(db.Text, default='[]')  # Store JSON string list
    activities = db.Column(db.Text, default='[]')  # Store JSON string list
    join_date = db.Column(db.DateTime, default=datetime.utcnow)
    profile_image_url = db.Column(db.String(300), nullable=True)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.streak = 0
        self.last_login = datetime.utcnow()
        self.progress = 0
        self.xp = 0
        self.badges = json.dumps([])  # Store list as string
        self.activities = json.dumps([])
        self.join_date = datetime.utcnow()
        self.profile_image_url = None
