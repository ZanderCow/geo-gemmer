from repositories.db import db
from typing import Any

def get_all_reviews_for_a_hidden_gem(gem_id) -> list[dict[str, Any]]:
    '''
    Retrieve all the reviews for a hidden gem.
    
    Parameters:
        gem_id (int): The ID of the hidden gem.
    
    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the reviews.

    Example:
        >>> get_all_reviews_for_a_hidden_gem(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'user_name': 'Sally', 
                'rating': 4,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
            }, 
            {
                'user_name': 'Zander',
                'rating': 5,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
            }
        
        ]
    
    '''
    pass

def add_review_to_hidden_gem(gem_id, user_id, rating, review):
    '''
    Add a review to a hidden gem.
    
    Parameters:
        gem_id (int): The ID of the hidden gem.
        user_id (int): The ID of the user.
        rating (int): The rating of the hidden gem.
        review (str): The review of the hidden gem.
    
    Returns:
        None

    Example:
        >>> add_review_to_hidden_gem(
            67e55044-10b1-426f-9247-bb680e5fe0c8, 
            67e55044-10b1-426f-9247-bb680e5fe0c8, 
            5, 
            'This hidden gem was amazing! I would definitely recommend it to others.'
            )
    '''

    pass

def delete_review(review_id) -> None:
    '''
    Delete a review from a hidden gem.
    
    Parameters:
        gem_id (int): The ID of the hidden gem.
        user_id (int): The ID of the user.
    
    Returns:
        None

    Example:
        >>> delete_review(67e55044-10b1-426f-9247-bb680e5fe0c8)
    
    '''
    pass

def update_review_for_hidden_gem(gem_id, user_id, rating, review):
    '''
    Update a review for a hidden gem.
    
    Parameters:
        gem_id (int): The ID of the hidden gem.
        user_id (int): The ID of the user.
        rating (int): The rating of the hidden gem.
        review (str): The review of the hidden gem.
    
    Returns:
        None
    '''
    pass

def get_review_by_id(review_id) -> dict[str, Any]:
    '''
    Retrieve a review by its ID.
    
    Parameters:
        review_id (int): The ID of the review.
    
    Returns:
        dict[str, Any]: A dictionary representing the review.

    Example:
        >>> get_review_by_id(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            'user_name': 'Sally', 
            'rating': 4,
            'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
        }
    '''
    pass


def get_review_distribution_of_a_hidden_gem_visited_by_a_user(user_id):
    '''
    Get the distribution of hidden gems visited by a user.
    
    Parameters:
        user_id (int): The ID of the user.
    
    Returns:
        dict[str, int]: A dictionary with the distribution of hidden gems visited by a user.
    
    Example:
        >>> get_review_distribution_of_a_hidden_gem_visited_by_a_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            '1': 23,
            '2': 5,
            '3': 0,
            '4': 1,
            '5': 2
    '''
    pass

def get_average_rating_for_a_hidden_gem(gem_id) -> float:
    '''
    Get the average rating for a hidden gem.
    
    Parameters:
        gem_id (int): The ID of the hidden gem.
    
    Returns:
        float: The average rating of the hidden gem.

    Example:
        >>> get_average_rating_for_a_hidden_gem(67e55044-10b1-426f-9247-bb680e5fe0c8)
        4.5
    '''
    pass