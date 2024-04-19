from psycopg.rows import dict_row
from repositories.db import get_pool, inflate_string
from datetime import datetime
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
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                SELECT
                    user_id,
                    gem_id,
                    rating,
                    review,
                    date
                FROM
                    review r
                WHERE gem_id = '{gem_id}';''')
            return _convert_reviews_to_proper_form(cursor.fetchall())

def add_review_to_hidden_gem(gem_id:str, user_id:str, rating:int, review:str):
    '''
    Add a review to a hidden gem.
    
    Parameters:
        gem_id (str): The ID of the hidden gem.
        user_id (str): The ID of the user.
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
    #convert rating to smaller form for postgres
    rating = _shrink_rating(rating)

    #inflate review, in case of apostrophe catastrophe
    review = inflate_string(review, 511)

    #DAY
    day = _date_to_int()

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''
                INSERT INTO review (user_id, gem_id, rating, review, date) VALUES (
                    '{user_id}',
                    '{gem_id}',
                    '{rating}',
                    '{review}',
                    '{day}'
                );''')



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

def get_all_reviews_user_has_made(user_id:str) -> list[dict[str, Any]]:
    '''
    Retrieve all the reviews a user has made.
    
    Parameters:
        user_id (str): The ID of the user.
    
    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the reviews.

    Example:
        >>> get_all_reviews_user_has_made(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'gem_name': 'Rocky Mountian',
                'rating': 4,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
            }, 
            {
                'gem_name': 'Rocky Mountian',
                'rating': 5,
                'review': 'This hidden gem was amazing! I would definitely recommend it to others.',
            }
        
        ]
    '''
    #for some reason user ids are stored as uuids and not strings
    #i made the gems convert to strings for abstraction but oh well :p
    if (user_id is not str):
        user_id = str(user_id)
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                SELECT
                    user_id,
                    gem_id,
                    rating,
                    review,
                    date
                FROM
                    review r
                WHERE user_id = '{user_id}'
                ORDER BY
                    date DESC;''')
            return _convert_reviews_to_proper_form(cursor.fetchall())

def _shrink_rating(num:int) -> chr:
    
    num = max(0, min(5, num))
    return chr(num+30)

def _expand_rating(rating:chr) -> int:
    return ord(rating)-30

def _date_to_int() -> int:
    day = str(datetime.today().date())
    day = int(day[:4]+day[5:7]+day[8:])
    return day

def _date_int_to_string(date:int) -> str:
    day = str(date)
    day = day[4:6]+'/'+day[6:]+'/'+day[:4]
    return day

def _convert_reviews_to_proper_form(the_reviews:list[dict[str,Any]]):
    if (the_reviews != None):
        for review in the_reviews:
            review['rating'] = _expand_rating(review['rating'])
            review['user_id'] = str(review['user_id'])
            review['gem_id'] = str(review['gem_id'])
            review['date'] = _date_int_to_string(review['date'])
    return the_reviews

def _convert_to_proper_form(review:dict[str,Any]):
    if (review != None):
        review['rating'] = _expand_rating(review['rating'])
        review['user_id'] = str(review['user_id'])
        review['gem_id'] = str(review['gem_id'])
        review['date'] = _date_int_to_string(review['date'])
    return review