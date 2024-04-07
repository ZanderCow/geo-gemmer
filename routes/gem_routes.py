from flask import Blueprint, render_template,redirect,request

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

    return render_template('gem-search.html')

@gem.get('/<gem_id>')
def gem_details():
    #TODO:
    #auethenticate user (user must be logged in to view a gem)
    #If user is not logged in, redirect to login page
    #get gem details from database

    return render_template('gem-details.html')





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