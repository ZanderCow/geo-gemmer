from flask import Flask,render_template, redirect, request

app = Flask(__name__)


@app.route('/')
def home():
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


@app.get('/sign-in')
def get_login():
    # gets login page
    return render_template('sign-in.html')

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
    
   
    return render_template('user-main-menu.html')

@app.get('/user-settings')
def userprofile():
    """
    This function returns the user profile data for rendering the user settings page.

    Returns:
        str: The rendered user settings HTML page with the user profile data.
    """


    return render_template('user-settings.html')

@app.post('/user-settings')
def update_userprofile():
    """
    This function updates the user profile data and redirects to the user main menu page.

    Returns:
        str: The rendered user main menu HTML page.
    """

    return redirect('/dashboard')



@app.get('/search')
def search():
    return render_template('gem-search.html')



'''
this is for later. to when we need to setup the search query correctly 
@app.get('/search/<search_query>')
def search():
    return render_template('gem-search.html')
'''


@app.route('/gem-details', methods=['GET', 'POST'])
def gemdetails():
    return render_template('gem-details.html')

'''
this is for later, when we setup the search query correctly

@app.get('/search/<gem_id>')
def gemdetails():
  
    return render_template('gem-details.html', gem_data=gem_data_example)
'''

if __name__ == '__main__':
    app.run(debug=True)



    
    
   