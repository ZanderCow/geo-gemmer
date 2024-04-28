import repositories.gem_repository as gem_repo
import repositories.review_repository as review_repo
import repositories.gems_pinned_repository as gem_pinned_repo

import sys
from flask import Blueprint, render_template, redirect, request, jsonify
from math import ceil
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
import datetime
import os
import requests

gem = Blueprint('gem', __name__)



@gem.post('/search/')
def filtered_gem_search_page():
    search_query = request.args.get('searchbar', '')
    data = request.json

    if not search_query:
        # Handle the case where search_query is empty or not provided
        return redirect('/user')
    #TODO:
    #auethenticate user (user must be logged in to search for gems)
    #If user is not logged in, redirect to login page
    #get search query 
    #search for gems in database based on search query
    acc = gem_repo.accessibility_class()

    return render_template('gem-search.html', user_query=search_query)


@gem.post('/send-location')
@jwt_required()
def receive_location():
    user_id = get_jwt_identity()
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")
    # Process the data as needed
    return jsonify({'status': 'success'})

@gem.get('/Doom')
@jwt_required()
def egg():
    return render_template('gem-doomtails.html')

@gem.get('/<gem_id>')
@jwt_required()
def gem_details(gem_id):
    user_id = get_jwt_identity()
    #TODO:
    #auethenticate user (user must be logged in to view a gem)
    #If user is not logged in, redirect to login page
    #get gem details from database
    location = (-80.734436, 35.306274)
    if (gem_id is not None and gem_id != "None" and not gem_repo.is_not_uuid(gem_id)):
        gem_info = gem_repo.get_hidden_gem_by_id(gem_id, location[0], location[1])

        gem_average_rating = round(gem_info['avg_rat'] * 2) / 2

        full_stars = int(ceil(gem_average_rating))-1
        half_stars = ceil(gem_average_rating % 1)

        
        gem_reviews = review_repo.get_all_reviews_for_a_hidden_gem(gem_id)

        gem_review_distribution = calculate_gem_review_distribution(gem_reviews)
        normal_rev_dist = [0,0,0,0,0,0]

        if (gem_review_distribution[0] != 0):
            for i in range(len(gem_review_distribution)-1):
                normal_rev_dist[i] = round(100*(gem_review_distribution[i+1]/gem_review_distribution[0]), 1)

        #format it for stupid jinja
        gem_review_distribution = {
            "total": gem_review_distribution[0],
            "one": gem_review_distribution[1],
            "two": gem_review_distribution[2],
            "three": gem_review_distribution[3],
            "four": gem_review_distribution[4],
            "five": gem_review_distribution[5]
        }
        normal_rev_dist = {
            "one": normal_rev_dist[0],
            "two": normal_rev_dist[1],
            "three": normal_rev_dist[2],
            "four": normal_rev_dist[3],
            "five": normal_rev_dist[4]
        }

        return render_template('gem-details.html', 
            gem_basic_info= gem_info, 
            full_stars= full_stars,
            half_stars= half_stars,
            gem_review_distribution= gem_review_distribution,
            normalized_review_distribution= normal_rev_dist,
            gem_reviews= gem_reviews
        )
    return ""

def calculate_gem_review_distribution(reviews):
    distro = [0,0,0,0,0,0]
    for review in reviews:
        distro[review['rating']]+=1
        distro[0]+=1

    return distro

@gem.get('/<gem_id>/create-review')
@jwt_required()
def render_create_gem_review(gem_id):
    user_id = get_jwt_identity()
    #TODO:
    #auethenticate user (user must be logged create a review for a gem)
    #If user is not logged in, redirect to login page
    if (user_id is None):
        return redirect('/login')

    return render_template('add-hidden-gem-review.html', gem_id=gem_id)

@gem.post('/<gem_id>/create-review')
@jwt_required()
def create_create_gem_review(gem_id):
    user_id = get_jwt_identity()
    #TODO:
    #auethenticate user (user must be logged create a review for a gem)
    #If user is not logged in, redirect to login page
    
    if (user_id is None):
        return redirect('/login')
    
    data = request.get_json()  # get the incoming JSON data

    # list of fields that should not be empty
    required_fields = ['rating', 'review']

    missing_fields = [field for field in required_fields if not data.get(field)]

    if missing_fields or not data['rating'].isdigit():
        return jsonify({'error': f'The following fields are required and were not provided: {", ".join(missing_fields)}'}), 400  # 400 is the status code for "Bad Request"


    # make the gem review and go back to the gem page
    review_repo.add_review_to_hidden_gem(gem_id, user_id, int(data['rating']), data['review'])
    return jsonify(
    {
        'message': 'Gem created successfully',
    })

@gem.get('/<gem_id>/edit-review')
@jwt_required()
def render_edit_gem_review(gem_id):
    user_id = get_jwt_identity()
    
    #make sure user_id is the same as the user_id of the review

    
    #review_repo.get_review_by_id_and(gem_id)
    pass

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



@gem.get('/search/')
@jwt_required()
def gem_search_page():

    user_id = get_jwt_identity()

    # Retrieve string and numerical query parameters with defaults
    search_query = request.args.get('searchbar', default="", type=str)
    gem_type = request.args.get('type', default="", type=str)
    distance = request.args.get('distance', default=0, type=int)
    minimum_rating = request.args.get('minimum_rating', default=0, type=int)  # Corrected the typo here
    latitude = request.args.get('latitude', default=0.0, type=float)
    longitude = request.args.get('longitude', default=0.0, type=float)
    offset = request.args.get('offset', default=0, type=int)

   

    # Retrieve boolean query parameters with inline conversion
    wheelchair_accessible = request.args.get('wheelchair_accessible', 'false').lower() in ['true', '1', 't', 'yes']
    service_animal_friendly = request.args.get('service_animal_friendly', 'false').lower() in ['true', '1', 't', 'yes']
    multilingual_support = request.args.get('multilingual_support', 'false').lower() in ['true', '1', 't', 'yes']
    braille_signage = request.args.get('braille_signage', 'false').lower() in ['true', '1', 't', 'yes']
    hearing_assistance = request.args.get('hearing_assistance', 'false').lower() in ['true', '1', 't', 'yes']
    large_print_materials = request.args.get('large_print_materials', 'false').lower() in ['true', '1', 't', 'yes']
    accessible_restrooms = request.args.get('accessible_restrooms', 'false').lower() in ['true', '1', 't', 'yes']

    new_page = request.args.get('new_page', 'true').lower() in ['true', '1', 't'] # will be false 

    # if the user came from another page (they searched for a gem on the dashboard)
    if new_page == True:
        #return the search page ()
        return render_template("gem-search.html",search_query=search_query)
        
    # else the request is made from async js
    else:
        # if the request was made because the user reached the bottom of the page
        if offset != 0:
            lat = float(latitude)
            long = float(longitude)
            gems = gem_repo.get_all_gems_ordered_by_nearest(long, lat)
            # return new gems to the user using all the filters
            return jsonify(gems), 200 # placeholder, change this to be the gems search results from the database
            
        # else the user just loaded the page, or filtered the gems
        else:
            lat = float(latitude)
            long = float(longitude)
            gems = gem_repo.get_all_gems_ordered_by_nearest(long, lat)
            # return new gems to the user using all the filters
            return jsonify(gems), 200 # placeholder, change this to be the gems search results from the database


    
        

