from flask import Flask, render_template, flash, redirect, url_for, session, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import db, Users, ImageList
from flask_debugtoolbar import DebugToolbarExtension
from flask_login import LoginManager, login_user, logout_user, current_user
# from forms import RegistrationForm, LoginForm
from flask_mail import Mail, Message
from flask_cors import CORS

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
app.debug = True
app.config['SECRET_KEY'] = 'IS_VERY_SECRET'
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False  

app.register_blueprint(user_routes, url_prefix='/user')
app.register_blueprint(list_routes, url_prefix='/lists')
app.register_blueprint(image_routes, url_prefix='/images')

login_manager = LoginManager(app)
login_manager.login_view = 'reg_log'

toolbar = DebugToolbarExtension(app)

API_KEY = "6cf94f30f65417266f15e2a31107b331"

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

# ADMIN ROUTES 
@app.route('/testSession')
def test_session():
    return str(dict(session))

# *** 
@app.route('/')
def home():
    return render_template('home.html', current_user=current_user) 

@app.route('/about')
def about():
    return render_template('about.html')

# @app.route('/regLog', methods=['GET', 'POST'])
# def reg_log():
#     reg_form = RegistrationForm()
#     login_form = LoginForm()

#     # Checking if it's a registration attempt
#     if reg_form.validate_on_submit() and reg_form.form_type.data == "register":
#         print("Form is validated for registration...")
#         try:
#             user = Users(
#                 username=reg_form.username.data,
#                 email=reg_form.email.data,
#                 first_name=reg_form.first_name.data,
#                 last_name=reg_form.last_name.data
#             )
#             print(f"Adding user: {user.username}, {user.email}")
#             user.set_password(reg_form.password.data)
#             db.session.add(user)
#             db.session.commit()
#             flash('Successfully registered! Please login.', 'success')
#         except Exception as e:
#             print("Error during registration:", str(e))
#             flash('Error during registration. Please try again.', 'danger')

#     # Checking if it's a login attempt
#     elif login_form.validate_on_submit() and login_form.form_type.data == "login":
#         try:
#             print("Form is validated for login...")
#             user_input = login_form.username_or_email.data

#             if "@" in user_input:
#                 # treat as email
#                 user = Users.query.filter_by(email=user_input).first()
#             else:
#                 # treat as username
#                 user = Users.query.filter_by(username=user_input).first()

#             if user and user.check_password(login_form.password.data):
#                 # The password matches. Log the user in.
#                 print("Login successful!")
#                 # Uncomment the next line if you're using Flask-Login
#                 login_user(user)
#                 print("About to redirect to home...")
#                 print("Session: ", session)
#                 # print(str(dict(session)))

#                 return redirect(url_for('home'))
#             else:
#                 flash('Invalid credentials. Please try again.', 'danger')
#         except Exception as e:
#             print("Error during login:", e)
#     else:
#         print("Form not validated:", reg_form.errors, login_form.errors)

#     return render_template('regLog.html', reg_form=reg_form, login_form=login_form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('home'))

@app.route('/ourLists')
def our_lists():
    return render_template('ourLists.html')

@app.route('/yourLists')
def your_lists():
    return render_template('yourLists.html')

# @app.route('/create_list')
# def create_list():
#     return render_template('create_list.html')

@app.route('/listDetails')
def list_details():
    return render_template('listDetails.html')

@app.route('/pictureDetails')
def picture_details():
    return render_template('pictureDetails.html')

@app.route('/base')  # This route might not be directly navigated to, but added for the sake of completeness
def base():
    return render_template('base.html')

# @app.route('/imageResponse')
# def imageResponse():
#     image_urls = fetch_image_urls(api_key="6cf94f30f65417266f15e2a31107b331", search_query="P-1 Hawk (Curtiss Model 34)", num_images=30)
#     return render_template('imageResponse.html', image_urls=image_urls)

# @app.route('/imageResponse')
# def imageResponse():
#     images = fetch_images(api_key="6cf94f30f65417266f15e2a31107b331", search_query="Springbok Puzzle", num_images=30)
#     print('Images: ', images)
#     return render_template('imageResponse.html', images=images)

# @app.route('/imageResponse')
# def imageResponse():
#     images = fetch_images(api_key=api_key, search_query="Gazelle", num_images=30)
#     print('Images: ', images)
#     return render_template('imageResponse.html', images=images)

@app.route('/allLists')
def allLists():
    image_lists = ImageList.query.all()
    return render_template('allLists.html', image_lists=image_lists)

@app.route('/singleList/<int:list_id>')
def singleList(list_id):
    image_list = ImageList.query.get_or_404(list_id)
    return render_template('singleList.html', image_list=image_list)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
 