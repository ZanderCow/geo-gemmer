from flask import Blueprint, render_template,redirect,request

user = Blueprint('user', __name__)

@user.get('/')
def dashboard():
    #TODO:
    # get user data from database

    return render_template('dashboard.html')

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

