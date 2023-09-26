from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import ImageList, Image, ListCategory, db
import requests

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
@image_routes.route('/edit_image/<int:list_id>', methods=['GET'])
def edit_image(list_id):
    selected_image_url = request.args.get('selected_image_url')
    
    if not selected_image_url:
        # Handle the absence of an image URL
        flash("No image provided!")
        return redirect(url_for('image_routes.image_search', list_id=list_id))
    
    # Fetch custom fields from the database
    # custom_fields = CustomField.query.filter_by(list_id=list_id).all()
    # Removed from return:  custom_fields=custom_fields

    return render_template('edit_image.html', image_url=selected_image_url, list_id=list_id,)
    
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