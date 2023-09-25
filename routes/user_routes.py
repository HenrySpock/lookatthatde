from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import Users, db, Feedback
from flask_mail import Mail, Message

mail = Mail()

user_routes = Blueprint('user_routes', __name__)

# Register or Login a user: 
@user_routes.route('/regLog', methods=['GET', 'POST'])
def reg_log():
    reg_form = RegistrationForm()
    login_form = LoginForm()

    # Checking if it's a registration attempt
    if reg_form.validate_on_submit() and reg_form.form_type.data == "register":
        print("Form is validated for registration...")
        try:
            user = Users(
                username=reg_form.username.data,
                email=reg_form.email.data,
                first_name=reg_form.first_name.data,
                last_name=reg_form.last_name.data
            )
            print(f"Adding user: {user.username}, {user.email}")
            user.set_password(reg_form.password.data)
            db.session.add(user)
            db.session.commit()
            flash('Successfully registered! Please login.', 'success')
        except Exception as e:
            print("Error during registration:", str(e))
            flash('Error during registration. Please try again.', 'danger')

    # Checking if it's a login attempt
    elif login_form.validate_on_submit() and login_form.form_type.data == "login":
        try:
            print("Form is validated for login...")
            user_input = login_form.username_or_email.data

            if "@" in user_input:
                # treat as email
                user = Users.query.filter_by(email=user_input).first()
            else:
                # treat as username
                user = Users.query.filter_by(username=user_input).first()

            if user and user.check_password(login_form.password.data):
                # The password matches. Log the user in.
                print("Login successful!")
                # Uncomment the next line if you're using Flask-Login
                login_user(user)
                print("About to redirect to home...")
                print("Session: ", session)
                # print(str(dict(session)))

                return redirect(url_for('home'))
            else:
                flash('Invalid credentials. Please try again.', 'danger')
        except Exception as e:
            print("Error during login:", e)
    else:
        print("Form not validated:", reg_form.errors, login_form.errors)

    return render_template('regLog.html', reg_form=reg_form, login_form=login_form)

# Logout current user: 
@user_routes.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

# Show the current user's profile:  
@user_routes.route('/profile')
@login_required
def user_profile():
    return render_template('user_profile.html', user=current_user)

# Update user's profile:
@user_routes.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        print("Inside edit_profile route")
        current_user.first_name = form.first_name.data
        current_user.last_name = form.last_name.data
        current_user.username = form.username.data
        current_user.email = form.email.data
        print("Form errors:", form.errors)
        # Don't allow direct password change here. Ideally, create another route for changing the password
        try:
            db.session.commit()
        except Exception as e:
            print("Error during database commit:", e)
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('user_routes.user_profile'))
    else:
        print("Form validation errors:", form.errors)
    return render_template('edit_profile.html', form=form)

# Change Password 
@user_routes.route('/profile/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.check_password(form.current_password.data):
            current_user.set_password(form.new_password.data)
            db.session.commit()
            flash('Your password has been updated!', 'success')
            return redirect(url_for('user_routes.user_profile'))
        else:
            flash('Incorrect current password.', 'danger')
    return render_template('change_password.html', form=form)

# Delete user's profile:
@user_routes.route('/profile/delete', methods=['POST'])
@login_required
def delete_profile():
    db.session.delete(current_user)
    db.session.commit()
    flash('Your profile has been deleted!', 'success')
    logout_user()
    return redirect(url_for('home'))

@user_routes.route('/support', methods=['GET', 'POST'])
def support():
    form = SupportForm()

    # pre-populate form fields if user is logged in
    if current_user.is_authenticated:
        form.name.data = current_user.username
        form.email.data = current_user.email

    if form.validate_on_submit():
        feedback = Feedback(
            user_id=current_user.id if current_user.is_authenticated else None,
            user_email=form.email.data,
            content=form.content.data
        )
        db.session.add(feedback)
        db.session.commit()
 
        try:
            email_body = f"""
            User:
            {form.name.data}

            Email:
            {form.email.data}

            Feedback:
            {form.content.data}
            """
            # Construct and send the email message:
            msg = Message('New Feedback from ' + form.name.data, 
                          sender=form.email.data, 
                          recipients=[current_app.config['MAIL_USERNAME']])
            # msg.body = form.content.data
            msg.body = email_body
            mail.send(msg)
            flash('Your feedback has been sent!', 'success')
        except Exception as e:
            flash(f'There was an error sending the email: {e}', 'danger')
            # You can also log the error for debugging

        return redirect(url_for('about'))

    return render_template('support.html', form=form)

