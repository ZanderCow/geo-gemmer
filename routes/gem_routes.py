from flask import Blueprint, render_template,redirect,request,jsonify
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
    searched_gems = [
        {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
            'name': 'fuck you bitch', 
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
    ]
    return render_template('gem-search.html',gem_data=searched_gems, user_query="rocky mountain")

@gem.post('/send-location')
def receive_location():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']
    print(f"Received location: Latitude = {latitude}, Longitude = {longitude}")
    # Process the data as needed
    return jsonify({'status': 'success'})


def gem_details(gem_id):
    #TODO:
    #auethenticate user (user must be logged in to view a gem)
    #If user is not logged in, redirect to login page
    #get gem details from database

    gem_images = {
        "image_1": "/static/img/nature-image.png",
        "image_2": "/static/img/nature-image.png",
        "image_3": "/static/img/nature-image.png",
    }

    gem_average_rating_in_float = 4.3
    gem_average_rating = round(gem_average_rating_in_float * 2) / 2

    full_stars = int((gem_average_rating // 1))
    half_stars = ceil(gem_average_rating % 1)


    
    gem_info =  { 
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
          }

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
    print(formatted_gem_review_cdf)


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
        gem_average_rating_in_float=gem_average_rating_in_float,
        gem_accessibility_info=gem_accessibility_info, 
        gem_review_distribution=gem_review_distribution,
        formatted_gem_review_cdf=formatted_gem_review_cdf,
        gem_reviews=gem_reviews
        )





@gem.get('/<gem_id>/create-review')
def render_create_gem_review():
    #TODO:
    #auethenticate user (user must be logged create a review for a gem)
    #If user is not logged in, redirect to login page

    return render_template('add-hidden-gem-review.html')

@gem.post('/<gem_id>/create-review')
def create_gem_review():
    #TODO:
    #auethenticate user (user must be logged in to create a review for a gem)
    #If user is not logged in, redirect to login page

    return render_template('gem-details.html')