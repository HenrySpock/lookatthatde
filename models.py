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

# class UserList(db.Model):
#     user_list_id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
#     list_id = db.Column(db.Integer, db.ForeignKey('image_list.list_id'), nullable=False)
#     is_favorited = db.Column(db.Boolean, nullable=False)

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
     
# class FieldData(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     field_id = db.Column(db.Integer, db.ForeignKey('field.id'), nullable=False)
#     image_id = db.Column(db.Integer, db.ForeignKey('image.image_id'), nullable=False)
#     value = db.Column(db.String(255), nullable=False)

# def seed_users():
#     # Check if users already exist to avoid seeding multiple times
#     existing_user = Users.query.first()
#     if existing_user:
#         print("Users already exist. Skipping seeding.")
#         return

#     # Create a regular user
#     regular_user = Users(username='testuser', email='testuser@example.com', first_name="Testy", last_name="User")
#     regular_user.set_password('testpassword')

#     # Create an admin user
#     admin_user = Users(username='adminuser', email='adminuser@example.com', is_admin=True, first_name="Adminy", last_name="Simp")
#     admin_user.set_password('adminpassword')

#     # Add and commit the users to the database
#     db.session.add(regular_user)
#     db.session.add(admin_user)
#     db.session.commit()

#     print("Test users seeded!")

# def seed_images_and_list():
#     # Check if any images/lists already exist to avoid seeding multiple times
#     existing_list = ImageList.query.first()
#     if existing_list:
#         print("Image lists already exist. Skipping seeding.")
#         return

#     # Fetch the admin user by username
#     admin_user = Users.query.filter_by(username='adminuser').first()
#     if not admin_user:
#         print("Admin user not found. Make sure to seed users first.")
#         return

#     # Create an ImageList and associate it with the admin user
#     image_list = ImageList(
#         name='Sample Image List', 
#         description='This is a sample list of images.',
#         creator_id=admin_user.id
#     )

#     # Add the ImageList to the session (not committed yet)
#     db.session.add(image_list)
    
#     # Ensure that it's committed to get an ID for the foreign key relationships
#     db.session.commit()

#     # Now we'll create 10 images associated with this list
#     for i in range(1, 11):
#         image = Image(
#             list_id=image_list.list_id,
#             flickr_url=f'https://example.com/image{i}.jpg',  # Placeholder URLs
#             name=f'Image {i}',
#             description=f'Description for image {i}'
#         )
#         db.session.add(image)

#     # Commit the session to save the images
#     db.session.commit()

#     print("Sample image list and images seeded!")
