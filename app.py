from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Users, ImageList
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, current_user
# from forms import RegistrationForm, LoginForm
from flask_mail import Mail, Message
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect

from routes.user_routes import user_routes, mail
from routes.list_routes import list_routes
from routes.image_routes import image_routes

# from flickr_service import fetch_image_urls
from flickr_service import fetch_images

from dotenv import load_dotenv
load_dotenv()

import os
api_key = os.environ.get("FLICKR_API_KEY")

import logging
logging.basicConfig(level=logging.DEBUG)

app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kodai:ronan@localhost/lookatthat'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://kodai:ronan@localhost/lookatthat_test'
app.debug = True
app.config['SECRET_KEY'] = 'IS_VERY_SECRET'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False   

csrf = CSRFProtect(app)

app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(list_routes, url_prefix='/lists')
app.register_blueprint(image_routes, url_prefix='/images')

login_manager = LoginManager(app)
login_manager.login_view = 'reg_log'

toolbar = DebugToolbarExtension(app)

API_KEY = "6cf94f30f65417266f15e2a31107b331"

WTF_CSRF_CHECK_DEFAULT = True
WTF_CSRF_HEADERS = ["X-CSRFToken", "X-CSRF-TOKEN"]

# Mail settings
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'mhenrytillman@gmail.com'
app.config['MAIL_PASSWORD'] = 'ijehagktvqxqmxbp'  # Replace 'YOUR_APP_PASSWORD' with the app password you generated
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
 
mail.init_app(app)

if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug=True, host='0.0.0.0')

print('app debug: ', app.debug)

db.init_app(app)
print("Connected to the database:", app.config['SQLALCHEMY_DATABASE_URI'])
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(user_id):
    return Users.query.get(int(user_id))

@app.route('/testSession')
def test_session():
    return str(dict(session))

@app.route('/')
def home(): 
    all_lists = ImageList.query.order_by(ImageList.list_id.desc()).all()
    return render_template('home.html', all_lists=all_lists, current_user=current_user)

@app.route('/about')
def about():
    return render_template('about.html')
    
if __name__ == '__main__':
    app.run(debug=True, port=5000)
 