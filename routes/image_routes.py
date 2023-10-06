"""
image_routes.py

This module contains routes related to image functionalities, including
fetching images from Flickr, editing images, updating and saving edits, 
deleting images, and updating image positions in a list.
"""

# Necessary imports for Flask, Flask-WTF forms, database operations, and other utilities.
from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import ImageList, Image, ListCategory, db, Field, FieldData, ImagePosition
import requests
import re

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()  

# Get Flickr API key from environment variables
FLICKR_API_KEY = os.getenv("FLICKR_API_KEY")

def fetch_from_flickr(query):
    FLICKR_API_URL = "https://api.flickr.com/services/rest/"

    params = {
        "method": "flickr.photos.search",
        "api_key": FLICKR_API_KEY,
        "text": query,
        "format": "json",
        "nojsoncallback": 1,  # To get a clean JSON response without the function wrapper
        "per_page": 32,  # Number of images returned from search
    }

    response = requests.get(FLICKR_API_URL, params=params)
    response_json = response.json()
    print(response_json)

    images = []
    for photo in response_json['photos']['photo']:
        # Construct the URL based on the data from the API
        url = f"https://farm{photo['farm']}.staticflickr.com/{photo['server']}/{photo['id']}_{photo['secret']}.jpg"
        images.append({
            "url": url,
            "title": photo.get("title", "")
        })

    return images


# Blueprint definition for image routes
image_routes = Blueprint('image_routes', __name__) 

# Error handler for unexpected exceptions in image routes
@image_routes.app_errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    print(str(e))
    return str(e), 500

# Route to search for images based on a given list ID
@image_routes.route('/image_search/<int:list_id>', methods=['GET'])
def image_search(list_id):
    image_list = ImageList.query.get_or_404(list_id)
    print('On image_search, list_id: ', list_id)
    
    error = request.args.get('error')
    if error == 'empty_url':
        flash("Please enter a URL.")
    elif error == 'invalid_url':
        flash("Please enter a valid URL.")
        
    return render_template('image_search.html', image_list=image_list, list_id=list_id, search_performed=False)

# Route to display fetched images based on a search query or a manual URL
@image_routes.route('/image_response/<int:list_id>', methods=['GET'])
def image_response(list_id):
    query = request.args.get('search_query')
    manual_image_url = request.args.get('manual_image_url')
    
    print('on image_response, list_id: ', list_id)
    print('on image_response, request.args: ', request.args)

    if manual_image_url:
        # Redirect to edit_image with the manual_image_url
        # return redirect(url_for('image_routes.edit_image', image_url=manual_image_url))
        return redirect(url_for('image_routes.edit_image', list_id=list_id, selected_image_url=manual_image_url))


    elif query:
        if not query or query.strip() == "":
            flash("Please enter a valid search term.")
            return redirect(url_for('image_routes.image_search', list_id=list_id))
        
        images = fetch_from_flickr(query)
        return render_template('image_response.html', images=images, list_id=list_id, search_performed=True)
    
    else:
        flash("Please enter a valid search term or a valid image URL.")
        return redirect(url_for('image_routes.image_search', list_id=list_id))

# Route to edit a specific image from a list
@image_routes.route('/edit_image/<int:list_id>/<int:image_id>', methods=['GET'])
def edit_image(list_id, image_id):
    # Directly fetch the image using the image_id
    image = Image.query.get_or_404(image_id)

    # Fetch the associated fields for this image list
    fields = Field.query.filter_by(list_id=list_id).all()

    # Fetch values of the fields for this image
    field_values = {data.field_id: data.value for data in FieldData.query.filter_by(image_id=image_id).all()}

    return render_template('edit_image.html', image=image, fields=fields, field_values=field_values, list_id=list_id, image_id=image_id)

# Route to save an image to a specific list
@image_routes.route('/save_image/<int:list_id>', methods=['POST'])
def save_image(list_id):
    data = request.json
    image_url = data['imageUrl']
    image_name = data['imageName']

    # Determine the next position for the image in the list
    last_position = db.session.query(db.func.max(ImagePosition.position)).filter_by(list_id=list_id).scalar()
    next_position = (last_position or 0) + 1  # If no images, start with 1

    try:
        new_image = Image(list_id=list_id, image_url=image_url, name=image_name)
        db.session.add(new_image)
        db.session.flush()  # Flush so that we can get new_image.image_id

        new_image_position = ImagePosition(image_id=new_image.image_id, list_id=list_id, position=next_position)
        db.session.add(new_image_position)

        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500

    flash("Image saved successfully!")
    return jsonify(success=True)

# Route to update a specific image
@image_routes.route('/update_image/<int:image_id>', methods=['GET', 'POST'])
@login_required
def update_image(image_id):
    image = Image.query.get_or_404(image_id)
    list_id = image.list_id

    # Get user-defined fields for the list this image belongs to
    fields = Field.query.filter_by(list_id=list_id).all()

    # For a POST request, update the image and its field data
    if request.method == 'POST':
        # Update image attributes here, like name and image_url
        image.name = request.form.get('name', image.name)
        image.image_url = request.form.get('image_url', image.image_url)
        
        # Save or update field data
        for field in fields:
            value = request.form.get(f"field_{field.id}")
            if value:
                field_data = FieldData.query.filter_by(image_id=image_id, field_id=field.id).first()
                if field_data:
                    field_data.value = value
                else:
                    new_field_data = FieldData(field_id=field.id, image_id=image_id, value=value)
                    db.session.add(new_field_data)
        
        try:
            db.session.commit()
            return redirect(url_for('list_routes.list_details', list_id=list_id))
        except Exception as e:
            db.session.rollback()
            flash(f"Error updating image: {str(e)}", "danger")
            return render_template('update_image.html', image=image, fields=fields), 500

    # For a GET request, just display the form with current data
    return render_template('update_image.html', image=image, fields=fields)

# Route to save edits of a specific image
@image_routes.route('/save_edits/<int:list_id>/<int:image_id>', methods=['POST'])
def save_edits(list_id, image_id):
    print("save_edits form: ", request.form)
    # Fetch the image to be updated
    image = Image.query.get_or_404(image_id)
    if not image:
        flash("Image not found!")
        return redirect(url_for('list_routes.list_details', list_id=list_id))

    # Update the image details
    image.name = request.form.get('name', image.name)
    image.image_url = request.form.get('image_url', image.image_url)

    # Fetch all the associated fields for this image list
    fields = Field.query.filter_by(list_id=list_id).all()

    for field in fields:
        field_name = field.name
        # field_value = request.form.get(field_name)
        field_value = request.form.get(f"field_{field.id}")
        
        # Check if the field data for this field and image already exists
        existing_field_data = FieldData.query.filter_by(field_id=field.id, image_id=image_id).first()

        if existing_field_data:
            # Update the value if it already exists
            existing_field_data.value = field_value
        else:
            # Or create a new field data entry if it doesn't exist
            new_field_data = FieldData(field_id=field.id, image_id=image_id, value=field_value)
            db.session.add(new_field_data)
    
    try:
        db.session.commit()
        flash("Image edits saved successfully!")
    except Exception as e:
        db.session.rollback()
        print(e)  # print full traceback for debugging
        flash(f"Error saving edits: {str(e)}", "error")

    
    return redirect(url_for('list_routes.list_details', list_id=list_id))

# Route to delete a specific image from a list
@image_routes.route('/delete_image/<int:list_id>/<int:image_id>', methods=['GET'])
@login_required
def delete_image(list_id, image_id):
    image = Image.query.get_or_404(image_id)

    # Fetch the associated ImagePosition
    img_position = ImagePosition.query.filter_by(image_id=image_id).first()

    if img_position:
        # Find all subsequent ImagePositions for the same list
        subsequent_positions = ImagePosition.query.filter(
            ImagePosition.list_id == img_position.list_id,
            ImagePosition.position > img_position.position
        ).order_by(ImagePosition.position).all()

        # Decrement their position value
        for position in subsequent_positions:
            position.position -= 1
        
        # Delete the ImagePosition for the image
        db.session.delete(img_position)

    # Delete associated field data for the image
    FieldData.query.filter_by(image_id=image_id).delete()

    # Delete the image itself
    db.session.delete(image)

    try:
        db.session.commit()
        flash('Image deleted successfully!')
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting image: {str(e)}", "error")

    return redirect(url_for('list_routes.list_details', list_id=list_id))

# Route to update image positions in a specific list
@image_routes.route('/update_image_positions', methods=['POST'])
def update_image_positions():
    print('Attempting to update route.')
    try:
        data = request.json

        if not isinstance(data, dict):
            raise ValueError("Data should be a dictionary with image ID as keys and position as values.")

        for image_id, position in data.items():
            image_position = ImagePosition.query.filter_by(image_id=image_id).first()
            if image_position:
                image_position.position = position

        db.session.commit()
        return jsonify(success=True)

    except ValueError as ve:
        return jsonify(success=False, error=str(ve)), 400  # Bad request for invalid data format
    except Exception as e:
        db.session.rollback()
        return jsonify(success=False, error=str(e)), 500

# Route to view a single image.
@image_routes.route('/view_full_image/<int:image_id>')
def view_full_image(image_id):
    image = Image.query.get(image_id)
    if not image:
        flash('Image not found!')
        return redirect(url_for('list_routes.list_details'))

    return render_template('full_image.html', image=image)
