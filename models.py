from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from sqlalchemy.dialects.mysql import JSON

db = SQLAlchemy()

class Todo(db.Model):
    __tablename__ = 'todos'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    due_date = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    priority = db.Column(db.String(20))
    status = db.Column(db.String(20), default='pending')
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    email = db.Column(db.String(120))
    reminder_time = db.Column(db.DateTime)
    reminder_sent = db.Column(db.Boolean, default=False)
    last_reminder_sent = db.Column(db.DateTime)
    order_index = db.Column(db.Integer, default=0)

class Category(db.Model):
    __tablename__ = 'categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(7))  # Hex color code
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))
    todos = db.relationship('Todo', backref='category', lazy=True)

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    theme = db.Column(db.String(20), default='light')  # Add this line
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    preferences = db.Column(db.Text, default='{}')  # Add this line
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)
    is_active = db.Column(db.Boolean, default=True)
    is_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    profile = db.relationship('UserProfile', backref='user', uselist=False)
    settings = db.relationship('UserSettings', backref='user', uselist=False)
    activities = db.relationship('UserActivityLog', backref='user', lazy='dynamic')
    tasks = db.relationship('Todo', backref='creator', lazy='dynamic')

class UserProfile(db.Model):
    __tablename__ = 'user_profiles'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    full_name = db.Column(db.String(100))
    bio = db.Column(db.Text)
    avatar_url = db.Column(db.String(255))
    phone = db.Column(db.String(20))
    timezone = db.Column(db.String(50), default='UTC')
    language = db.Column(db.String(10), default='en')
    notification_preferences = db.Column(JSON)
    theme_preferences = db.Column(JSON)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class UserSettings(db.Model):
    __tablename__ = 'user_settings'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    email_notifications = db.Column(db.Boolean, default=True)
    push_notifications = db.Column(db.Boolean, default=True)
    daily_digest = db.Column(db.Boolean, default=False)
    weekly_summary = db.Column(db.Boolean, default=True)
    task_reminder_advance = db.Column(db.SmallInteger, default=30)
    default_task_view = db.Column(db.Enum('list', 'grid', 'calendar'), default='list')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

class UserActivityLog(db.Model):
    __tablename__ = 'user_activity_log'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    activity_type = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)