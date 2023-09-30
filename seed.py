# from app import app, db
# from models import seed_users  # Import the seed_users function

# with app.app_context():
#     db.drop_all()
#     db.create_all()
#     seed_users()  # Call the function to seed users

from app import app, db
from tableSeeds import seed_users, seed_image_lists, seed_categories  # Import the functions from the new file 
from back_populate import back_populate

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_categories()
    seed_users() # Call the function to seed users
    seed_image_lists() # Call the function to seed images and lists
    back_populate() # Add image_position data for all images
