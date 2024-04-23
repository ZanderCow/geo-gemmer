from flask import Blueprint, render_template,redirect,request,jsonify, session
from repositories import user_repository
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from repositories import user_repository, gem_repository as gem_repo
from repositories import user_repository, gems_pinned_repository, gems_visited_repository

user = Blueprint('user', __name__)



@user.get('/')
@jwt_required()
def dashboard():
    #TODO:
    # get user data from database
    # get user hidden gems from database
    user_id = get_jwt_identity()  # Retrieves the identity from the JWT
    user_info = user_repository.get_user_by_id(user_id)

    user_name = user_repository.get_username_by_id(user_id)["username"]
    
    

    gem_visted_frequency = {
        'January': 1,
        'February': 2,
        'March': 3,
        'April': 4,
        'May': 2,
        'June': 5,
        'July': 7,
        'August': 5,
        'September': 3,
        'October': 2,
        'November': 1,
        'December': 1
    }


    gem_distribution = {
            'Restaurant': 7,
            'Park': 3,
            'Museum':2,
            'Beach': 1,
            'Trail': 1,
        }  
    
    gems_pinned = [
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15",
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"
            }, 
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15",
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"        
            },
            {
               'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15",
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"      
            }         
        ]
    gem_visted_frequency = gems_visited_repository.get_hidden_gems_visited_by_month(user_id)

    gem_distribution = gems_visited_repository.get_distribution_of_hidden_gems_visited_by_a_user(user_id)
    
    gems_pinned = gems_pinned_repository.get_gems_pinned_by_user(user_id)
    
    reviews_made =  [
            {
                'gem_name': 'Rocky Mountian',
                'rating': 1,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
                
            }, 
            {
                'gem_name': 'Rocky Mountian',
                'rating': 5,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
            }
        
        ]


    return render_template('dashboard.html', 
        user_info=user_info,
        gem_visted_frequency=gem_visted_frequency,
        gem_distribution=gem_distribution,
        gems_pinned=gems_pinned,
        reviews_made=reviews_made,username=user_name
        )




@user.get('/settings')
@jwt_required()
def render_settings_page():
    user_id = get_jwt_identity()  # Retrieves the identity from the JWT
    user_settings = user_repository.get_user_settings_details(user_id)

    return render_template('user-settings.html', user_settings=user_settings)

@user.post('/settings')
@jwt_required()
def change_settings_page():
    user_id = get_jwt_identity()
    data = request.get_json()

    user_name = data.get('username')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    pfp_url = data.get('pfp')
    print(user_name)

    errors = {}

    if user_repository.does_username_exist(user_name):
        errors['username'] = 'Username already exists'

    
    if user_name == '':
        errors['username'] = 'Username is required'

    # if there are no errors, create the user
    if errors == {}:
        user_repository.change_user_settings(user_id, user_name, first_name, last_name, pfp_url)
        return jsonify({'username': user_name}), 200
    
    else:
        return jsonify(errors), 400

    user_repository.change_user_settings(user_id, first_name, last_name)

    

@user.get('/create-gem')
@jwt_required()
def render_create_gem_page():
    return render_template('create-hidden-gem.html')

@user.post('/create-gem')
@jwt_required()
def create_gem():
    """
    Create a new gem in the database based on the incoming JSON data.

    Returns:
        A JSON response containing a success message and the URL of the created gem.
    """
    data = request.get_json()  # get the incoming JSON data

    # list of fields that should not be empty
    required_fields = ['gem_name', 'gem_type', 'latitude', 'longitude']

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields:
        return jsonify({'error': f'The following fields are required and were not provided: {", ".join(missing_fields)}'}), 400  # 400 is the status code for "Bad Request"


    #get the images into a list
    images = list()
    if ('image_1' in data): images.append(images['image_1'])
    if ('image_2' in data): images.append(images['image_2'])
    if ('image_3' in data): images.append(images['image_3'])

    #TODO : something with the images T_T
    #actually create the gem
    gem_url = gem_repo.create_new_gem(data['gem_name'], data['gem_type'], data['longitude'], data['latitude'], True)

    #set the accesssibility
    acc = gem_repo.accessibility_class()
    if ('wheelchair_accessible' in data and data['wheelchair_accessible'] == True):
        acc.wheelchair_accessible = True
    if ('service_animal_friendly' in data and data['service_animal_friendly'] == True):
        acc.service_animal_friendly = True
    if ('multilingual_support' in data and data['multilingual_support'] == True):
        acc.multilingual_support = True
    if ('braille_signage' in data and data['braille_signage'] == True):
        acc.braille_signage = True
    if ('large_print_materials' in data and data['large_print_materials'] == True):
        acc.large_print_materials = True
    if ('accessible_restrooms' in data and data['accessible_restrooms'] == True):
        acc.accessible_restrooms = True
    if ('hearing_assistance' in data and data['hearing_assistance'] == True):
        acc.hearing_assistance = True
    gem_repo.change_accessibility(gem_url, acc)
    

    return jsonify(
    {
        'message': 'Gem created successfully',
        'gem_id': gem_url
    }
)




@user.post("/logout")
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response 

