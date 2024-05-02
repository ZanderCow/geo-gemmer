import repositories.gem_repository as gem_repo
import repositories.review_repository as review_repo
import repositories.gems_pinned_repository as gem_pinned_repo
import repositories.images_repository as images_repository
from repositories.gem_accessibility_repository import get_accesibility_for_hidden_gem
import repositories.gems_visited_repository as visited_repo
import repositories.gem_accessibility_repository as gem_accessibility_repository
from repositories import user_repository
from repositories.user_repository import increment_reviews_made
import sys
from flask import Blueprint, render_template, redirect, request, jsonify
from math import ceil
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
import datetime
import os
import requests
import base64

gem = Blueprint('gem', __name__)

@gem.get('/search/')
@jwt_required()
def gem_search_page():
    user_id = get_jwt_identity()
    return render_template("gem-search.html")

@gem.get('/search-for-gems/')
@jwt_required()
def search_for_gems():
    user_id = get_jwt_identity()
    search_query = request.args.get('searchbar', default=None, type=str)
    gem_type = request.args.get('type', default="", type=str)
    distance = request.args.get('distance', default=0, type=int)
    minimum_rating = request.args.get('minimum_rating', default=0, type=int)
    latitude = request.args.get('latitude', default=0.0, type=float)
    longitude = request.args.get('longitude', default=0.0, type=float)
    offset = request.args.get('offset', default=0, type=int)
    new_page = request.args.get('new_page', 'false').lower() == 'true'
    

    # Retrieve boolean accessibility parameters
    accessibility_conditions = {name: request.args.get(name, 'false').lower() == 'true'
                                for name in ['wheelchair_accessible', 'service_animal_friendly',
                                             'multilingual_support', 'braille_signage', 
                                             'hearing_assistance', 'large_print_materials', 
                                             'accessible_restrooms']}
    gems = gem_repo.search_for_gems(
        search_bar=search_query,
        gem_type=gem_type,
        distance=distance,
        off_set=offset,
        lat=latitude,
        long=longitude,
        wheelchair_accessible=accessibility_conditions['wheelchair_accessible'],
        service_animal_friendly=accessibility_conditions['service_animal_friendly'],
        multilingual_support=accessibility_conditions['multilingual_support'],
        braille_signage=accessibility_conditions['braille_signage'],
        hearing_assistance=accessibility_conditions['hearing_assistance'],
        large_print_materials=accessibility_conditions['large_print_materials'],
        accessible_restrooms=accessibility_conditions['accessible_restrooms'],

        
    )
    
    return jsonify(gems), 200
      

@gem.get('/Doom')
@jwt_required()
def egg():
    return render_template('gem-doomtails.html')


@gem.get('/<gem_id>')
@jwt_required()
def gem_details(gem_id):
    user_id = get_jwt_identity()
    return render_template('gem-details.html')
            

@gem.get('/<gem_id>/create-review')
@jwt_required()
def render_create_gem_review(gem_id):
    gem_name = gem_repo.get_gem_header(gem_id)[0]['name']
    user_id = get_jwt_identity()
    return render_template('add-hidden-gem-review.html', gem_id=gem_id, gem_name=gem_name)


@gem.post('/<gem_id>/create-review')
@jwt_required()
def create_create_gem_review(gem_id):
    user_id = get_jwt_identity()
    data = request.get_json()  # get the incoming JSON data

    required_fields = ['rating', 'review']

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields or not data['rating'].isdigit():
        return jsonify({'error': f'The following fields are required and were not provided: {", ".join(missing_fields)}'}), 400  # 400 is the status code for "Bad Request"


    # make the gem review and go back to the gem page
    review_repo.add_review_to_hidden_gem(gem_id, user_id, int(data['rating']), data['review'])
    increment_reviews_made(user_id)
    return jsonify({'message': 'Gem created successfully',
    })


@gem.get("/success/<gemid>")
@jwt_required()
def success(gemid:str):
    user_id = get_jwt_identity()
    return render_template("gem-success.html", gemid=gemid)


@gem.post('/<gem_id>/pin')
@jwt_required()
def pin_gem(gem_id):
    user_id = get_jwt_identity()
    current_date = datetime.date.today()
    user_repository.increment_gems_saved(user_id)
    gem_pinned = gem_pinned_repo.add_pinned_gem(user_id, gem_id, current_date)

    if gem_pinned == "gem already pinned":
        return jsonify({'error': 'gem already pinned'}), 400

    return jsonify(
        {'message': 'gem pinned successfully'}), 200


@gem.route('/map')
@jwt_required()
def proxy_maps_request():
    latitude = request.args.get('lat', default='-34.397')
    longitude = request.args.get('lng', default='150.644')
    callback = request.args.get('callback', default='initMap')

    google_maps_api_key = os.getenv('GOOGLE_MAPS_API_KEY')
    maps_endpoint = 'https://maps.googleapis.com/maps/api/js'

    # Fetch Google Maps JS API
    response = requests.get(f"{maps_endpoint}?key={google_maps_api_key}&callback={callback}")

    # Generate custom JS with proper map options and callback definition
    custom_js = f"""
    {response.text}
    function {callback}() {{
        var mapOptions = {{
            center: new google.maps.LatLng({latitude}, {longitude}),
            zoom: 13
        }};
        var map = new google.maps.Map(document.getElementById('map'), mapOptions);
    }}
    """
    return custom_js, 200, {'Content-Type': 'application/javascript'}


@gem.get('/<gem_id>/get-primary-gem-image')
@jwt_required()
def get_primary_image_for_gem(gem_id):
    user_id = get_jwt_identity()

    image_bytes = None
    image_bytes = images_repository.get_primary_image_for_hidden_gem(gem_id)
    base64_encoded_data = base64.b64encode(image_bytes)
    base64_image = base64_encoded_data.decode('utf-8')
    return jsonify(base64_image), 200


@gem.get('/<gem_id>/get-all-gem-images')
@jwt_required()
def get_all_images_for_gem(gem_id):
    user_id = get_jwt_identity()

    
    images = []
    image_bytes = images_repository.get_hidden_gem_images(gem_id)
    for image in image_bytes:
        base64_encoded_data = base64.b64encode(image)
        base64_image = base64_encoded_data.decode('utf-8')
        images.append(base64_image)
    return jsonify(images), 200

@gem.get("/<gem_id>/get-header-info")
@jwt_required()
def get_header_info(gem_id):
    user_id = get_jwt_identity()
    gem =  gem_repo.get_gem_header(gem_id)
    return jsonify(gem), 200


@gem.get('/<gem_id>/get-average-rating')
@jwt_required()
def get_average_rating(gem_id):
    user_id = get_jwt_identity()
    average_rating = review_repo.get_average_rating_for_hidden_gem(gem_id)
    return jsonify(average_rating), 200


@gem.get('/<gem_id>/get-basic-gem-info')
@jwt_required()
def get_gem_details(gem_id):
    user_id = get_jwt_identity()
    gem = gem_repo.get_basic_gem_info(gem_id)
    return jsonify(gem), 200


@gem.get('/<gem_id>/get-accessibility-features')
@jwt_required()
def get_accesibility_features(gem_id):
   accesibility_features = get_accesibility_for_hidden_gem(gem_id)
   return jsonify(accesibility_features), 200


@gem.get('/<gem_id>/get-rating-distribution')
@jwt_required()
def get_rating_distribution(gem_id):

    gem_review_distribution = review_repo.get_gem_review_distribution(gem_id)
    
    return jsonify(gem_review_distribution), 200


@gem.get('/<gem_id>/get-reviews')
@jwt_required()
def get_gem_reviews(gem_id):
    reviews = review_repo.get_all_reviews_for_a_hidden_gem(gem_id)
    return jsonify(reviews), 200


@gem.get("/<gem_id>/edit-gem")
@jwt_required()
def edit_gem(gem_id):
    user_id = get_jwt_identity()
    gem_creator = gem_repo.get_gem_creator(gem_id)
    return render_template("edit-hidden-gem.html")


#TODO make this a patch request
@gem.post('/<gem_id>/edit-gem')
@jwt_required()
def confirm_edit_gem(gem_id):
    """
    Create a new gem in the database based on the incoming JSON data.

    Returns:
        A JSON response containing a success message and the URL of the created gem.
    """
    user_id = get_jwt_identity()
    gem_creator = gem_repo.get_gem_creator(gem_id)

    if gem_creator != user_id:
        return jsonify({'error': 'You are not the creator of this gem'}), 403


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
    print(image_1)
    print(image_2)
    print(image_3)
    
    current_accessibility = gem_accessibility_repository.get_accesibility_for_hidden_gem(gem_id)
    

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
    
    errors = {}
    update_image = False
    if latitude == '':
        errors['latitude'] = 'Latitude is required'

    if longitude == '':
        errors['longitude'] = 'Longitude is required'
    if gem_name == '':
        errors['gem_name'] = 'Gem name is required'
    if gem_type == '':
        errors['gem_type'] = 'Gem type is required'
    if image_1 == None:
        errors['image_1'] = 'Image 1 is required'
    if image_2 == None:
        errors['image_2'] = 'Image 2 is required'
    if image_3 == None:
        errors['image_3'] = 'Image 3 is required'

    if errors == {}:

        #grab current gem info, compare it what the user has
        # if any of them are the same, dont change that value

        current_gem_info = gem_repo.get_basic_gem_info(gem_id)
    
        print(current_gem_info[0]['name'])
        print(current_gem_info[0]['gem_type'])

        if current_gem_info[0]['name'] != gem_name:
            gem_repo.change_gem_name(gem_id, gem_name)
        if current_gem_info[0]['gem_type'] != gem_type:
            gem_repo.change_gem_type(gem_id, gem_type)
        
        #one of the old ones. the artefacts of the original version of this project
        #before the Great Rewrite the week it is due. That is why longitude comes before latitude
        gem_repo.change_gem_location(gem_id, longitude, latitude)


        gem_accessibility_repository.set_accesibility_for_gem(
            gem_id, 
            wheelchair_accessible,
            service_animal_friendly,
            multilingual_support,
            braille_signage,
            hearing_assistance,
            large_print_materials,
            accessible_restrooms
        )

        #uncomment the line below to make s3 work
        #images_repository.update_gem_images(gem_id, image_1, image_2, image_3) 

        
        return jsonify(
    {
        'message': 'Gem edited successfully',
        'gem_id': gem_id 
    })
    else:
        return jsonify(errors), 400
    


@gem.delete("/delete-gem")
@jwt_required()
def delete_gem():
    user_id = get_jwt_identity()
    data = request.get_json()
    gem_id = data['gem_id']
    gem_creator = gem_repo.get_gem_creator(gem_id)
    if gem_creator != user_id:
        return jsonify({'error': 'You are not the creator of this gem'}), 403
    images_repository.delete_gem_images(gem_id)
    gem_repo.delete_gem(gem_id)
    return jsonify({'message': 'Gem deleted successfully'}), 200
    


@gem.route("/<gem_id>/get-distance-from-user/")
@jwt_required()
def get_distance_from_user(gem_id):
    latitude = request.args.get('lat', default='-34.397')
    longitude = request.args.get('lng', default='150.644')
    user_id = get_jwt_identity()
    distance = gem_repo.get_gem_distance_from_user(gem_id, latitude, longitude)
    return jsonify(distance), 200


@gem.post('/<gem_id>/visit')
@jwt_required()
def visiting(gem_id):
    user_id = get_jwt_identity()
    current_date = datetime.date.today()
    visited_repo.add_gem_to_visited_list(user_id, gem_id, current_date)