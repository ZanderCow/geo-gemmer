from flask import Blueprint, render_template,redirect,request

user = Blueprint('user', __name__)

@user.get('/')
def dashboard():
    #TODO:
    # get user data from database
    # get user hidden gems from database

    user_info = {
        'user_name': 'TheCowanPlayz',
        'profile_picture': 'amazons3.com/cool-profile-picture',
        'gems_explored': 1030023908,
        'reviews_made': 5349084350,
        'gems_created': 334098534,
        'gems_saved': 230495830495834
    }

    gem_visted_frequency = {
        'January': 2,
        'February': 1,
        'March': 3,
        'April': 2,
        'May': 1,
        'June': 1,
        'July': 1,
        'August': 1,
        'September': 1,
        'October': 1,
        'November': 10,
        'December': 1
    }


    gem_distribution = {
            'Restaurant': 2,
            'Park': 1,
            'Museum': 1,
            'Beach': 1,
            'Trail': 1,
            'Bar': 1,
            'Hotel': 1,
            'Store': 1,
    
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
    return render_template('user-settings.html')

@user.post('/settings')
def change_settings_page():
    #TODO:
    # update user settings data in database
    return render_template('user-settings.html')






@user.get('/create-gem')
def render_create_gem_page():
    return render_template('create-hidden-gem.html')

@user.post('/create-gem')
def create_gem():
    #TODO:
    # create gem in database
    return render_template('about.html')

