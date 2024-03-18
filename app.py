from flask import Flask,render_template, redirect

app = Flask(__name__)


@app.route('/')
def hello():
    return render_template('index.html')

@app.route('/about-us')
def aboutus():
    return render_template('about-us.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/contact-us')
def contactus():
    return render_template('contact-us.html')

@app.get('/sign-up')
def get_signup():
    # gets signup page
    return render_template('sign-up.html')

@app.post('/sign-up')
def signup_user():
    # signs up user and redirects to dashboard


    return redirect('/dashboard')


@app.get('/login')
def get_login():
    # gets login page
    return render_template('login.html')

@app.post('/login')
def login_user():
    # logs in user and redirects to dashboard
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    '''
    Renders the user main menu page with the provided user data.

    Parameters:
    user_data (dict): A dictionary containing the user's data.

    Returns:
    The rendered user main menu page.
   '''
    


    user_data_example = {
        "username": "TheCowanPlayz",
        "first_name": "Zander",
        "last_name": "Cowan",
        "profile_picture": "../static/img/nature-image.png",
        "gems_explored": 5,
        "reviews_made": 0,
        "gems_created": 0,
        "gems_saved": 4,
       
        "gems_visited": [
            {
                "gem_name": "Rocky Mountain",
                "gem_type": "mountain",
                "date_visited": "2023-03-10",
            },
            {
                "gem_name": "slipper slope",
                "gem_type": "bar",
                "date_visited": "2023-04-10",
            },
            {
                "gem_name": "Diamond Lake",
                "gem_type": "lake",
                "date_visited": "2023-05-15"
            },
            {
                "gem_name": "Emerald Forest",
                "gem_type": "forest",
                "date_visited": "2023-06-20"
            },
            {
                "gem_name": "Sapphire Falls",
                "gem_type": "waterfall",
                "date_visited": "2023-07-25"
            }
        ],


        "gems_saved_details": [
            {
                "gem_name": "Rocky Mountain",
                "gem_type": "mountain",
                "website_link": "https://rockymountain.com",
            },
            {
                "gem_name": "slipper slope",
                "gem_type": "bar",
                "website_link": "https://slipperslope.com",
            }
        ],
                 
        "left_reviews": [
            {
                "rating": 4,
                "review": "this place is great as;lfkjsda;lfkas"
            },
            {
                "rating": 1,
                "review": "this place sucks fsdajk;lfsadjfklsda"
            }
        ]


    }
    return render_template('user-main-menu.html', user_data=user_data_example)

@app.get('/user-settings')
def userprofile():
    """
    This function returns the user profile data for rendering the user settings page.

    Returns:
        str: The rendered user settings HTML page with the user profile data.
    """

    user_settings_example = {
        "username": "TheCowanPlayz",
        "first_name": "Zander",
        "last_name": "Cowan",
        "email": "zandercowan01@gmail.com",
        "profile_picture": "../static/img/nature-image.png",
    }

    return render_template('user-settings.html', profile_data=user_settings_example)

@app.post('/user-settings')
def update_userprofile():
    """
    This function updates the user profile data and redirects to the user main menu page.

    Returns:
        str: The rendered user main menu HTML page.
    """

    return redirect('/dashboard')



@app.route('/search', methods=['GET', 'POST'])
def search():
    #change this to a search query
    gem_search_example = {



    }
    return render_template('gem-search.html')



@app.route('/gem-details', methods=['GET', 'POST'])
def gemdetails():

    
    gem_data_example = {
        "name": "Rocky Mountain",
        "gem_type": "mountain",
        "times_visited": 2035,
        "acessibilty": "elderly friendly, wheelchair unaccessible",
        "website_link": "http://rockymountain.com",

        "gem_images":{
            "image_1": "../static/img/nature-image.png",
            "image_2": "../static/img/nature-image.png",
            "image_3": "../static/img/Screenshot%202024-03-10%20at%203.40.09 PM.png",


        },              
        "reviews": [
            {
                "username": "gertrude123",
                "rating": 4,
                "review": "this place is great as;lfkjsda;lfkas"
            },
            {
                "username": "suzansmith",
                "rating": 1,
                "review": "this place sucks fsdajk;lfsadjfklsda"
            }
        ]
    }

    return render_template('gem-details.html', gem_data=gem_data_example)

if __name__ == '__main__':
    app.run(debug=True)



    
    
   