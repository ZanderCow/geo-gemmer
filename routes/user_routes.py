from flask import Blueprint, render_template,redirect,request,jsonify, session
from repositories import user_repository, gems_pinned_repository, gems_visited_repository

user = Blueprint('user', __name__)

@user.get('/')
def dashboard():
    #TODO:
    # get user data from database
    # get user hidden gems from database

    user_id = request.args.get('user_id')
    user_info = user_repository.get_user_by_id(user_id)

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


    return render_template('dashboard.html', user_info=user_info, gem_visted_frequency=gem_visted_frequency, gem_distribution=gem_distribution, gems_pinned=gems_pinned, reviews_made=reviews_made)

@user.post('/logout')
def logout():
    #TODO:
    # logout user
    return redirect('/')


@user.get('/settings')
def render_settings_page():
    #TODO:
    # get user settings data from database

    user_id = request.args.get('user_id')
    user_settings = user_repository.get_user_settings_details(user_id)

    return render_template('user-settings.html', user_settings=user_settings)

@user.post('/settings')
def change_settings_page():
    #TODO:
    # update user settings data in database

    user_id = request.args.get('user_id')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    user_repository.change_user_settings(user_id, first_name, last_name)

    return render_template('user-settings.html', message='Settings updated successfully')

@user.get('/create-gem')
def render_create_gem_page():
    return render_template('create-hidden-gem.html')

@user.post('/create-gem')
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

    return jsonify(
    {
        'message': 'Gem created successfully',
        'gem_url': '/gem/67e55044-10b1-426f-9247-bb680e5fe0c8'
    }
)

