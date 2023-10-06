"""
list_routes.py

This module contains routes related to image list functionalities, including
creating, editing, deleting lists, managing fields associated with lists,
and viewing the slideshow of images in a list.
"""

# Necessary imports for Flask, Flask-WTF forms, database operations, and other utilities.
from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from forms import CreateListForm, EditListNameForm
from models import ImageList, Image, ListCategory, db, Field, FieldData, ImagePosition
from flask_cors import CORS 
import re

# Blueprint definition for list routes
list_routes = Blueprint('list_routes', __name__)

# Function to either create a new category or fetch it if it already exists.
def create_or_get_category(category_name):
    """Function to create or fetch an existing category."""
    if not category_name:
        return None  # No category is assigned

    # Capitalize the category name
    category_name = category_name.capitalize()

    category = ListCategory.query.filter_by(name=category_name).first()

    if not category:
        # If category doesn't exist, create it
        category = ListCategory(name=category_name)
        db.session.add(category)
        db.session.commit()

    return category

# Route to navigate to a user's lists
@list_routes.route("/go_to_lists")
@login_required
def go_to_lists():
    user_id = current_user.id

    your_lists = ImageList.query.filter_by(creator_id=user_id).all()
    our_lists = ImageList.query.filter_by(core_list=True).all()
    all_lists = ImageList.query.all()

    # Categories for "Your Lists"
    your_categories_ids = set(list_.category_id for list_ in your_lists if list_.category_id)
    your_categories = ListCategory.query.filter(ListCategory.category_id.in_(your_categories_ids)).all()
    # Check for lists without images
    has_new_lists = any(len(image_list.images) == 0 for image_list in your_lists)
    
    # Categories for "Our Lists"
    our_categories_ids = set(list_.category_id for list_ in our_lists if list_.category_id)
    our_categories = ListCategory.query.filter(ListCategory.category_id.in_(our_categories_ids)).all()

    # Categories for "All Lists"
    all_categories = ListCategory.query.all()

    return render_template(
        "go_to_lists.html", 
        your_categories=your_categories, 
        your_lists=your_lists, 
        our_categories=our_categories,
        our_lists=our_lists, 
        all_categories=all_categories, 
        all_lists=all_lists,
        has_new_lists=has_new_lists
    )

# Route to view details of a particular list.
@list_routes.route("/list_details/<int:list_id>")
@login_required
def list_details(list_id):
    print('On list_details, list_id: ', list_id)
    image_list = ImageList.query.get_or_404(list_id)
    categories = ListCategory.query.all()

    # Fetch the ordered images for this list
    ordered_images_query = db.session.query(
        Image
    ).join(
        ImagePosition, ImagePosition.image_id == Image.image_id
    ).filter(
        ImagePosition.list_id == list_id
    ).order_by(
        ImagePosition.position
    ).all()

    # Fetch the associated fields for this list
    fields = Field.query.filter_by(list_id=list_id).all()
    print('fields: ', fields)

    # Fetch field values for each image
    image_field_values = {}
    for image in ordered_images_query:
        image_field_values[image.image_id] = {data.field_id: data.value for data in FieldData.query.filter_by(image_id=image.image_id).all()}

    return render_template("list_details.html", image_list=image_list, images=ordered_images_query, list_id=list_id, fields=fields, categories=categories, image_field_values=image_field_values)

# Route to create a new image list.
@list_routes.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    form = CreateListForm()  # instantiate the form

    # Dynamically set the category_name choices while preserving the default choice
    default_choice = [('', '-- No Category For Now --')]
    dynamic_choices = [(c.name, c.name) for c in ListCategory.query.all()]
    form.category_name.choices = default_choice + dynamic_choices

    if form.validate_on_submit():  # This replaces the check for request.method == 'POST'

        list_name = form.list_name.data
        is_core_list = form.core_list.data == 'yes'
        category_name = form.category_name.data

        # Check if user has provided a new category
        if form.new_category.data:
            category_name = form.new_category.data

        category = create_or_get_category(category_name)

        # If category is None, don't set category_id, else set it to the returned category's ID
        category_id = None
        if category:
            category_id = category.category_id
            print("Assigned Category ID:", category_id)

        image_list = ImageList(name=list_name, category_id=category_id, creator_id=current_user.id, core_list=is_core_list)
        db.session.add(image_list)
        try:
            db.session.commit()
            flash('List created successfully!', 'success')
            return redirect(url_for('list_routes.go_to_lists'))
        except Exception as e:
            print("Error committing to database:", e)
            flash('Error creating list.', 'danger')

    return render_template('create_list.html', form=form)

# Category Routes: 
# Route to remove a category from a list.
@list_routes.route("/remove_category/<int:list_id>", methods=["POST"])
@login_required
def remove_category(list_id):
    """ Remove category_id from a list """
    image_list = ImageList.query.get_or_404(list_id)
    
    # Ensure that only the creator can remove the category
    if image_list.creator_id != current_user.id:
        # flash('You do not have permission to modify this list.', 'danger') 
        return jsonify({"status": "error", "message": 'You do not have permission to modify this list.'})

    image_list.category_id = None  # remove the category
    db.session.commit()
    # flash('Category removed successfully!', 'success') 
    return jsonify({"status": "success", "message": 'Category removed successfully!'})

# Route to navigate to a page for adding a new category to a list.
@list_routes.route('/add_a_category/<list_id>', methods=['GET'])
def add_category_page(list_id):
    image_list = ImageList.query.get_or_404(list_id)  # This is a hypothetical function, replace with your actual function that retrieves the image list by ID.
    print('from list details - image_list.list_id: ', image_list.list_id)
    if not list_id or list_id == "undefined":
    # Handle the error, maybe redirect to a 404 page or to the home page with an error message
        return redirect(url_for('home'))
    if not image_list:
        abort(404)
    categories = ListCategory.query.all()           # Again, replace with your actual function that retrieves all categories.
    return render_template('add_a_category.html', image_list=image_list, categories=categories)

# Route to add a new category to an existing list.
@list_routes.route('/<int:list_id>/add_category', methods=['GET', 'POST'])
@login_required
def add_category_to_list(list_id):
    image_list = ImageList.query.get_or_404(list_id)  # Assuming ImageList is your model for lists
    print('from add_a_category - image_list.list_id: ', image_list.list_id)
    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            category_name = category_name.capitalize()
            category = create_or_get_category(category_name)
            if category:
                image_list.category_id = category.category_id # Linking the list to the category
                db.session.commit()  # Save the changes. Ensure you've imported db from your app.
                flash(f'Category "{category_name}" added to the list!', 'success')
            #     return redirect(url_for('list_routes.list_details', list_id=list_id))
            # else:
            #     flash(f'Error creating category "{category_name}".', 'danger')

                return jsonify({ "status": "success", "message": f'Category "{category_name}" added to the list!', "redirect_url": url_for('list_routes.list_details', list_id=list_id) })
            else:
                return jsonify({"status": "error", "message": f'Error creating category "{category_name}".'})

    categories = Category.query.all()
    return render_template('list_details.html', categories=categories, image_list=image_list)  

# Route to delete a specific image list.
@list_routes.route('/delete_list/<int:list_id>', methods=['GET', 'POST'])
@login_required
def delete_list(list_id):
    image_list = ImageList.query.get_or_404(list_id)

    # Check if the list belongs to the current user OR if the current user is an admin
    if image_list.creator_id != current_user.id and not current_user.is_admin:
        flash("You don't have permission to delete this list.", 'error')
        return redirect(url_for('list_routes.go_to_lists'))

    try:
        # Simply delete the list, the cascade options should handle related deletions
        db.session.delete(image_list)
        db.session.commit()
        flash("List deleted successfully!")
    except Exception as e:
        db.session.rollback()
        flash(f"Error deleting the list: {str(e)}", "error")

    return redirect(url_for('list_routes.go_to_lists'))

# Route to navigate to a page for editing the name of a list.
@list_routes.route('/edit_list_name/<int:list_id>', methods=['GET', 'POST'])
def edit_list_name(list_id):
    # Retrieve the current list by its ID.
    image_list = ImageList.query.get_or_404(list_id)
    
    # Instantiate the form and set the initial value.
    form = EditListNameForm(list_name=image_list.name)

    # Handle POST request.
    if form.validate_on_submit():
        image_list.name = form.list_name.data
        db.session.commit()
        return redirect(url_for('list_routes.list_details', list_id=list_id))

    # Handle GET request.
    form.list_name.data = image_list.name
    return render_template('edit_list_name.html', form=form, list_id=list_id)

# Route to update the name of a list.
@list_routes.route('/update_list_name/<int:list_id>', methods=['POST'])
def update_list_name(list_id):
    print('Trying to save list name')
    try:
        # Get the new name from the form data
        new_name = request.form.get('list_name')

        # Fetch the list
        image_list = ImageList.query.get(list_id)
        if not image_list:
            return jsonify(success=False, message="List not found"), 404

        # Update the list name
        image_list.name = new_name
        db.session.commit()

        return jsonify(success=True)

    except Exception as e:
        print(str(e))
        return jsonify(success=False, message="An error occurred"), 500

# Route to navigate to a page for editing fields associated with a list.
@list_routes.route('/edit_fields_get/<int:list_id>', methods=['GET'])
def edit_fields_get(list_id):
    # Fetch the custom fields for the list
    # fields = Field.query.filter_by(list_id=list_id).all()
    fields = Field.query.filter_by(list_id=list_id).order_by(Field.name).all()

    return render_template('edit_fields.html', list_id=list_id, fields=fields)

# Route to save changes to fields associated with a list.
@list_routes.route('/edit_fields/<int:list_id>', methods=['POST'])
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
        # Return a failure response if there's an exception
        # return jsonify({'success': False, 'message': 'Failed to update database'})
        flash('Failed to update database!')
        return redirect(url_for('list_routes.list_details', list_id=list_id))

    # If everything goes well, return a success response
    flash('Fields edited successfully!')
    return redirect(url_for('list_routes.list_details', list_id=list_id))

# Route to navigate to a carousel/slideshow for a list.
@list_routes.route('/carousel/<int:list_id>')
def carousel(list_id):
    # Pass the list_id to the carousel.html template
    return render_template('carousel.html', list_id=list_id)

# Route to initiate the slideshow for a list.
@list_routes.route('/slideshow/<int:list_id>')
def slideshow(list_id):
    # Join Image and ImagePosition and filter by list_id.
    # Then, order the images by their position in the ImagePosition table.
    images = db.session.query(Image).join(
        ImagePosition, Image.image_id == ImagePosition.image_id
    ).filter(
        ImagePosition.list_id == list_id
    ).order_by(
        ImagePosition.position
    ).all()

    print('images: ', images)
    return render_template('carousel.html', images=images, list_id=list_id)

