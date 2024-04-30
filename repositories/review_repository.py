from psycopg.rows import dict_row
from repositories.db import get_pool
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
                    r.user_id,
                    username AS user_name,
                    profile_picture AS pfp,
                    gem_id,
                    rating,
                    review,
                    date
                FROM
                    review r
                JOIN geo_user u
                ON u.user_id = r.user_id
                WHERE gem_id = '{gem_id}'
                ORDER BY date DESC;''')
            return (cursor.fetchall())

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
           
            
            cursor.execute('''
            SELECT AVG(CAST(rating AS FLOAT))
            FROM review
            WHERE gem_id = %s;
                           
        ''', (gem_id,))
            avg_rating = cursor.fetchone()['avg']
            cursor.execute('''
            UPDATE hidden_gem
            SET avg_rat = %s
            WHERE gem_id = %s;
        ''', (avg_rating, gem_id))
            
            return True


def get_gem_review_distribution(gem_id):
    '''
    Retrieves the review distribution for a given gem.

    Parameters:
        gem_id (int): The ID of the gem.

    Returns:
        dict: A dictionary containing the review distribution, with keys 'total', 'one', 'two', 'three', 'four', and 'five'.
    '''
    review_distribution = {'total': 0, 'one': 0, 'two': 0, 'three': 0, 'four': 0, 'five': 0}

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT 
                    rating, 
                    COUNT(*) AS count
                FROM review
                WHERE gem_id = %s
                GROUP BY rating;
            ''', (gem_id,))
            results = cursor.fetchall()
    
    
    review_distribution = {
        'total': 0, 
        'one': 0, 
        'two': 0, 
        'three': 0, 
        'four': 0, 
        'five': 0
        }
    
    for rating in results:
        if int(rating['rating']) == 1:
            review_distribution['one'] = int(rating['count'])
            review_distribution['total'] += int(rating['count'])
        elif int(rating['rating']) == 2:
            review_distribution['two'] = int(rating['count'])
            review_distribution['total'] += int(rating['count'])
        elif int(rating['rating']) == 3:
            review_distribution['three'] = int(rating['count'])
            review_distribution['total'] += int(rating['count'])
        elif int(rating['rating']) == 4:
            review_distribution['four'] = int(rating['count'])
            review_distribution['total'] += int(rating['count'])
        elif int(rating['rating']) == 5:
            review_distribution['five'] = int(rating['count'])
            review_distribution['total'] += int(rating['count'])
    return review_distribution

def refresh_avg_rating_for_gem(gem_id):
    '''
    refreshes the average rating for a gem. 
    updates when user creates a new review or deletes one
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
            SELECT AVG(CAST(rating AS FLOAT))
            FROM review
            WHERE gem_id = %s;
        ''', (gem_id,))
            avg_rating = cursor.fetchone()['avg']
            cursor.execute('''
            UPDATE hidden_gem
            SET avg_rat = %s
            WHERE gem_id = %s;
        ''', (avg_rating, gem_id))
        return True


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
            cursor.execute('''
                SELECT
                    hg.name AS gem_name,
                    r.rating,
                    r.review,
                    r.review_id
                FROM
                    review r
                INNER JOIN
                    hidden_gem hg ON r.gem_id = hg.gem_id
                WHERE r.user_id = %s
                ORDER BY
                    r.date DESC;
            ''', (user_id,))
            return (cursor.fetchall())



def _date_to_int() -> int:
    day = str(datetime.today().date())
    day = int(day[:4]+day[5:7]+day[8:])
    return day

def _date_int_to_string(date:int) -> str:
    day = str(date)
    day = day[4:6]+'/'+day[6:]+'/'+day[:4]
    return day




def get_review_by_review_id(review_id):
    '''
    Retrieve a review by its ID.

    Parameters:
        review_id (str): The ID of the review.

    Returns:
        dict[str, Any]: A dictionary representing the review.
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                SELECT
                    h.gem_id,
                    h.name AS gem_name,
                    h.gem_type,
                    r.rating,
                    r.review,
                    r.review_id 
                FROM
                    review r
                JOIN
                    hidden_gem h ON  r.gem_id = h.gem_id
                WHERE
                    r.review_id = %s
                """, (review_id,))
            return (cursor.fetchall())
        

def change_rating_for_a_review(review_id,rating):
    '''
    Change the rating for a review.

    Parameters:
        review_id (str): The ID of the review.
        rating (int): The new rating for the review.

    Returns:
        None
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                UPDATE
                    review
                SET
                    rating = %s
                WHERE
                    review_id = %s
                """, (rating,review_id))
            
            cursor.execute('''              
            SELECT gem_id
            FROM review
            WHERE review_id = %s;
            ''', (review_id,))
            gem_id = cursor.fetchone()['gem_id']
            cursor.execute('''
            SELECT AVG(CAST(rating AS FLOAT))
            FROM review
            WHERE gem_id = %s;
                           
        ''', (gem_id,))
            avg_rating = cursor.fetchone()['avg']
            cursor.execute('''
            UPDATE hidden_gem
            SET avg_rat = %s
            WHERE gem_id = %s;
        ''', (avg_rating, gem_id))
            return True
        
def change_review_for_a_review(review_id,review):
    '''
    Change the review for a review.

    Parameters:
        review_id (str): The ID of the review.
        review (str): The new review for the review.

    Returns:
        None
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("""
                UPDATE
                    review
                SET
                    review = %s
                WHERE
                    review_id = %s
                """, (review,review_id))
            return True
   
def delete_review(review_id):
    '''
    Delete a review.

    Parameters:
        review_id (str): The ID of the review.

    Returns:
        None
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''              
            SELECT gem_id
            FROM review
            WHERE review_id = %s;
            ''', (review_id,))
            gem_id = cursor.fetchone()['gem_id']
            cursor.execute("""
                DELETE FROM
                    review
                WHERE
                    review_id = %s
                """, (review_id,))
            
            cursor.execute('''
            SELECT AVG(CAST(rating AS FLOAT))
            FROM review
            WHERE gem_id = %s;
                           
        ''', (gem_id,))
            avg_rating = cursor.fetchone()['avg']
            cursor.execute('''
            UPDATE hidden_gem
            SET avg_rat = %s
            WHERE gem_id = %s;
        ''', (avg_rating, gem_id))
            return True        
