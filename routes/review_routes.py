from flask import Blueprint, render_template,redirect,request,jsonify, session
from flask_jwt_extended import jwt_required, get_jwt_identity, unset_jwt_cookies
from repositories import review_repository


review = Blueprint('review', __name__)

@review.get('/<review_id>/edit-review')
@jwt_required()
def edit_review(review_id):
    user_id = get_jwt_identity()  # Retrieves the identity from the JWT
    # grab the review from the database
    review_data = review_repository.get_review_by_review_id(review_id)

    print(review_data)
    # see if the user for the review is the same as the user that is logged in
    # if not, redirect to the dashboard

    # if the user is the same, render the edit review page with the review data
    return render_template('edit-hidden-gem-review.html', review_data=review_data)


@review.post('/<review_id>/edit-review')
@jwt_required()
def sumbit_edit_review(review_id):
    

    user_id = get_jwt_identity()
    data = request.get_json()

    edited_rating = data.get('rating')
    edited_review = data.get('review')

    errors = {}

    #user filled out the rating
    if edited_rating != '':

        #try to convert to a int and add to database
        try :
            inted_rating = int(edited_rating)

            if inted_rating < 1 or inted_rating > 5:
                errors['rating'] = 'Rating must be between 1 and 5'
            else:
                review_repository.change_rating_for_a_review(review_id, inted_rating)



        except ValueError:
            errors['rating'] = 'Rating must be a number'


    if edited_review != '':
        if len(edited_review) > 500:
            errors['review'] = 'Review must be less than 500 characters'
        else:
            review_repository.change_review_for_a_review(review_id, edited_review)

    if errors == {}:
        return jsonify({
            'success': 'Review updated successfully',
            'review_id' : review_id
            })
    return jsonify(errors), 400


    


    #grab the post data from the form

    #make sure the user is the same as the user that is logged in
    
    #update the review in the database
    

    # if the user is the same, render the edit review page with the review data
    return render_template('gem-details.html', review_id=review_id)


@review.delete('/<review_id>/delete-review')
@jwt_required()
def delete_review(review_id):
    user_id = get_jwt_identity()
    review_repository.delete_review(review_id)
    return jsonify({
        'success': 'Review deleted successfully'
        })