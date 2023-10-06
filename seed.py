# This is the original seed.py file, however, for the future, using dblookatthatback.sql directly is the preferred method for reinitializing the database. 
from app import app, db
from tableSeeds import seed_users, seed_image_lists, seed_categories   

with app.app_context():
    db.drop_all()
    db.create_all()
    seed_categories() # Call the function to seed categories
    seed_users() # Call the function to seed users
    seed_image_lists() # Call the function to seed images and lists 
