from flask import Blueprint, render_template,redirect,request

main = Blueprint('main', __name__)

@main.route('/')
def home():
    return render_template('index.html')

@main.route('/about-us')
def about_us():
    return render_template('about-us.html')

@main.route('/faq')
def faq():
    return render_template('faq.html')

@main.route('/contact-us')
def contact_us():
    return render_template('contact-us.html')

@main.get('/employee-success')
def employee_success():
    return render_template('employee-success.html')

@main.get('/job-openings')
def job_openings():
    return render_template('job-openings.html')

@main.get('/benefits')
def benefits():
    return render_template('benefits.html')

@main.get('/our-company')
def our_company():
    return render_template('our-company.html')





@main.get('/404')
def four_0_four_error():
    return render_template('404.html')

@main.get('/unauthorized')
def unauthorized_error():
    return render_template('unauthorized.html')

@main.get('/forgot-password')
def forgot_password():
    return render_template('forgot-password.html')






@main.get('/sign-up')
def render_signup_page():
    # gets signup page
    return render_template('sign-up.html')

@main.post('/sign-up')
def signup_user():
    '''
    signs up user and redirects to dashboard
    '''
    email = request.form.get('email')
    password = request.form.get('password')

    #TODO:
    # check if user exists already
    #adds user to database
    #logs in user

    return redirect('/user')







@main.get('/login')
def get_login():
    # gets login page
    return render_template('login.html')

@main.post('/login')
def login_user():

    email = request.form.get('email')
    password = request.form.get('password')

    #TODO:
    # check if user exists
    # check if password is correct
    # if user does not exist or password is incorrect, return error message
    # if user exists and password is correct, log in user and redirect to dashboard
    #authenticates user
    return redirect('/user')


