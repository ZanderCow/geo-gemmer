from flask import Blueprint, render_template,redirect,request,jsonify, session
from repositories import user_repository
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from repositories import user_repository, gem_repository as gem_repo
from repositories import user_repository, gems_pinned_repository, gems_visited_repository
from repositories import images_repository
import base64


from repositories import review_repository

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
    

    gem_visted_frequency = gems_visited_repository.get_hidden_gems_visited_by_month(user_id)

    gem_distribution = gems_visited_repository.get_distribution_of_hidden_gems_visited_by_a_user(user_id)
    
    gems_pinned = gems_pinned_repository.get_gems_pinned_by_user(user_id)
    


    reviews_made = review_repository.get_all_reviews_user_has_made(user_id)
    print(reviews_made)


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


    current_pfp_url = images_repository.get_database_pfp(user_id)

    # Check if the user has a profile picture
    if current_pfp_url != None:
        
        #image_bytes = None
        #image_bytes = images_repository.get_user_pfp(user_id)
        #base64_encoded_data = base64.b64encode(image_bytes)
        #base64_image = base64_encoded_data.decode('utf-8')
        return render_template('user-settings.html', user_settings=user_settings)
        #uncomment and delete the line above to make s3 work
        #return render_template('user-settings.html', user_settings=user_settings,image_data=base64_image)
    else:
        return render_template('user-settings.html', user_settings=user_settings)



@user.post('/settings')
@jwt_required()
def change_settings_page():
    user_id = get_jwt_identity()
    file = request.files.get('file')
    user_name = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')

    errors = {}
    
    #user filled out the username field
    if user_name != '':
        #check if the username is already taken
        if user_repository.does_username_exist(user_name):
            errors['username'] = 'Username already exists'
        else:
            user_repository.change_username(user_id, user_name)


    #user filled out the first name field
    if first_name != '':
        user_repository.change_first_name(user_id, first_name)

    if last_name != '':
        user_repository.change_last_name(user_id, last_name)


    # Check if the user uploaded a profile picture
    if file:
        current_pfp_url = images_repository.get_database_pfp(user_id)
        
        # Check if the user already has a profile picture
        if current_pfp_url != None:
            
            #uncomment the line below to make s3 work 
            # images_repository.update_user_pfp(user_id, file)
            pass
        
        else:
            #uncomment the line below to make s3 work 
            # images_repository.create_user_pfp(user_id, file)
            pass

    
   
    if errors == {}:
        return jsonify(
            {
            'message': 'Settings updated successfully',
            'username': user_name,
             }
            ), 200
    else:
        return jsonify(errors), 400



    

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
    user_id = get_jwt_identity()
    gem_name = request.form.get('gem_name')
    gem_type = request.form.get('gem_type')
    latitude = request.form.get('latitude')
    longitude = request.form.get('longitude')

    wheelchair_accessible = request.form.get('wheelchair_accessible')
    service_animal_friendly = request.form.get('service_animal_friendly')
    multilingual_support = request.form.get('multilingual_support')
    braille_signage = request.form.get('braille_signage')
    large_print_materials = request.form.get('large_print_materials')
    accessible_restrooms = request.form.get('accessible_restrooms')
    hearing_assistance = request.form.get('hearing_assistance')

    image_1 = request.files.get('image_1')
    image_2 = request.files.get('image_2')
    image_3 = request.files.get('image_3')
    
    
    acc = gem_repo.accessibility_class()

    if wheelchair_accessible == True:
        acc.wheelchair_accessible = True
    if service_animal_friendly == True:
        acc.service_animal_friendly = True
    if multilingual_support == True:
        acc.multilingual_support = True
    if braille_signage == True:
        acc.braille_signage = True
    if large_print_materials == True:
        acc.large_print_materials = True
    if accessible_restrooms == True:
        acc.accessible_restrooms = True
    if hearing_assistance == True:
        acc.hearing_assistance = True
   




    print(wheelchair_accessible)

    
    image_1 = request.files.get('image_1')
    image_2 = request.files.get('image_2')
    image_3 = request.files.get('image_3')

    print(image_1)
    print(image_2)
    print(image_3)
    
    errors = {}

    if gem_name == '':
        errors['gem_name'] = 'Gem name is required'

    if gem_type == '':
        errors['gem_type'] = 'Gem type is required'

    if latitude == '':
        errors['latitude'] = 'Latitude is required'
    
    if longitude == '':
        errors['longitude'] = 'Longitude is required'
    
    #if the user doesnt provide any images, we will force them too
    if image_1 and image_2 and image_3:
        pass
    else:
        errors['images'] = 'Please provide 3 images'

    
    if errors == {}:
        
        gem_url = gem_repo.create_new_gem(gem_name, gem_type, longitude, latitude, True)
        gem_repo.change_accessibility(gem_url, acc)

        #uncomment the line below to make s3 work
        images_repository.create_hidden_gem_images(gem_url, image_1, image_2, image_3)
        
        return jsonify(
    {
        'message': 'Gem created successfully',
        'gem_id': gem_url
    })
    else:
        return jsonify(errors), 400
    
    

@user.post("/logout")
def logout():
    response = jsonify({"msg": "Logout successful"})
    unset_jwt_cookies(response)
    return response 



