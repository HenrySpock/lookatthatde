# forms.py 
# Import necessary modules and classes for Flask-WTF forms.
from flask_wtf import FlaskForm 
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, HiddenField, RadioField, SelectField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
# Import Flask-Login's current_user to get the current logged-in user's data.
from flask_login import current_user
# Import Users model to interact with the user database table.
from models import Users 

# Define a form for sending messages.
class MessageForm(FlaskForm):
    """Form for adding/editing messages."""
    text = TextAreaField('text', validators=[DataRequired()])

# Define a form for user registration.
class RegistrationForm(FlaskForm):
    # Fields for user details.
    # Basic validations are added such as length checks and data requirements.
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')
    # HiddenField to identify the form type.
    form_type = HiddenField(default="register")

# Define a form for user login.
class LoginForm(FlaskForm):
    username_or_email = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Login')
    form_type = HiddenField(default="login")

# Define a form for editing user profile.
class EditProfileForm(FlaskForm):
    first_name = StringField('First Name', validators=[DataRequired(), Length(max=50)])
    last_name = StringField('Last Name', validators=[DataRequired(), Length(max=50)])
    username = StringField('Username', validators=[DataRequired(), Length(min=4, max=25)])
    email = StringField('Email Address', validators=[DataRequired(), Email()]) 
    submit = SubmitField('Update Profile')

    # Custom validators to ensure the username and email aren't taken by another user.
    def validate_username(self, username):
        if username.data != current_user.username:
            user = Users.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError('Username is already in use. Please choose a different one.')

    def validate_email(self, email):
        if email.data != current_user.email:
            user = Users.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email is already in use. Please choose a different one.')

    def validate_current_password(self, current_password):
        if not current_user.check_password(current_password.data):
            raise ValidationError('The current password is incorrect.')

# Define a form for changing user password.
class ChangePasswordForm(FlaskForm):
    current_password = PasswordField('Current Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired(), Length(min=6)])
    confirm_new_password = PasswordField('Confirm New Password', validators=[DataRequired(), EqualTo('new_password')])
    submit = SubmitField('Update Password')

# Define a form for user support or feedback.
class SupportForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    content = TextAreaField('Briefly tell us what\'s on your mind:', validators=[DataRequired()])
    submit = SubmitField('Submit')

# Define a form for creating image lists.
class CreateListForm(FlaskForm):
    # list_name = StringField('List Name:', validators=[DataRequired()])
    list_name = StringField('List Name:', validators=[DataRequired(), Length(max=80)])
    core_list = RadioField('Make a core list?', choices=[('yes', 'Yes'), ('no', 'No')], default='no')
    # category_name = SelectField('Choose existing category')
    category_name = SelectField('Choose existing category', choices=[('', '-- Choose existing or enter new --')])
    new_category = StringField('Or enter new category')
    submit = SubmitField('Create')

# Define a form for editing the name of an image list.
class EditListNameForm(FlaskForm):
    list_name = StringField('List Name', validators=[DataRequired(), Length(max=80)])
    submit = SubmitField('Save List Name?')
 