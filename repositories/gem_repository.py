from repositories.db import get_pool, inflate_string
from psycopg.rows import dict_row
from typing import Any

class accessibility_class:
    def __init__(self, wheelchair:bool=False, service_animal:bool=False, multilingual:bool=False, braille:bool=False, hearing_assistance:bool=False, large_print:bool=False, restrooms:bool=False):
        self.wheelchair_accessible = wheelchair
        self.service_animal_friendly = service_animal
        self.multilingual_support = multilingual
        self.braille_signage = braille
        self.hearing_assistance = hearing_assistance
        self.large_print_materials = large_print
        self.accessible_restrooms = restrooms
    
    def has_a_true(self):
        return self.wheelchair_accessible or self.service_animal_friendly or self.multilingual_support or self.braille_signage or self.hearing_assistance or self.large_print_materials or self.accessible_restrooms

    def to_string(self):
        stringy = ''
        if self.wheelchair_accessible:
            stringy += " AND wheelchair_accessible = true"
        if self.service_animal_friendly:
            stringy += " AND service_animal_friendly = true"
        if self.multilingual_support:
            stringy += " AND multilingual_support = true"
        if self.braille_signage:
            stringy += " AND braille_signage = true"
        if self.hearing_assistance:
            stringy += " AND hearing_assistance = true"
        if self.large_print_materials:
            stringy += " AND large_print_materials = true"
        if self.accessible_restrooms:
            stringy += " AND accessible_restrooms = true"
        return stringy

#grabbing from gems

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
            'user_created': True
            
            }, 
            {
            'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
            'name': 'Rocky Mountian',
            'latitude': '84.2315',
            'longitude': '31.3151',
            'type': 'Restaurant',
            'times_visited': 2,
            'user_created': True
            }
        ]
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''SELECT
                                    g.gem_id,
                                    name,
                                    ST_X(location::geometry) AS longitude,
                                    ST_Y(location::geometry) AS latitude,
                                    gem_type,
                                    times_visited,
                                    user_created,
                                    image_1,
                                    image_2,
                                    image_3
                                FROM
                                    hidden_gem g
                                JOIN image_group i
                                ON g.gem_id = i.gem_id;''')
            return _format_gem(cursor.fetchall())

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
                    g.gem_id,
                    g.name,
                    ST_X(g.location::geometry) AS longitude,
                    ST_Y(g.location::geometry) AS latitude,
                    ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                    g.gem_type,
                    g.times_visited,
                    g.user_created,
                    i.image_1,
                    i.image_2,
                    i.image_3
                FROM
                    hidden_gem g
                JOIN image_group i
                ON g.gem_id = i.gem_id
                ORDER BY
                    distance;''')
            return _format_gem(cursor.fetchall())

def get_hidden_gem_by_id(gem_id, longitude:float=None, latitude:float=None) -> dict[str, Any] | None:
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
            'gem_type': 'Restaurant',
            'times_visited': 2,
            'user_created': True,
            'wheelchair_accessible': false,
            'service_animal_friendly': false,
            'multilingual_support': false,
            'braille_signage': false,
            'hearing_assistance': false,
            'large_print_materials': false,
            'accessible_restrooms': false
        }
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            g.gem_id,
            g.name,
            ST_X(g.location::geometry) AS longitude,
            ST_Y(g.location::geometry) AS latitude,
            {f'ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance, ' if longitude != None and latitude != None else ''}
            g.gem_type,
            g.times_visited,
            g.user_created,
            g.avg_rat,
            a.wheelchair_accessible,
            a.service_animal_friendly,
            a.multilingual_support,
            a.braille_signage,
            a.hearing_assistance,
            a.large_print_materials,
            a.accessible_restrooms,
            i.image_1,
            i.image_2,
            i.image_3
        FROM
            hidden_gem g
        JOIN accessibility a
        ON g.gem_id = a.gem_id
        JOIN image_group i
        ON g.gem_id = i.gem_id
        WHERE
            g.gem_id='{gem_id}';''')
            list = _format_gem(cursor.fetchall())
            if (len(list) == 0):
                return None
            return list[0]

def get_all_hidden_gems_with_a_specific_type(longitude:float, latitude:float, gem_type, offset:int=0):
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
                                    gem_type,
                                    times_visited,
                                    user_created
                                FROM
                                    hidden_gem
                                WHERE
                                    gem_type={gem_type}
                                ORDER BY
                                    distance
                                OFFSET
                                    {offset}
                                LIMIT
                                    20;''')
            return _format_gem(cursor.fetchall())

def get_all_gems_within_a_certain_distance_from_the_user(longitude:float, latitude:float, outer_distance:float, offset:int=0):
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
                g.gem_id,
                g.name,
                g.gem_type,
                ST_Y(g.location::geometry) AS latitude,
                ST_X(g.location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                g.times_visited,
                g.user_created,
                g.avg_rat,
                i.image_1,
                i.image_2,
                i.image_3
            FROM
                hidden_gem g
            JOIN image_group i
            ON g.gem_id = i.gem_id
            WHERE ST_DWithin(
                location::geography,
                ST_MakePoint({longitude}, {latitude})::geography,
                {outer_distance*1000})
            ORDER BY
                distance ASC
            OFFSET
                {offset}
            LIMIT
                20;''') # distance is in meters
            return _format_gem(cursor.fetchall())

def search_all_gems_within_a_certain_distance_from_the_user(search_string:str, longitude:float, latitude:float, outer_distance:float, offset:int=0):
    '''
    Retrieves all gems within a certain distance from the user's location.

    Args:
        latitude (float): The latitude of the user's location.
        longitude (float): The longitude of the user's location.
        outer_distance (float): The maximum distance in kilometers from the user's location.
        offset (int): the number of entries to skip before grabbing the next 20

    Returns:
        list[dict[str, Any]]: A list of all gems in the database that are within the specified distance from the user.
    '''
    search_string = inflate_string(search_string, 255)

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
            SELECT
                g.gem_id,
                g.name,
                g.gem_type,
                word_similarity(g.name, 'closey') AS name_similarity,
                ST_Y(g.location::geometry) AS latitude,
                ST_X(g.location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                g.times_visited,
                g.user_created,
                g.avg_rat,
                i.image_1,
                i.image_2,
                i.image_3
            FROM
                hidden_gem g
            JOIN image_group i
            ON g.gem_id = i.gem_id
            WHERE ST_DWithin(
                location::geography,
                ST_MakePoint({longitude}, {latitude})::geography,
                {outer_distance*1000}) AND word_similarity(name, '{search_string}') > 0.1
            ORDER BY
                distance ASC,name_similarity DESC
            OFFSET
                {offset}
            LIMIT
                20;''')
            return _format_gem(cursor.fetchall())

def filtered_get_all_gems_within_a_certain_distance_from_the_user(longitude:float, latitude:float, outer_distance:float, type:str|None, accessibility:accessibility_class, min_avg_rating:int=0, offset:int=0):
    '''
    Retrieves all gems within a certain distance from the user's location.

    Args:
        latitude (float): The latitude of the user's location.
        longitude (float): The longitude of the user's location.
        outer_distance (float): The maximum distance in kilometers from the user's location.

    Returns:
        list[dict[str, Any]]: A list of all gems in the database that are within the specified distance from the user.
    '''
    #clamp rating from 0-4
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
            SELECT
                g.gem_id,
                name,
                gem_type,
                ST_Y(location::geometry) AS latitude,
                ST_X(location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                times_visited,
                user_created,
                avg_rat,
                wheelchair_accessible,
                service_animal_friendly,
                multilingual_support,
                braille_signage,
                hearing_assistance,
                large_print_materials,
                accessible_restrooms,
                i.image_1,
                i.image_2,
                i.image_3
            FROM
                hidden_gem g
            JOIN accessibility a
            ON g.gem_id = a.gem_id
            JOIN image_group i
            ON g.gem_id = i.gem_id
            WHERE ST_DWithin(
                location::geography,
                ST_MakePoint({longitude}, {latitude})::geography, {outer_distance*1000}){accessibility.to_string()}
                {f"AND g.gem_type = '{type}'" if type != None else ""}
                AND avg_rat > {min_avg_rating}
            ORDER BY
                distance
            OFFSET
                {offset}
            LIMIT
                20;''') # distance is in meters
            return _format_gem(cursor.fetchall())

def filtered_search_all_gems_within_a_certain_distance_from_the_user(search_string:str, longitude:float, latitude:float, outer_distance:float, type:str|None=None, accessibility:accessibility_class|None=None, min_avg_rating:int=0, offset:int=0):
    '''
    Retrieves all gems within a certain distance from the user's location.

    Args:
        latitude (float): The latitude of the user's location.
        longitude (float): The longitude of the user's location.
        outer_distance (float): The maximum distance in kilometers from the user's location.
        offset (int): the number of entries to skip before grabbing the next 20

    Returns:
        list[dict[str, Any]]: A list of all gems in the database that are within the specified distance from the user.
    '''
    #in case
    search_string = inflate_string(search_string, 255)

    #clamp rating from 0-4
    min_avg_rating = min(5, max(1, min_avg_rating))-1

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
            SELECT
                g.gem_id,
                name,
                gem_type,
                word_similarity(g.name, 'closey') AS name_similarity,
                ST_Y(location::geometry) AS latitude,
                ST_X(location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                times_visited,
                user_created,
                avg_rat,
                wheelchair_accessible,
                service_animal_friendly,
                multilingual_support,
                braille_signage,
                hearing_assistance,
                large_print_materials,
                accessible_restrooms,
                image_1,
                image_2,
                image_3
            FROM
                hidden_gem g
            JOIN accessibility a
            ON  g.gem_id = a.gem_id
            JOIN image_group i
            ON g.gem_id = i.gem_id
            WHERE ST_DWithin(
                location::geography,
                ST_MakePoint({longitude}, {latitude})::geography,
                {outer_distance*1000}) {accessibility.to_string() if accessibility != None else ''}
                AND word_similarity(name, '{search_string}') > 0.1
                {f"AND g.gem_type = '{type}'" if type != None else ""}
                AND avg_rat > {min_avg_rating}
            ORDER BY
                name_similarity DESC, distance ASC
            OFFSET
                {offset}
            LIMIT
                20;''') # distance is in meters
            return _format_gem(cursor.fetchall())

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
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
                'name': 'Rocky Mountian', 
                'type': 'Restaurant',
                'times_visited': 2,
                'user_created': True,
            }, 
            {
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'name': 'Rocky Mountian',
                'latitude': '84.2315',
                'longitude': '31.3151',
                'type': 'Restaurant',
                'times_visited': 2,
                'user_created': True
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
                h.gem_id,
                h.name,
                h.gem_type,
                ST_Y(h.location::geometry) AS latitude,
                ST_X(h.location::geometry) AS longitude,
                ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
                h.times_visited,
                h.user_created,
                i.image_1,
                i.image_2,
                i.image_3
            FROM
                hidden_gem h
            INNER JOIN
                accessibility a
            ON
                h.gem_id = a.gem_id
            JOIN image_group i
            ON h.gem_id = i.gem_id
            WHERE
                a.{assesiblity} = true
            ORDER BY
                distance;''')
            return _format_gem(cursor.fetchall())



#adding gem
def create_new_gem(name, gem_type, longitude:float, latitude:float, user_created:bool, image1:str=None,image2:str=None,image3:str=None) -> str:
    # img failsafes
    if (image1 == ''): image1 = None
    elif (image1 != None): image1 = inflate_string(image1, 255)
    if (image2 == ''): image2 = None
    elif (image2 != None): image2 = inflate_string(image2, 255)
    if (image3 == ''): image3 = None
    elif (image3 != None): image3 = inflate_string(image3, 255)
    '''
    Creates a new hidden gem and adds it to the database.

    Parameters:
        name (str): The name of the gem. (max length: 127)
        gem_type (str): The type of the gem. (max length: 63)
        longitude (float): The location (E/W) of the gem.
        latitude (float): The location (N/S) of the gem.
        user_created (bool): Whether a user created the gem or not
        image1 (str): Link to image 1 (max length: 255)
        image2 (str): Link to image 2 (max length: 255)
        image3 (str): Link to image 3 (max length: 255)

    Returns:
        id (str): The id of the newly created gem

    NOTE: notice how not all the parameters for the hidden gem are present, this is on purpose.
        - when a gem is created it should have a default value for times_visited (0)
    '''
    #FAILSAFE IN CASE OF APOSTROPHES
    name = inflate_string(name, 127)
    gem_type = inflate_string(gem_type, 63)

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                INSERT INTO hidden_gem (name, gem_type, location, times_visited, user_created) VALUES (
                    '{name}',
                    '{gem_type}',
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326),
                    0,
                    {'true' if user_created else 'false'})
                RETURNING
                    gem_id;''')
            #failsafe
            fetched_stuff = cursor.fetchone()
            if (fetched_stuff is not None):
                gem_id = str(fetched_stuff['gem_id'])
                cursor.execute(f"""
                    INSERT INTO accessibility (gem_id) VALUES (
                        '{gem_id}');""")
                cursor.execute(f"""
                    INSERT INTO image_group (gem_id, image_1, image_2, image_3) VALUES (
                        '{gem_id}',
                        {"'" + image1 + "'" if image1 is not None else 'null'},
                        {"'" + image2 + "'" if image2 is not None else 'null'},
                        {"'" + image3 + "'" if image3 is not None else 'null'});""")
                return gem_id
            return None



#modifying gems
def change_gem_name(gem_id:str, name:str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE hidden_gem
                                SET
                                    name = '{name}'
                                WHERE
                                    gem_id='{gem_id}';''')

def change_gem_type(gem_id:str, type:str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE hidden_gem
                                SET
                                    gem_type = '{type}'
                                WHERE
                                    gem_id='{gem_id}';''')

def change_gem_location(gem_id:str, longitude:float, latitude:float):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE hidden_gem
                                SET
                                    location = ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326)
                                WHERE
                                    gem_id='{gem_id}';''')

def increment_gem_times_visited(gem_id:str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE hidden_gem
                                SET
                                    times_visited = times_visited+1
                                WHERE
                                    gem_id='{gem_id}';''')

def _change_gem_times_visited(gem_id:str, times_visited:int=-1):
    if (times_visited > -1):
        pool = get_pool()
        with pool.connection() as conn:
            with conn.cursor(row_factory=dict_row) as cursor:
                cursor.execute(f'''UPDATE hidden_gem
                                    SET
                                        times_visited = {times_visited}
                                    WHERE
                                        gem_id='{gem_id}';''')

def change_accessibility(gem_id:str, acc:accessibility_class):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE accessibility
                                SET
                                    wheelchair_accessible = {'true' if acc.wheelchair_accessible else 'false'},
                                    service_animal_friendly = {'true' if acc.service_animal_friendly else 'false'},
                                    multilingual_support = {'true' if acc.multilingual_support else 'false'},
                                    braille_signage = {'true' if acc.braille_signage else 'false'},
                                    hearing_assistance = {'true' if acc.hearing_assistance else 'false'},
                                    large_print_materials = {'true' if acc.large_print_materials else 'false'},
                                    accessible_restrooms = {'true' if acc.accessible_restrooms else 'false'}
                                WHERE
                                    gem_id='{gem_id}';''')

def change_images(gem_id:str, image_1:str='', image_2:str='', image_3:str=''):
    if (image_1 == None): image_1 = ''
    if (image_2 == None): image_2 = ''
    if (image_3 == None): image_3 = ''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE image_group
                                SET
                                    image_1 = {image_1 if image_1 == '' else 'image_1'},
                                    image_2 = {image_2 if image_2 == '' else 'image_2'},
                                    image_3 = {image_3 if image_3 == '' else 'image_3'}
                                WHERE
                                    gem_id='{gem_id}';''')


def delete_hidden_gem(gem_id:str):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''DELETE
                                FROM
                                    hidden_gem
                                WHERE
                                    gem_id='{gem_id}';''')


#abstracted stuff so i dont have to rewrite a bunch of boilerplate
def _format_gem(gems:dict[str:Any]):
    if gems != None:
        for gem in gems:
            if ('distance' in gem): gem['distance'] = round(gem['distance']/1000, 4)
            gem['gem_id'] = str(gem['gem_id'])
    return gems