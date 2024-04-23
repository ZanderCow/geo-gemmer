from psycopg.rows import dict_row
from repositories.db import get_pool, inflate_string
from datetime import datetime
from typing import Any

def get_all_reviews_for_a_hidden_gem(gem_id:str) -> list[dict[str, Any]]:
    '''
    Retrieve all the reviews for a hidden gem.
    
    Parameters:
        gem_id (str): The ID of the hidden gem.
    
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
                WHERE gem_id = '{gem_id}'
                ORDER BY date DESC;''')
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
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                INSERT INTO review (user_id, gem_id, rating, review, date) VALUES (
                    '{user_id}',
                    '{gem_id}',
                    '{rating}',
                    '{review}',
                    '{day}'
                );''')
            cursor.execute(f'''
                SELECT
                    rating
                FROM
                    review r
                WHERE gem_id = '{gem_id}'
                ORDER BY date DESC;''')
            
            #calculate new average
            reviews = _convert_reviews_to_proper_form(cursor.fetchall())
            newAvg = 0.0
            for review in reviews:
                newAvg+=review['rating']
            newAvg /= len(reviews)

            #give the updated average to the hidden gem
            cursor.execute(f'''
                UPDATE hidden_gem
                SET
                    avg_rat={newAvg};''')



def get_review_distribution_of_a_hidden_gems_visited_by_a_user(user_id:str) -> list:
    '''
    Get the distribution of hidden gem ratings visited by a user.
    
    Parameters:
        user_id (str): The ID of the user.
    
    Returns:
        list(int): A list with the distribution of hidden gems visited by a user. Index 0 is 1 star, index 4 is 5 stars
    
    Example:
        >>> get_review_distribution_of_a_hidden_gem_visited_by_a_user('67e55044-10b1-426f-9247-bb680e5fe0c8')
        { #rating    1, 2, 3, 4, 5
                    23, 5, 0, 1, 2
    '''
    distro = [0,0,0,0,0]
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
                WHERE user_id = '{user_id}';''')
            reviews = _convert_reviews_to_proper_form(cursor.fetchall())
            for review in reviews:
                distro[review['rating']-1]+=1
            return distro



def get_average_rating_for_a_hidden_gem(gem_id:str) -> float:
    '''
    Get the average rating for a hidden gem.
    
    Parameters:
        gem_id (str): The ID of the hidden gem.
    
    Returns:
        float: The average rating of the hidden gem.

    Example:
        >>> get_average_rating_for_a_hidden_gem(67e55044-10b1-426f-9247-bb680e5fe0c8)
        4.5
    '''
    #this is probably gonna lag like crazy on the server since its not particularly fast and this is the .
    total:float = 0
    list = get_all_reviews_for_a_hidden_gem(gem_id)
    for review in list:
        total+=review['rating']
    total /= len(list)
    return total



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
            if ('rating' in review):
                review['rating'] = _expand_rating(review['rating'])
            if ('user_id' in review):
                review['user_id'] = str(review['user_id'])
            if ('gem_id' in review):
                review['gem_id'] = str(review['gem_id'])
            if ('date' in review):
                review['date'] = _date_int_to_string(review['date'])
    return the_reviews

def _convert_to_proper_form(review:dict[str,Any]):
    if (review != None):
        if ('rating' in review):
            review['rating'] = _expand_rating(review['rating'])
        if ('user_id' in review):
            review['user_id'] = str(review['user_id'])
        if ('gem_id' in review):
            review['gem_id'] = str(review['gem_id'])
        if ('date' in review):
            review['date'] = _date_int_to_string(review['date'])
    return review