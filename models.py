from flask_sqlalchemy import SQLAlchemy
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
    # description = db.Column(db.Text, nullable=True)
    # year = db.Column(db.String(50), nullable=True) 
    # num_pieces = db.Column(db.Integer, nullable=True)
    # cat_number = db.Column(db.String(100), nullable=True)
    # country_of_origin = db.Column(db.String(100), nullable=True)
    # manufacturer = db.Column(db.String(100), nullable=True) 
    # custom_fields = db.Column(db.JSON) 
    field_data = db.relationship('FieldData', backref='image', lazy=True, cascade="all, delete-orphan")

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

class Field(db.Model):
    __tablename__ = 'fields'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    type = db.Column(db.String)  # either 'text' or 'number'
    list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id'))

class FieldData(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    field_id = db.Column(db.Integer, db.ForeignKey('fields.id'), nullable=False)
    image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
    value = db.Column(db.String(255), nullable=True)
      