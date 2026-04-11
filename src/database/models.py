from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(100), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    created_at = db.Column(db.DateTime)

    tasks = db.relationship('Task', backref='user', lazy=True)
    files = db.relationship('File', backref='user', lazy=True)

class Task(db.Model):
    __tablename__ = 'Tasks'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'), nullable=False)
    title = db.Column(db.String(200))
    description = db.Column(db.Text)
    deadline = db.Column(db.DateTime)
    priority = db.Column(db.String(20))  # Low, Medium, High
    status = db.Column(db.String(50))    # Pending, Completed, Overdue
    reminder_minutes = db.Column(db.Integer, default=0)  # Nhắc nhở bao nhiêu phút trước deadline
    created_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)

    notifications = db.relationship('Notification', backref='task', lazy=True)

class Notification(db.Model):
    __tablename__ = 'Notifications'
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('Tasks.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    message = db.Column(db.String(200))
    notify_time = db.Column(db.DateTime)

class File(db.Model):
    __tablename__ = 'Files'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('Users.id'))
    file_type = db.Column(db.String(50))  # JSON, CSV
    created_at = db.Column(db.DateTime)
    path = db.Column(db.String(200))
