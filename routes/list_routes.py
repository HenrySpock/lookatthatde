from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app, jsonify
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import ImageList, Image, ListCategory, db, Field, FieldData, ImagePosition
from flask_cors import CORS 

list_routes = Blueprint('list_routes', __name__)

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

# @list_routes.route("/list_details/<int:list_id>")
# @login_required
# def list_details(list_id):
#     print('On list_details, list_id: ', list_id)
#     image_list = ImageList.query.get_or_404(list_id)
#     categories = ListCategory.query.all()

#     # Fetch the images for this list
#     images = Image.query.filter_by(list_id=list_id).all()
    
#     # Fetch the associated fields for this list
#     fields = Field.query.filter_by(list_id=list_id).all()
#     print('fields: ', fields)

#     # Fetch field values for each image
#     image_field_values = {}
#     for image in images:
#         image_field_values[image.image_id] = {data.field_id: data.value for data in FieldData.query.filter_by(image_id=image.image_id).all()}

#     return render_template("list_details.html", image_list=image_list, images=images, list_id=list_id, fields=fields, categories=categories, image_field_values=image_field_values)

# Updated list_details for ordering by image_position.
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

@list_routes.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    if request.method == 'POST':
        list_name = request.form.get('list_name')
        
        category_name = request.form.get('category_name')  # assuming it's a dropdown with values or user input
        new_category_name = request.form.get('new_category')

        if new_category_name:  # Check if user has provided a new category
            category_name = new_category_name  # Override category_name with the new one

        category = create_or_get_category(category_name)

        # If category is None, don't set category_id, else set it to the returned category's ID
        category_id = None
        if category:
            category_id = category.category_id
            print("Assigned Category ID:", category_id)
        
        image_list = ImageList(name=list_name, category_id=category_id, creator_id=current_user.id)
        db.session.add(image_list)
        try:
            db.session.commit()
        except Exception as e:
            print("Error committing to database:", e)

        flash('List created successfully!', 'success')
        return redirect(url_for('list_routes.go_to_lists'))
    
    return render_template('create_list.html', categories=ListCategory.query.all())


# Category Routes:

#Removing a category from a list
@list_routes.route("/remove_category/<int:list_id>", methods=["POST"])
@login_required
def remove_category(list_id):
    """ Remove category_id from a list """
    image_list = ImageList.query.get_or_404(list_id)
    
    # Ensure that only the creator can remove the category
    if image_list.creator_id != current_user.id:
        flash('You do not have permission to modify this list.', 'danger')
        return redirect(url_for('list_routes.list_details', list_id=list_id))

    image_list.category_id = None  # remove the category
    db.session.commit()
    flash('Category removed successfully!', 'success')
    return redirect(url_for('list_routes.list_details', list_id=list_id))

#Adding a category to a list after creation:
@list_routes.route('/<int:list_id>/add_category', methods=['GET', 'POST'])
@login_required
def add_category_to_list(list_id):
    image_list = ImageList.query.get_or_404(list_id)  # Assuming ImageList is your model for lists

    if request.method == 'POST':
        category_name = request.form.get('category_name')
        if category_name:
            category_name = category_name.capitalize()
            category = create_or_get_category(category_name)
            if category:
                image_list.category_id = category.category_id # Linking the list to the category
                db.session.commit()  # Save the changes. Ensure you've imported db from your app.
                flash(f'Category "{category_name}" added to the list!', 'success')
                return redirect(url_for('list_routes.list_details', list_id=list_id))
            else:
                flash(f'Error creating category "{category_name}".', 'danger')

    categories = Category.query.all()
    return render_template('list_details.html', categories=categories, image_list=image_list)  

# @list_routes.route('/delete_list/<int:list_id>', methods=['GET', 'POST'])
# @login_required
# def delete_list(list_id):
#     image_list = ImageList.query.get_or_404(list_id)

#     # Check if the list belongs to the current user
#     if image_list.creator_id != current_user.id:
#         flash("You don't have permission to delete this list.", 'error')
#         return redirect(url_for('list_routes.go_to_lists'))

#     try:
#         # Simply delete the list, the cascade options should handle related deletions
#         db.session.delete(image_list)
#         db.session.commit()
#         flash("List deleted successfully!")
#     except Exception as e:
#         db.session.rollback()
#         flash(f"Error deleting the list: {str(e)}", "error")

#     return redirect(url_for('list_routes.go_to_lists'))

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


#Update List name: 
@list_routes.route('/update_list_name/<int:list_id>', methods=['POST'])
def update_list_name(list_id):
    print('Trying to save list name')
    try:
        # Get the new name from the form data
        new_name = request.form.get('new_name')

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

