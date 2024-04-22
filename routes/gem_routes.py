from flask import Blueprint, render_template,redirect,request,jsonify
import repositories.gem_repository as gem_repo
from math import ceil

gem = Blueprint('gem', __name__)

@gem.get('/search/')
def gem_search_page():
    search_query = request.args.get('searchbar', '')

    if not search_query:
        # Handle the case where search_query is empty or not provided
        return redirect('/user')

    #TODO:
    #auethenticate user (user must be logged in to search for gems)
    #If user is not logged in, redirect to login page
    #get search query 
    #search for gems in database based on search query
    location = (-80.734436, 35.306274)
    searched_gems = gem_repo.search_all_gems_within_a_certain_distance_from_the_user(search_query, location[0], location[1], 50)
    '''[
        {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
            'name': 'Lorem ipsum, dolor sit amet consectetur',
            "image" : "/static/img/nature-image.png",
            'distance_from_user': 20.3346,
            'type': 'hiking Trail'
            
        },
        {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
            'name': 'Rocky Mountian',
            "distance_from_user" : 20.3346,
            'type': 'hiking Trail'
        },
        {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
            'name': 'Rocky Mountian',
            "distance_from_user" : 20.3346,
            'type': 'hiking Trail'
        },
        {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
            'name': 'Rocky Mountian',
            "distance_from_user" : 20.3346,
            'type': 'hiking Trail'
        }           
    ]'''
    return render_template('gem-search.html',gem_data=searched_gems, user_query=search_query)

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
    print(data)
    acc = gem_repo.accessibility_class()

    location = (-80.734436, 35.306274)
    searched_gems = gem_repo.filtered_search_all_gems_within_a_certain_distance_from_the_user(search_query, location[0], location[1], 50, None, acc, 0, 0)
    return render_template('gem-search.html',gem_data=searched_gems, user_query=search_query)


@gem.post('/send-location')
def receive_location():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")
    # Process the data as needed
    return jsonify({'status': 'success'})

@gem.get('/<gem_id>')
def gem_details(gem_id):
    #TODO:
    #auethenticate user (user must be logged in to view a gem)
    #If user is not logged in, redirect to login page
    #get gem details from database
    location = (-80.734436, 35.306274)
    gem_info = gem_repo.get_hidden_gem_by_id(gem_id, location[0], location[1])
    gem_images = {
        "image_1": gem_info['image_1'],
        "image_2": gem_info['image_2'],
        "image_3": gem_info['image_3'],
    }

    gem_average_rating = round(gem_info['avg_rat'] * 2) / 2

    full_stars = int((gem_average_rating // 1))
    half_stars = ceil(gem_average_rating % 1)


    
    '''gem_info =  { 
            "gem_id": "67e55044-10b1-426f-9247-bb680e5fe0c8",
            'name': 'hello',
            'type': 'hiking Trail',
            'distance_from_user': 20.3346,
            'times_visited': 2,
        }
    

    
    gem_accessibility_info = {
        "wheelchair_accessible": True,
        "service_animal_friendly": True,
        "multilingual_support": True,
        "braille_signage": True,
        "hearing_assistance": True,
        "large_print_materials": True,   
    }'''

    gem_review_distribution = {
        "one": 2,
        "two": 3,
        "three": 4,
        "four": 5,
        "five": 5,
        "total_reviews": 19
    }
    
    gem_review_cdf = {
        "one": 0.1,
        "two": 0.2,
        "three": 0.3,
        "four": 0.4,
        "five": 0.5,
    }

    formatted_gem_review_cdf = {k: f"{v:.0%}" for k, v in gem_review_cdf.items()}


    gem_reviews = [
    
        {
            'user_name': 'Sally', 
            "pfp": "/static/img/grandma.png",
            'rating': 4,
            'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
        }, 
        {
        'user_name': 'Zander',
        "pfp": "/static/img/neckbeard.png",
        'rating': 1,
        'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
        }
    ]

    formatted_gem_review_cdf = {k: f"{v:.0%}" for k, v in gem_review_cdf.items()}
    return render_template('gem-details.html', 
        gem_basic_info=gem_info, 
        gem_images=gem_images, 
        full_stars=full_stars,
        half_stars=half_stars,
        gem_review_distribution=gem_review_distribution,
        formatted_gem_review_cdf=formatted_gem_review_cdf,
        gem_reviews=gem_reviews
        )


@gem.get('/<gem_id>/create-review')
def render_create_gem_review(gem_id):
    #TODO:
    #auethenticate user (user must be logged create a review for a gem)
    #If user is not logged in, redirect to login page

    return render_template('add-hidden-gem-review.html')


@gem.get('/<gem_id>/edit-review')
def render_edit_gem_review(gem_id):
    pass

@gem.get("/success/<gemid>")
def success(gemid:str):
    return render_template("gem-success.html", gemid=gemid)
