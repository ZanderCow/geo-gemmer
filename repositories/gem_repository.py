from repositories.db import get_pool
from psycopg.rows import dict_row
from typing import Any

def get_all_gems() -> list[dict[str, Any]]:
    """
    Return all gems from the database

    - This function is going to probably be used for testing.
    - if we had like 30000 gems in the database we would not want to use this function

    Returns:
        list[dict[str, Any]]: A list of all gems in the database.
            
    Example: 
        >>> get_all_gems()
        [
            {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
            'name': 'Rocky Mountian', 
            'latitude': '40.7128',
            'longitude': '74.0060',
            'type': 'Restaurant',
            'times_visited': 2,
            'user_created': True,
            'website_link': 'https://www.ruby-lang.org/en/',
            
            }, 
            {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
            'name': 'Rocky Mountian',
            'latitude': '84.2315',
            'longitude': '31.3151',
            'type': 'Restaurant',
            'times_visited': 2,
            'user_created': True,
            'website_link': 'https://www.pennies.com', 
            }
        ]
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''SELECT
                                    gem_id,
                                    name,
                                    ST_X(location::geometry) AS longitude,
                                    ST_Y(location::geometry) AS latitude,
                                    gem_type AS type,
                                    times_visited,
                                    user_created,
                                    website_link
                                FROM
                                    hidden_gem;''')
            return cursor.fetchall()

def get_all_gems_ordered_by_nearest(longitude:float, latitude:float) -> list[dict[str, Any]]:
    """
    Return all gems from the database in order of distance

    - This function is going to probably be used for testing.
    - if we had like 30000 gems in the database we would not want to use this function

    Returns:
        list[dict[str, Any]]: A list of all gems in the database.
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                SELECT
                    gem_id,
                    name,
                    ST_X(location::geometry) AS longitude,
                    ST_Y(location::geometry) AS latitude,
                    ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                    gem_type AS type,
                    times_visited,
                    user_created,
                    website_link
                FROM
                    hidden_gem
                ORDER BY
                    distance;''')
            return cursor.fetchall()

def create_new_gem(name, gem_type, location, user_created):
    '''
    Creates a new hidden gem and adds it to the database.

    Parameters:
        name (str): The name of the gem.
        gem_type (str): The type of the gem.
        location (str): The location of the gem.
        user_created (str): The user who created the gem.

    Returns:
        None

    NOTE: notice how not all the parameters for the hidden gem are present, this is on purpose.
        - when a gem is created it should have a default value for times_visited (0)
        - the website_link should be None by default (not all gems have a website)
        
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                INSERT INTO hidden_gem (name, gem_type, location, times_visited, user_created, website_link) VALUES (
                    '{name}',
                    '{gem_type}',
                    ST_SetSRID(ST_MakePoint(-80.7324, 35.3036), 4326),
                    0,
                    true,
                    'https://www.charlotte.edu/'
                );''')
    
    
def get_hidden_gem_by_id(gem_id) -> dict[str, Any] | None:
    '''
    Retrieve a hidden gem from the repository based on its ID.

    Parameters:
        gem_id (string): The ID of the hidden gem to retrieve. (UUID)

    Returns:
        dict[str, Any]: A dictionary containing the details of the hidden gem.

    Example: 
        >>> get_hidden_gem_by_id('67e55044-10b1-426f-9247-bb680e5fe0c8')
        {
            'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
            'name': 'Rocky Mountian', 
            'latitude': '40.7128',
            'longitude': '74.0060',
            'type': 'Restaurant',
            'times_visited': 2,
            'user_created': True,
            'website_link': 'https://www.ruby-lang.org/en/',
        }
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''SELECT
                                    gem_id,
                                    name,
                                    ST_X(location::geometry) AS longitude,
                                    ST_Y(location::geometry) AS latitude,
                                    gem_type AS type,
                                    times_visited,
                                    user_created,
                                    website_link
                                FROM
                                    hidden_gem
                                WHERE
                                    gem_id={gem_id};''')
            return cursor.fetchall()

def get_all_hidden_gems_with_a_specific_type(longitude:float, latitude:float, gem_type):
    '''
    Gets all hidden gems based on a specific type. Used for filter search

    Returns:
        list[dict[str, Any]]: A list of all gems in the database with the specified type.
            
    Example: 
        >>> get_all_hidden_gems_with_a_specific_type("hiking_trail")
        [
            {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
                'name': 'Rocky Mountian', 
                'distance': 20.3346
                'type': 'hiking_trail',
                
                }, 
                {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'name': 'Rocky Mountian',
                distance': 20.3346
                'type': 'hiking_trail',
                }           
        ]
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''SELECT
                                    gem_id,
                                    name,
                                    ST_X(location::geometry) AS longitude,
                                    ST_Y(location::geometry) AS latitude,
                                    ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                                    gem_type AS type,
                                    times_visited,
                                    user_created,
                                    website_link
                                FROM
                                    hidden_gem
                                WHERE
                                    gem_type={gem_type}
                                ORDER BY
                                    distance;''')
            return cursor.fetchall()

def get_all_gems_within_a_certain_distance_from_the_user(longitude:float, latitude:float, outer_distance:float):
    '''
    Retrieves all gems within a certain distance from the user's location.

    Args:
        latitude (float): The latitude of the user's location.
        longitude (float): The longitude of the user's location.
        outer_distance (float): The maximum distance in kilometers from the user's location.

    Returns:
        list[dict[str, Any]]: A list of all gems in the database that are within the specified distance from the user.
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
            SELECT
                gem_id AS id,
                name,
                gem_type,
                ST_Y(location::geometry) AS latitude,
                ST_X(location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                times_visited,
                user_created,
                website_link
            FROM
                hidden_gem
            WHERE ST_DWithin(
                location::geography,
                ST_MakePoint({longitude}, {latitude})::geography,
                {outer_distance*1000})
            ORDER BY
                distance;''') # distance is in meters
            return cursor.fetchall()


def get_all_gems_with_a_specific_assesiblity(longitude:float, latitude:float, assesiblity) -> dict[str, Any] | None:
    """
    Retrieves all gems with a specific accessibility level.

    Parameters:
    - assesiblity (str): The desired accessibility level of the gems.

    Returns:
    - list: A list of gems that match the specified accessibility level.

    Example: 
        >>> get_all_gems_with_a_specific_assesiblity('autistic_friendly')
        [
            {
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
                'name': 'Rocky Mountian', 
                'type': 'Restaurant',
                'times_visited': 2,
                'user_created': True,
                'website_link': 'https://www.ruby-lang.org/en/',
                
            }, 
            {
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'name': 'Rocky Mountian',
                'latitude': '84.2315',
                'longitude': '31.3151',
                'type': 'Restaurant',
                'times_visited': 2,
                'user_created': True,
                'website_link': 'https://www.pennies.com', 
            }           
        ]
    """
    #ERROR HANDLING
    possibilities = ('wheelchair_accessible',
                    'service_animal_friendly',
                    'multilingual_support',
                    'braille_signage',
                    'hearing_assistance',
                    'large_print_materials',
                    'accessible_restrooms')
    if assesiblity not in possibilities:
        return None

    #get things with that accessibility
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
            SELECT
                h.gem_id AS id,
                h.name,
                h.gem_type,
                ST_Y(h.location::geometry) AS latitude,
                ST_X(h.location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                h.times_visited,
                h.user_created,
                h.website_link
            FROM
                hidden_gem h
            INNER JOIN
                accessibility a
            ON
                h.gem_id = a.gem_id
            WHERE
                a.{assesibility} = true
            ORDER BY
                distance;''')
            return cursor.fetchall()


