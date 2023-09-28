from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import ImageList, Image, ListCategory, db, Field, FieldData
import requests
import re

import os
from dotenv import load_dotenv

load_dotenv()  # Load the .env file

FLICKR_API_KEY = os.getenv("FLICKR_API_KEY")

def fetch_from_flickr(query):
    FLICKR_API_URL = "https://api.flickr.com/services/rest/"

    params = {
        "method": "flickr.photos.search",
        "api_key": FLICKR_API_KEY,
        "text": query,
        "format": "json",
        "nojsoncallback": 1,  # To get a clean JSON response without the function wrapper
        "per_page": 30,  # You can adjust this to get more or fewer images
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


# Routes 
image_routes = Blueprint('image_routes', __name__) 

@image_routes.app_errorhandler(Exception)
def handle_exception(e):
    # Log the error for debugging
    print(str(e))
    return str(e), 500

# # Add Image route
# @image_routes.route('/image_search/<int:list_id>', methods=['GET'])
# def image_search(list_id):
#     image_list = ImageList.query.get_or_404(list_id)
#     print('On image_search, list_id: ', list_id)
    
#     return render_template('image_search.html', image_list=image_list, list_id=list_id, search_performed=False)

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

# @image_routes.route('/image_response')
# def image_response(list_id):
#     query = request.args.get('search_query')
#     list_id = request.args.get('list_id')
#     # image_list = ImageList.query.get_or_404(list_id)
#     print('on image_response, list_id: ', list_id)
#     print('on image_response, request.args: ', request.args)

#     if not query or query.strip() == "":
#         flash("Please enter a valid search term.")
#         return redirect(url_for('image_routes.image_search', list_id=list_id))
     
#     images = fetch_from_flickr(query)
#     return render_template('image_response.html', image_list=image_list, images=images, list_id=list_id)

# @image_routes.route('/image_response/<int:list_id>', methods=['GET'])
# def image_response(list_id):
#     query = request.args.get('search_query')
#     manual_image_url = request.args.get('manual_image_url')
#     # You don't need the line below, as list_id is now part of the route itself
#     # list_id = request.args.get('list_id')
     
#     print('on image_response, list_id: ', list_id)
#     print('on image_response, request.args: ', request.args)

#     if not query or query.strip() == "":
#         flash("Please enter a valid search term.")
#         return redirect(url_for('image_routes.image_search', list_id=list_id))
     
#     images = fetch_from_flickr(query)
#     return render_template('image_response.html', images=images, list_id=list_id, search_performed=True)

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


# @image_routes.route('/edit_image')
# def edit_image():
#     image_url = request.args.get('image_url', '')
#     return render_template('edit_image.html', image_url=image_url)

# @image_routes.route('/edit_image/<int:list_id>', methods=['GET'])
# def edit_image(list_id):
#     selected_image_url = request.args.get('selected_image_url')
    
#     if not selected_image_url:
#         # Handle the absence of an image URL
#         flash("No image provided!")
#         return redirect(url_for('image_routes.image_search', list_id=list_id))
    
#     # Rest of the code...
    
#     return render_template('edit_image.html', image_url=selected_image_url, list_id=list_id)

# Adding field retrieval
# @image_routes.route('/edit_image/<int:list_id>/<int:image_id>', methods=['GET'])
# def edit_image(list_id, image_id):
#     selected_image_url = request.args.get('selected_image_url')
    
#     if not selected_image_url:
#         # Handle the absence of an image URL
#         flash("No image provided!")
#         return redirect(url_for('image_routes.image_search', list_id=list_id))
    
#     # Get the image details using the provided URL
#     image = Image.query.filter_by(image_url=selected_image_url).first()
#     if not image:
#         flash("Image not found!")
#         return redirect(url_for('list_routes.list_details', list_id=list_id))

#     # Fetch the associated fields for this image list
#     fields = Field.query.filter_by(list_id=list_id).all()

#     # Fetch values of the fields for this image
#     field_values = {data.field_id: data.value for data in FieldData.query.filter_by(image_id=image.image_id).all()}

#     return render_template('edit_image.html', image=image, fields=fields, field_values=field_values, list_id=list_id, image_id=image_id)
#     # return render_template('edit_image.html', image_url=selected_image_url, list_id=list_id,)

@image_routes.route('/edit_image/<int:list_id>/<int:image_id>', methods=['GET'])
def edit_image(list_id, image_id):
    # Directly fetch the image using the image_id
    image = Image.query.get_or_404(image_id)

    # Fetch the associated fields for this image list
    fields = Field.query.filter_by(list_id=list_id).all()

    # Fetch values of the fields for this image
    field_values = {data.field_id: data.value for data in FieldData.query.filter_by(image_id=image_id).all()}

    return render_template('edit_image.html', image=image, fields=fields, field_values=field_values, list_id=list_id, image_id=image_id)

    
# @image_routes.route('/save_image/<int:list_id>', methods=['POST'])
# def save_image(list_id):
#     image_url = request.form.get('image_url')
#     name = request.form.get('name')
#     # Grab other fields similarly...

#     # Create a new Image instance and add it to the database
#     new_image = Image(list_id=list_id, image_url=image_url, name=name)
#     db.session.add(new_image)
#     db.session.commit()

#     flash("Image saved successfully!")
    
#     # Redirecting to list_details for the current list
#     return redirect(url_for('list_routes.list_details', list_id=list_id))

@image_routes.route('/save_image/<int:list_id>', methods=['POST'])
def save_image(list_id):
    data = request.json
    image_url = data['imageUrl']
    image_name = data['imageName']

    # Logic to save image_url and image_name to database
    try:
        new_image = Image(list_id=list_id, image_url=image_url, name=image_name)
        db.session.add(new_image)
        db.session.commit()
    except Exception as e:
        return jsonify(success=False, error=str(e)), 500


    flash("Image saved successfully!")

    return jsonify(success=True)

@image_routes.route('/edit_fields/<int:list_id>', methods=['GET'])
def edit_fields_get(list_id):
    # Fetch the custom fields for the list
    # fields = Field.query.filter_by(list_id=list_id).all()
    fields = Field.query.filter_by(list_id=list_id).order_by(Field.name).all()

    return render_template('edit_fields.html', list_id=list_id, fields=fields)

# @image_routes.route('/edit_fields/<int:list_id>', methods=['POST'])
# def edit_fields_post(list_id):
#     print('request.form: ', request.form)
#     field_names = request.form.getlist('field_names[]')
#     field_types = request.form.getlist('field_types[]')
    
#     if len(field_names) != len(field_types):
#         print("Mismatch between field names and field types count.")
#         return "Error processing form", 400

#     for name, field_type in zip(field_names, field_types):
#         if name and field_type:  # Only save if both name and type are present
#             new_field = Field(name=name, type=field_type, list_id=list_id)
#             db.session.add(new_field)

#     try:
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print("Error during database commit: ", str(e))
#         return "Failed to update database", 500

#     return redirect(url_for('list_routes.list_details', list_id=list_id))

# @image_routes.route('/edit_fields/<int:list_id>', methods=['POST'])
# def edit_fields_post(list_id):
#     print('request.form: ', request.form)
#     fields_data = {}

#     # Iterate over all the keys in the form data
#     for key in request.form.keys():
#         match_name = re.match(r'field_name_(\d+)', key)
#         match_type = re.match(r'field_type_(\d+)', key)

#         if match_name:
#             field_id = int(match_name.group(1))
#             fields_data.setdefault(field_id, {})['name'] = request.form[key]

#         elif match_type:
#             field_id = int(match_type.group(1))
#             fields_data.setdefault(field_id, {})['type'] = request.form[key]

#     # Now, iterate over the extracted fields data and save to the database
#     for field_id, field_data in fields_data.items():
#         name = field_data.get('name')
#         field_type = field_data.get('type')

#         if name and field_type:  # Only process if both name and type are present
#             existing_field = Field.query.filter_by(id=field_id, list_id=list_id).first()
            
#             if existing_field:  # Field exists, so update it
#                 existing_field.name = name
#                 existing_field.type = field_type
#             else:  # Field does not exist, so create it
#                 new_field = Field(name=name, type=field_type, list_id=list_id)
#                 db.session.add(new_field)

#     try:
#         db.session.commit()
#     except Exception as e:
#         db.session.rollback()
#         print("Error during database commit: ", str(e))
#         return "Failed to update database", 500

#     return redirect(url_for('list_routes.list_details', list_id=list_id))

@image_routes.route('/edit_fields/<int:list_id>', methods=['POST'])
def edit_fields_post(list_id):
    print('request.form: ', request.form)
    fields_data = {}

    # Iterate over all the keys in the form data
    for key in request.form.keys():
        match_name = re.match(r'field_name_(\d+)', key)
        match_type = re.match(r'field_type_(\d+)', key)

        if match_name:
            field_id = int(match_name.group(1))
            fields_data.setdefault(field_id, {})['name'] = request.form[key]

        elif match_type:
            field_id = int(match_type.group(1))
            fields_data.setdefault(field_id, {})['type'] = request.form[key]

    # Now, iterate over the extracted fields data and save to the database
    for field_id, field_data in fields_data.items():
        name = field_data.get('name')
        field_type = field_data.get('type')

        # Check if the name is not blank and both name and type are present
        if name and name.strip() and field_type:
            existing_field = Field.query.filter_by(id=field_id, list_id=list_id).first()
            
            if existing_field:  # Field exists, so update it
                existing_field.name = name
                existing_field.type = field_type
            else:  # Field does not exist, so create it
                new_field = Field(name=name, type=field_type, list_id=list_id)
                db.session.add(new_field)

    # Handle new fields
    new_field_names = request.form.getlist('field_names[]')
    new_field_types = request.form.getlist('field_types[]')

    for name, field_type in zip(new_field_names, new_field_types):
        # Check if the name is not blank
        if name and name.strip():
            new_field = Field(name=name, type=field_type, list_id=list_id)
            db.session.add(new_field)

    # Handle deletion of fields
    delete_field_ids = request.form.getlist('delete_field_ids[]')
    print("IDs to delete:", delete_field_ids)
    for delete_id in delete_field_ids:
        field_to_delete = Field.query.get(delete_id)
        if field_to_delete:
            db.session.delete(field_to_delete)

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print("Error during database commit: ", str(e))
        return "Failed to update database", 500

    return redirect(url_for('list_routes.list_details', list_id=list_id))

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

# Delete an Image 
@image_routes.route('/delete_image/<int:list_id>/<int:image_id>', methods=['GET'])
@login_required
def delete_image(list_id, image_id):
    image = Image.query.get_or_404(image_id)

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
