from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey, Integer, String, Column
from sqlalchemy.orm import relationship
from flask_login import UserMixin
import bcrypt 

db = SQLAlchemy()

class Users(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    first_name = db.Column(db.String(80), nullable=True)
    last_name = db.Column(db.String(80), nullable=True)
    lists_created = db.relationship('ImageList', backref='creator', lazy=True)

    def set_password(self, password):
        self.password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password_hash.encode('utf-8'))

class ListCategory(db.Model):
    category_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=True)
    image_lists = db.relationship('ImageList', backref='category', lazy=True)

# Here is where we are 
class ImagePosition(db.Model):
    __tablename__ = 'image_position'
    
    id = db.Column(db.Integer, primary_key=True)
    # image_id = db.Column(db.Integer, db.ForeignKey('image.image_id', ondelete='CASCADE'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id', onupdate='CASCADE', ondelete='CASCADE'), nullable=False)
    list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id', ondelete='CASCADE'), nullable=False)
    position = db.Column(db.Integer, nullable=False)

    # Relationships 
    list = db.relationship('ImageList', backref='list_image_positions', lazy=True)

    def __init__(self, image_id, list_id, position):
        self.image_id = image_id
        self.list_id = list_id
        self.position = position
         
class ImageList(db.Model):
    list_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.Text, nullable=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    category_id = db.Column(db.Integer, db.ForeignKey('list_category.category_id'), nullable=True)  
    core_list = db.Column(db.Boolean, default=False)
    images = db.relationship('Image', backref='image_list', lazy=True, cascade="all, delete-orphan")
    
    # New relationship for fields
    fields = db.relationship('Field', backref='image_list', lazy=True, cascade="all, delete-orphan")

class Image(db.Model):
    image_id = db.Column(db.Integer, primary_key=True)
    list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id'), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(80), nullable=False)
    field_data = db.relationship('FieldData', backref='image', lazy=True, cascade="all, delete-orphan") 
    image_positions = db.relationship('ImagePosition', backref='image', cascade="all, delete-orphan")
    
class UserImage(db.Model):
    user_image_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    name = db.Column(db.String(80), nullable=True)
    description = db.Column(db.Text, nullable=True)
    is_custom_added = db.Column(db.Boolean, nullable=False)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user_email = db.Column(db.String(100), nullable=False)
    content = db.Column(db.String(250))
    # For the /report route:
    list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id'))
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)  # either 'text' or 'number'
    # list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id')) 
    list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id', ondelete='CASCADE'))
      
class FieldData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id', ondelete='CASCADE'), nullable=False)  
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id', ondelete='CASCADE'), nullable=False)
    value = db.Column(db.String(255), nullable=True)
  
