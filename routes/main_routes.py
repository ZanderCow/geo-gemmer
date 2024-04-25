from flask import Blueprint, render_template,redirect,request, jsonify
from repositories import user_repository
import bcrypt
from flask_jwt_extended import JWTManager, create_access_token, set_access_cookies, jwt_required, get_jwt_identity
from datetime import timedelta

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

    data = request.get_json()  # get the incoming JSON data


    created_username = data.get('username')
    created_password = data.get('password')

    errors = {}

    if user_repository.does_username_exist(created_username):
        errors['username'] = 'Username already exists'

    
    if created_username == '':
        errors['username'] = 'Username is required'


    if created_password == '':
        errors['password'] = 'Password is required'


    

    # if there are no errors, create the user
    if errors == {}:
         user_id = user_repository.create_new_user(created_username, created_password)
         return jsonify({'message': 'user created successfully'}), 200
    
    else:
        return jsonify(errors), 400
    










@main.get('/login')
def get_login():
    # gets login page
    return render_template('login.html')

@main.post('/login')
def login_user():

    data = request.get_json()  # get the incoming JSON data


    entered_username = data.get('username')
    entered_password = data.get('password')

    errors = {}

    if entered_username == '':
        errors['error'] = 'username or password is incorrect'
    if entered_password == '':
        errors['error'] = 'username or password is incorrect'
    else: 
        if not user_repository.does_username_exist(entered_username):
            errors['error'] = 'username or password is incorrect'
        else:
            actual_password = user_repository.get_password(entered_username)["password"]


            if bcrypt.checkpw(entered_password.encode('utf-8'), actual_password):
                user_id = user_repository.get_userid_by_username(entered_username)
                access_token = create_access_token(identity=str(user_id),expires_delta=timedelta(days=7))
                response = jsonify(
                    {'login': True},
                    {'username': entered_username}
                    )
                set_access_cookies(response, access_token)
                return response
            
            else:
                errors['error'] = 'username or password is incorrect'
 
    return jsonify(errors), 400   
        


@main.route('/we-need-your-location')
def location():
    return render_template('user-needs-to-allow-location.html')
