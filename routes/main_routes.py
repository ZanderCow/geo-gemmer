from flask import Blueprint, render_template,redirect,request, jsonify
from repositories import user_repository
import bcrypt
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity

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

    required_fields = ['username', 'password']

    created_username = data.get('username')
    created_password = data.get('password')
  

    missing_fields = [field for field in required_fields if not data.get(field)]

    #check if all required fields are provided
    if missing_fields:
        return jsonify({'error': f'The following fields are required and were not provided: {", ".join(missing_fields)}'}), 400  # 400 is the status code for "Bad Request"

    #check if username already exists
    if user_repository.does_username_exist(created_username):
        return jsonify({'error': 'Username already exists'}), 400
    

    user_id = user_repository.create_new_user(created_username, created_password)

    return jsonify({'message': 'Gem created successfully'}), 200








@main.get('/login')
def get_login():
    # gets login page
    return render_template('login.html')

@main.post('/login')
def login_user():

    username = request.json.get('username', None)
    password = request.json.get('password', None)

    #TODO:
    # check if password is correct
    stored_password = user_repository.get_password(username)
    if bcrypt.checkpw(password.encode('utf-8'), stored_password.encode('utf-8')):

        user_id = user_repository.get_user_id(username)
        access_token = create_access_token(identity=str(user_id))
        return jsonify(access_token=access_token), 200
    else:
        return jsonify({"msg": "Bad username or password"}), 401



