from flask import Blueprint, redirect, url_for, render_template, session, flash, request, current_app
from flask_login import logout_user, login_user, current_user, login_required
from forms import RegistrationForm, LoginForm, EditProfileForm, ChangePasswordForm, SupportForm
from models import ImageList, Image, ListCategory, db

list_routes = Blueprint('list_routes', __name__)

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

@list_routes.route("/list_details/<int:list_id>")
@login_required
def list_details(list_id):
    print('On list_details, list_id: ', list_id)
    image_list = ImageList.query.get_or_404(list_id)
    image_records = Image.query.filter_by(list_id=list_id).all()

    # Prepare a list to hold dictionaries for each image with only non-empty fields
    images = []
    for image in image_records:
        image_dict = {}
        for column in image.__table__.columns:
            value = getattr(image, column.name)
            if value and column.name not in ['list_id', 'image_id']:  # Exclude the fields list_id and image_id
                image_dict[column.name] = value
        images.append(image_dict)
    
    return render_template("list_details.html", image_list=image_list, images=images, list_id=list_id)

#Create a List
@list_routes.route('/create_list', methods=['GET', 'POST'])
@login_required
def create_list():
    if request.method == 'POST':
        list_name = request.form.get('list_name')
        
        # Handle category
        category_name = request.form.get('category_name')  # assuming it's a dropdown with values or user input
        new_category_name = request.form.get('new_category')

        if new_category_name:  # Check if user has provided a new category
            category_name = new_category_name  # Override category_name with the new one

        # Capitalize the category name
        category_name = category_name.capitalize()
        print("Category Name:", category_name)

        category_id = None  # default to no category
        category = None  # Initialize category to None

        if category_name:
            category = ListCategory.query.filter_by(name=category_name).first()

        if not category:
            print("Creating a new category:", category_name)
            # If category doesn't exist, create it
            category = ListCategory(name=category_name)
            db.session.add(category)
            db.session.commit()

        category_id = category.category_id
        print("Assigned Category ID:", category_id)

        # Save list details
        # NOTE: ImageList model has a creator_id and category_id, not a user_id. Thus, we adjust the attributes.
        image_list = ImageList(name=list_name, category_id=category_id, creator_id=current_user.id)
        db.session.add(image_list)
        try:
            db.session.commit()
        except Exception as e:
            print("Error committing to database:", e)

        # (I've omitted the handling of fields as you said it was not relevant at this moment)

        flash('List created successfully!', 'success')
        return redirect(url_for('list_routes.go_to_lists'))
    
    return render_template('create_list.html', categories=ListCategory.query.all())
