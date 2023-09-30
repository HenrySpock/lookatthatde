from app import db
from models import Users, ImageList, Image, ListCategory

#User Seed function
def seed_users():
    # Check if users already exist to avoid seeding multiple times
    existing_user = Users.query.first()
    if existing_user:
        print("Users already exist. Skipping seeding.")
        return

    # Create regular user 1
    regular_user1 = Users(username='testuser1', email='testuser1@testuser1.com', first_name="Testy1", last_name="User1")
    regular_user1.set_password('testuser1')

    # Create regular user 2
    regular_user2 = Users(username='testuser2', email='testuser2@testuser2.com', first_name="Testy2", last_name="User2")
    regular_user2.set_password('testuser2')

    # Create an admin user
    admin_user1 = Users(username='admin1', email='admin1@admin1.com', is_admin=True, first_name="admin1", last_name="admin1")
    admin_user1.set_password('admin1')
    
    # Create a second  admin user
    admin_user2 = Users(username='admin2', email='admin2@admin2.com', is_admin=True, first_name="admin2", last_name="admin2")
    admin_user2.set_password('admin2')

    # Add and commit the users to the database 
    db.session.add_all([regular_user1, regular_user2, admin_user1, admin_user2])
    db.session.commit()

    print("Test users seeded!")


#List Seed function
def seed_image_lists():

    # Lists and their images
    data = [
        {
            "name": "American WWII Fighters",
            "description": "Images of WWII fighter planes flown by the United States Air Force.",
            "category_id": 2,
            "creator_id": 3,
            "core_list": True,
            "images": [
                {
                    'image_url': 'https://farm6.staticflickr.com/5530/13785673395_285d044b65.jpg',
                    'name': 'P-1 Hawk',
                    # 'description': 'Open-cockpit biplane flown by the United States Army Air Corps.',
                    # 'year': 1923,
                    # 'manufacturer': 'Curtiss'
                },
                {
                    'image_url': 'https://farm4.staticflickr.com/3157/4562140266_fb2d52f17f.jpg',
                    'name': 'P-2 Hawk',
                    # 'description': 'Open-cockpit biplane flown by the United States Army Air Corps.',
                    # 'year': 1925,
                    # 'manufacturer': 'Curtiss'
                },
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/2/2c/Curtiss_P-3_Hawk_with_no_engine_cowling_060831-F-1234P-011.jpg',
                #     'name': 'P-3 Hawk',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # }, 
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/4f/Curtiss_-_P-5_-_Hawk_%284584019427%29.jpg?20150524102954',
                #     'name': 'P-5 Hawk',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'https://farm66.staticflickr.com/65535/49049647067_2ed465f8b9.jpg',
                #     'name': 'P-6 Hawk',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },    
                # {
                #     'image_url': 'https://farm66.staticflickr.com/65535/40858056973_fcb591ce3c.jpg',
                #     'name': 'P-12',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Boeing'
                # },
                # {
                #     'image_url': 'https://farm4.staticflickr.com/3054/4561517515_e109f9b727.jpg',
                #     'name': 'P-13 Viper',
                #     'description': 'XP-13, an experimental plane.',
                #     'year': 19,
                #     'manufacturer': 'Thomas-Morse'
                # }, 
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/4/46/Boeing_XP-15_060906-F-1234P-001.jpg',
                #     'name': 'P-15',
                #     'description': 'Prototype monoplane.',
                #     'year': 19,
                #     'manufacturer': 'Boeing'
                # },
                # {
                #     'image_url': 'https://farm8.staticflickr.com/7434/14168891612_cc6f478f45.jpg',
                #     'name': 'P-16',
                #     'description': 'Redesignated PB-1.',
                #     'year': 19,
                #     'manufacturer': 'Berliner-Joyce'
                # },  
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/0/08/Curtiss_YP-20.jpg',
                #     'name': 'P-20',
                #     'description': 'Designated YP-20.',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # }, 
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/1/13/Curtiss_XP-22_060906-F-1234P-008.jpg',
                #     'name': 'P-22 Hawk',
                #     'description': 'Designated experimental: XP 22.',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'https://oldmachinepress.files.wordpress.com/2021/01/curtiss-xp-23-front-left.jpg?w=768',
                #     'name': 'P-23 Hawk',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'https://upload.wikimedia.org/wikipedia/commons/e/e4/Detroit-Lockheed_YP-24_side_view.jpg',
                #     'name': 'P-24',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # }, 
                # {
                #     'image_url': 'https://farm66.staticflickr.com/65535/53122806617_ffb709a3ab.jpg',
                #     'name': 'P-26 Peashooter',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Boeing'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-27',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Consolidated'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-28',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Consolidated'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-29',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Boeing'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-30',
                #     'description': 'Redesignated PB-2',
                #     'year': 19,
                #     'manufacturer': 'Consolidated'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-31 Swift',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-32',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Boeing'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-33',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Consolidated'
                # },
                # {
                #     'image_url': '',
                #     'name': 'P-34',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Wedell-Williams'
                # },
                # {
                #     'image_url': 'P-35',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Seversky'
                # },
                # {
                #     'image_url': 'P-36 Hawk',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-37',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-38 Lighting',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # },
                # {
                #     'image_url': 'P-39 Airacobra',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-40 Warhawk',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-41',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Seversky'
                # },
                # {
                #     'image_url': 'P-42',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-43 Lancer',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-44 Rocket',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-45',
                #     'name': '',
                #     'description': 'Redesignated P-39C.',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-46',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-47 Thunderbolt',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-48',
                #     'name': '',
                #     'description': 'Not Built',
                #     'year': 19,
                #     'manufacturer': 'Douglas'
                # },
                # {
                #     'image_url': 'P-49',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # },
                # {
                #     'image_url': 'P-50',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Grumman'
                # },
                # {
                #     'image_url': 'P-51 Mustang',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'North American'
                # },
                # {
                #     'image_url': 'P-52',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-53',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-54 Swoose Goose',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Vultee'
                # },
                # {
                #     'image_url': 'P-55 Ascender',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-56 Black Bullet',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Northrop'
                # },
                # {
                #     'image_url': 'P-57 Peashooter',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Tucker'
                # },
                # {
                #     'image_url': 'P-58 Chain Lightning',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # },
                # {
                #     'image_url': 'P-59',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-59 Airacomet',
                #     'name': '',
                #     'description': 'Conflicting designation, assigned after original P-59 was canceled.',
                #     'year': 19,
                #     'manufacturer': ''
                # },
                # {
                #     'image_url': 'P-60',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-61 Black Widow',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Northrop'
                # },
                # {
                #     'image_url': 'P-62',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-63 Kingcobra',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-64',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'North American'
                # },
                # {
                #     'image_url': 'P-65',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Grumman'
                # },
                # {
                #     'image_url': 'P-66 Vanguard',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Vultee'
                # },
                # {
                #     'image_url': 'P-67 Bat',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'McDonnell'
                # },
                # {
                #     'image_url': 'P-68 Tornado',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Vultee'
                # },
                # {
                #     'image_url': 'P-69',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-70 Nighthawk',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Douglas'
                # },
                # {
                #     'image_url': 'P-71',
                #     'name': '',
                #     'description': 'Not built.',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-72',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-73',
                #     'name': '',
                #     'description': 'Unofficial designation.',
                #     'year': 19,
                #     'manufacturer': 'Hughes'
                # },
                # {
                #     'image_url': 'P-74',
                #     'name': '',
                #     'description': 'Skipped.',
                #     'year': 19,
                #     'manufacturer': ''
                # },
                # {
                #     'image_url': 'P-75 Eagle',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Fisher'
                # },
                # {
                #     'image_url': 'P-76',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-77',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-78',
                #     'name': '',
                #     'description': 'Redesignated P-51B.',
                #     'year': 19,
                #     'manufacturer': 'North American'
                # },
                # {
                #     'image_url': 'P-79',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Northrop'
                # },
                # {
                #     'image_url': 'P-80 Shooting Star',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # },
                # {
                #     'image_url': 'P-81',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Convair'
                # },
                # {
                #     'image_url': 'P-82 Twin Mustang',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'North American'
                # },
                # {
                #     'image_url': 'P-83',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Bell'
                # },
                # {
                #     'image_url': 'P-84 Thunderjet',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-85 Goblin',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'McDonnell'
                # },
                # {
                #     'image_url': 'P-86 Sabre',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'North American'
                # },
                # {
                #     'image_url': 'P-87 Blackhawk',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Curtiss'
                # },
                # {
                #     'image_url': 'P-88 Voodoo',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'McDonnell'
                # },
                # {
                #     'image_url': 'P-89 Scorpion',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Northrop'
                # },
                # {
                #     'image_url': 'P-90',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Lockheed'
                # },
                # {
                #     'image_url': 'P-91 Thunderceptor',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Republic'
                # },
                # {
                #     'image_url': 'P-92',
                #     'name': '',
                #     'description': '',
                #     'year': 19,
                #     'manufacturer': 'Convair'
                # },
            ],
        },
        {
            "name": "Construction Vehicles",
            "description": "Various types of construction vehicles.",
            "category_id": 2,
            "creator_id": 3, 
            "core_list": False,
            "images": [
                {
                    'image_url': 'https://farm66.staticflickr.com/65535/53193912641_3a1cdb01da.jpg',
                    'name': 'Excavator',
                    # 'description': 'A modern update of the steam shovel consisting of a boom, dipper (or stick), bucket and cab on a rotating platform known as the "house". The house sits atop an undercarriage commonly with tracks.',  
                },
                {
                    'image_url': 'https://farm66.staticflickr.com/65535/53100752888_ee04696220.jpg',
                    'name': 'Dozer (or Bulldozer)',
                    # 'description': 'A large, motorized machine equipped with a metal blade to the front for pushing material, shown here with a rear multi-line ripper.',  
                },
            ],
        },
        {
            "name": "Zoo Animals",
            "description": "Various animals you might find in a zoo.",
            "category_id": 1,
            "creator_id": 1, 
            "core_list": False,
            "images": [
                {
                    'image_url': 'https://farm66.staticflickr.com/65535/53200619296_91500606db.jpg',
                    'name': 'Puma', 
                    # 'country_of_origin': 'South America and the Western United States',
                    # 'description': 'A modern update of the steam shovel consisting of a boom, dipper (or stick), bucket and cab on a rotating platform known as the "house". The house sits atop an undercarriage commonly with tracks.',  
                },
        # ... Repeat for all 11 lists ...
            ]
        },
                {
            "name": "Jigsaw Puzzles",
            "description": "My list of owned jigsaw puzzles.",
            # "category_id": ,
            "creator_id": 2, 
            "core_list": False,
            "images": [
                {
                    'image_url': 'https://farm66.staticflickr.com/65535/52944894166_46898891be.jpg',
                    'name': 'Florentine Mosaic', 
                    # 'num_pieces': '500',
                    # 'manufacturer': 'Springbok',
                    # 'year': 1971,
                    # 'description': 'A beautiful octagonal puzzle based on a table design for the Medici in Renaissance Florence.',  
                },
        # ... Repeat for all 11 lists ...
            ]
        },
    ]

    # Loop through the data to populate the database
    # for item in data:
    #     image_list = ImageList(
    #         name=item["name"],
    #         description=item.get("description"),  # Optional, so using get
    #         creator_id=admin_id
    #     )
    #     db.session.add(image_list)
    #     db.session.flush()  # So we get the list_id immediately

    #     for img_data in item["images"]:
    #         image = Image(
    #             list_id=image_list.list_id,
    #             image_url=img_data['image_url'],
    #             name=img_data['name'],
    #             description=img_data['description'],
    #             year=img_data.get('year', None),  # Using get in case 'year' or 'manufacturer' is missing
    #             manufacturer=img_data.get('manufacturer', None)
    #         )
    #         db.session.add(image)

    #     db.session.commit()

    for item in data:
        image_list = ImageList(
            name=item["name"],
            description=item.get("description"),  # Optional, so using get
            creator_id=item["creator_id"],
            category_id=item.get("category_id", None),  # Using get in case 'category_id' is missing
            core_list=item.get("core_list", False)
        )
        db.session.add(image_list)
        db.session.flush()  # So we get the list_id immediately

        for img_data in item["images"]:
            image = Image(
                list_id=image_list.list_id,
                image_url=img_data['image_url'],
                name=img_data['name'],
                # description=img_data.get('description', None),
                # year=img_data.get('year', None),
                # num_pieces=img_data.get('num_pieces', None),
                # cat_number=img_data.get('cat_number', None),
                # country_of_origin=img_data.get('country_of_origin', None),
                # manufacturer=img_data.get('manufacturer', None)
            )
            db.session.add(image)

        db.session.commit()


    print("Image lists seeded!")

def seed_categories():
    # Check if categories already exist to avoid seeding multiple times
    existing_category = ListCategory.query.first()
    if existing_category:
        print("Categories already exist. Skipping seeding.")
        return

    # List of category names
    category_names = [
                    # "Uncategorized", 
                    "Animals", "Vehicles"]

    # Iterate through the category names and add each to the database
    for name in category_names:
        category = ListCategory(name=name)
        db.session.add(category)

    # Commit the session to save the categories
    db.session.commit()

    print("Categories seeded!")

