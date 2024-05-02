from flask import Blueprint, render_template,redirect,request,jsonify, session
from repositories import user_repository
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from repositories import user_repository, gem_repository as gem_repo
from repositories import user_repository, gems_pinned_repository, gems_visited_repository
from repositories import images_repository
from repositories import gem_accessibility_repository
import base64


from repositories import review_repository
import datetime

user = Blueprint('user', __name__)



@user.get('/')
@jwt_required()
def dashboard():
    #TODO:
    # get user data from database
    # get user hidden gems from database
    user_id = get_jwt_identity()  # Retrieves the identity from the JWT

    return render_template('dashboard.html')




@user.get('/settings')
@jwt_required()
def render_settings_page():
    user_id = get_jwt_identity()  # Retrieves the identity from the JWT
    user = user_repository.get_user_by_id(user_id)
    bio = user_repository.get_user_bio(user_id)
    
    return render_template('user-settings.html', user=user, bio=bio)


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
    

    acc = gem_accessibility_repository.accessibility_class()

    if wheelchair_accessible == 'true':
        acc.wheelchair_accessible = True
    if service_animal_friendly == 'true':
        acc.service_animal_friendly = True
    if multilingual_support == 'true':
        acc.multilingual_support = True
    if braille_signage == 'true':
        acc.braille_signage = True
    if large_print_materials == 'true':
        acc.large_print_materials = True
    if accessible_restrooms == 'true':
        acc.accessible_restrooms = True
    if hearing_assistance == 'true':
        acc.hearing_assistance = True
    
    image_1 = request.files.get('image_1')
    image_2 = request.files.get('image_2')
    image_3 = request.files.get('image_3')

    errors = {}

    if gem_name == '':
        errors['gem_name'] = 'Gem name is required'

    if gem_type == '':
        errors['gem_type'] = 'Gem type is required'

    if latitude == '':
        errors['latitude'] = 'Latitude is required'
    
    if longitude == '':
        errors['longitude'] = 'Longitude is required'
    

    print(acc.update_string())
    print('newy\nnewy\nnewy')
    if errors == {}:
        
        gem_url = gem_repo.create_new_gem(gem_name, gem_type, latitude=latitude, longitude=longitude, user_id=user_id)
        gem_accessibility_repository.set_accesibility_for_hidden_gem(gem_url, acc)

        #uncomment the line below to make s3 work
        images_repository.create_hidden_gem_images(gem_url, image_1, image_2, image_3) 

        user_repository.increment_gems_created(user_id)
        
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






@user.get("/get-basic-user-info")
@jwt_required()
def get_basic_user_info():
    '''
    Get the basic information of the user

    their name
    # of gems explored, 
    # of reviews made, 
    # of gems created, 
    and gems pinned
    '''
    user_id = get_jwt_identity()
    user_info = user_repository.get_user_by_id(user_id)

    return jsonify(user_info), 200


@user.get("/get-gems-overview")
@jwt_required()
def get_gems_overview():
    '''
    Get the gems overview of the user stuff

    their name
    # of gems explored, 
    # of reviews made, 
    # of gems created, 
    and gems pinned
    '''
    user_id = get_jwt_identity()
    gem_visted_frequency = gems_visited_repository.get_hidden_gems_visited_by_month(user_id)
   

    return jsonify(gem_visted_frequency), 200


@user.get("/get-gems-details")
@jwt_required()
def get_gems_details():
    user_id = get_jwt_identity()
    gem_distribution = gems_visited_repository.get_distribution_of_hidden_gems_visited_by_a_user(user_id)
    return jsonify(gem_distribution), 200


@user.get("/get-gems-pinned")
@jwt_required()
def get_gems_pinned():
    user_id = get_jwt_identity()
    gems_pinned = gems_pinned_repository.get_gems_pinned_by_user(user_id)
    return jsonify(gems_pinned), 200

@user.get("/get-reviews-made")
@jwt_required()
def get_reviews_made():
    user_id = get_jwt_identity()
    reviews_made = review_repository.get_all_reviews_user_has_made(user_id)
    return jsonify(reviews_made), 200


@user.get("/get-gems-created")
@jwt_required()
def get_gems_created():
    user_id = get_jwt_identity()
    gems_created = gem_repo.get_gems_created_by_user(user_id)
    return jsonify(gems_created), 200

@user.delete("/delete-gem/<gem_id>")
@jwt_required()
def delete_gem(gem_id):
    user_id = get_jwt_identity()
    gems_pinned_repository.delete_pinned_gem_user(user_id, gem_id)
    return jsonify({'message': 'Gem deleted successfully'}), 200


@user.get("/navbar-get-username")
@jwt_required()
def get_username():
    user_id = get_jwt_identity()
    username = user_repository.get_username_by_id(user_id)
    username['user_id'] = user_id
    return jsonify(username), 200

@user.get("/get-pfp")
@jwt_required()
def get_user_pfp():
    user_id = get_jwt_identity()
    try:

        image_bytes = None
        image_bytes = images_repository.get_user_pfp(user_id)
        base64_encoded_data = base64.b64encode(image_bytes)
        base64_image = base64_encoded_data.decode('utf-8')
        return jsonify(base64_image), 200
    except:
        return jsonify({'error': 'No profile picture found'}), 404
    
@user.get("/get-user-settings-info")
@jwt_required()
def get_user_settings_info():
    user_id = get_jwt_identity()
    user_settings = user_repository.get_user_settings_details(user_id)
    return jsonify(user_settings), 200

@user.post("/update-user-settings")
@jwt_required()
def update_user_settings():
    user_id = get_jwt_identity()
    file = request.files.get('file')
    user_name = request.form.get('username')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    bio = request.form.get('bio')

    errors = {}
    user = user_repository.get_user_by_id(user_id)
    

    #user filled out the username field
    if user_name != '':
        #check if the username is already taken
        if user_repository.does_username_exist(user_name):
            errors['username'] = 'Username already exists'
        else:
            user_repository.change_username(user_id, user_name)

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
            images_repository.update_user_pfp(user_id, file)
            pass
        
        else:
            #uncomment the line below to make s3 work 
            images_repository.create_user_pfp(user_id, file)
            pass

    if (bio != None):
        user_repository.change_user_bio(user_id, bio)
   
    if errors == {}:
        return jsonify(
            {
            'message': 'Settings updated successfully',
            'username': user_name,
             }
            ), 200
    else:
        return jsonify(errors), 400
    


@user.post("/add-visited-gem")
@jwt_required()
def gem_visited():
    user_id = get_jwt_identity()
    gem_id = request.form.get('gem_id')
    date_visited = datetime.datetime.now().strftime('%Y-%m-%d')
    gems_visited_repository.add_gem_to_visited_list(user_id, gem_id, date_visited)
    user_repository.increment_gems_explored(user_id)
    gem_repo.increment_gem_times_visited(gem_id)
    cordinates = gem_repo.get_cordinates(gem_id)
    print(cordinates)
    return jsonify(
        {'message': 'Gem added to visited list',
         "latitude": cordinates[0]["latitude"],
         "longitude": cordinates[0]["longitude"]
         }
         ), 200


@user.get('/<user_id>')
@jwt_required()
def profile(user_id):
    ur_user_id = get_jwt_identity()  # Retrieves the identity from the JWT
    if ur_user_id is None:
        return redirect('/')

    # get user data from database
    if (gem_repo.is_not_uuid(user_id)):
        return redirect('/user')
    user_info = user_repository.get_user_by_id(user_id)
    if (user_info is None or len(user_info) == 0):
        return redirect('/user')

    gem_visted_frequency = gems_visited_repository.get_hidden_gems_visited_by_month(user_id)
    gem_distribution = gems_visited_repository.get_distribution_of_hidden_gems_visited_by_a_user(user_id)
    gems_pinned = gems_pinned_repository.get_gems_pinned_by_user(user_id)
    reviews_made = review_repository.get_recent_reviews_user_has_made(user_id)
    bio = user_repository.get_user_bio(user_id)
    
    return render_template('user-profile.html', 
        user_info=user_info,
        username="username",
        bio=bio,
        gem_visted_frequency=gem_visted_frequency,
        gem_distribution=gem_distribution,
        gems_pinned=gems_pinned,
        reviews_made=reviews_made
    )

@user.delete('/delete-account')
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    images_repository.delete_pfp(user_id)
    user_repository.delete_user_by_id(user_id)
    response = jsonify({"msg": "deletion successful"})
    unset_jwt_cookies(response)
    return response, 200

@user.get('/setup')
@jwt_required()
def user_setup():
    user_id = get_jwt_identity()
    return render_template('user-setup.html')

@user.post('/setup')
@jwt_required()
def setup_the_user():
    user_id = get_jwt_identity()
    file = request.files.get('file')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    bio = request.form.get('bio')

    errors = {}
    user = user_repository.get_user_by_id(user_id)

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
            images_repository.update_user_pfp(user_id, file)
        
        else:
            #uncomment the line below to make s3 work 
            images_repository.create_user_pfp(user_id, file)
            pass

    if (bio != None):
        user_repository.change_user_bio(user_id, bio)
   
    if errors == {}:
        return jsonify(
            {
            'message': 'Profile set successfully',
             }
            ), 200
    else:
        return jsonify(errors), 400
    


