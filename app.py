#app.py

# Standard Library Imports
import os
import logging

# Third-Party Library Imports
# Flask and its extensions
from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, current_user
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from dotenv import load_dotenv  # To load environment variables from .env file

# Application Modules
from models import db, Users, ImageList  # Database models
from routes.user_routes import user_routes, mail  # User-related routes
from routes.list_routes import list_routes  # Image list-related routes
from routes.image_routes import image_routes  # Image-related routes
from flickr_service import fetch_images  # Service for fetching images from Flickr

# Load environment variables
load_dotenv()

# Configure logging to output debug-level logs
logging.basicConfig(level=logging.DEBUG)

# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Allow Cross-Origin Resource Sharing for the app
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')  # Secret key for sessions and CSRF protection
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('SQLALCHEMY_DATABASE_URI')  # Database URI
app.debug = True  # Enable debug mode
app.config['TEMPLATES_AUTO_RELOAD'] = True  # Automatically reload templates if changed
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  # Disable interception of redirects by the debug toolbar

# CSRF protection setup
csrf = CSRFProtect(app)

# Registering blueprints for routes
app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(list_routes, url_prefix='/lists')
app.register_blueprint(image_routes, url_prefix='/images')

# Setup Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'reg_log'  # Route to redirect to if user needs to login

# Setup debug toolbar
toolbar = DebugToolbarExtension(app)

# Constants
API_KEY = os.environ.get("FLICKR_API_KEY")  # Fetch the API key for Flickr from environment

# CSRF configuration
WTF_CSRF_CHECK_DEFAULT = True
WTF_CSRF_HEADERS = ["X-CSRFToken", "X-CSRF-TOKEN"]

# Mail Settings - setting up email configurations from environment variables
app.config['MAIL_SERVER'] = os.environ.get('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.environ.get('MAIL_PORT', 465))
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = os.environ.get('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.environ.get('MAIL_USE_SSL') == 'True'
mail.init_app(app)  # Initialize Flask-Mail with app settings

# This block is run if the script is started directly and not imported
if __name__ == '__main__':
    app.jinja_env.auto_reload = True  # Enable jinja template auto-reload
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')  # Start the Flask development server

# Print statements for debugging and information
print('app debug: ', app.debug)
db.init_app(app)  # Initialize SQLAlchemy with app settings
print("Connected to the database:", app.config['SQLALCHEMY_DATABASE_URI'])
migrate = Migrate(app, db)  # Initialize Flask-Migrate for database migrations

# Load user callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

# Test route for checking session data
@app.route('/testSession')
def test_session():
    return str(dict(session))

# Home route - displays all image lists
@app.route('/')
def home():
    all_lists = ImageList.query.order_by(ImageList.list_id.desc()).all()
    return render_template('home.html', all_lists=all_lists, current_user=current_user)

# About route - displays about page
@app.route('/about')
def about():
    return render_template('about.html')

# This block is a redundancy and should be removed
# if __name__ == '__main__':
#     app.run(debug=True, port=5000)
