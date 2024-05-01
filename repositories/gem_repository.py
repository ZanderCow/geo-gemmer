from repositories.db import get_pool, inflate_string
from psycopg.rows import dict_row
from typing import Any
from uuid import UUID


def search_for_gems(search_bar: str = '',
                    off_set: int = 0, 
                    lat: float = 0.0, 
                    long: float = 0.0, 
                    gem_type: str = '', 
                    wheelchair_accessible: bool = None, 
                    service_animal_friendly: bool = None, 
                    multilingual_support: bool = None, 
                    braille_signage: bool = None, 
                    hearing_assistance: bool = None, 
                    large_print_materials: bool = None, 
                    accessible_restrooms: bool = None, 
                    distance: int = 0,
                    minimum_rating: float = None):
    '''
    Searches for 20 gems based on the search bar and the filters, including distance and minimum rating criteria.

    Parameters:
        search_bar (str): the search bar
        off_set (int): the offset for the search
        lat (float): the latitude of the user's location
        long (float): the longitude of the user's location
        gem_type (str): the type of gem
        wheelchair_accessible (bool): if the gem is wheelchair accessible
        service_animal_friendly (bool): if the gem is service animal friendly
        multilingual_support (bool): if the gem has multilingual support
        braille_signage (bool): if the gem has braille signage
        hearing_assistance (bool): if the gem has hearing assistance
        large_print_materials (bool): if the gem has large print materials
        accessible_restrooms (bool): if the gem has accessible restrooms
        distance (int): how far the user is willing to travel in miles
        minimum_rating (float): the minimum average rating for the gem

    Returns:
        list[dict]: A list of gems matching the criteria.
    '''
    
    # Start building the query
    query = """
    SELECT h.gem_id, h.name, h.gem_type,
           ST_Distance(h.location, ST_MakePoint(%s, %s)::geography) AS distance,
           COALESCE(AVG(r.rating::int), 0)::float AS average_rating
    FROM hidden_gem h
    LEFT JOIN review r ON h.gem_id = r.gem_id
    LEFT JOIN accessibility a ON h.gem_id = a.gem_id
    WHERE 1=1
    """
    query_params = [lat, long]

    # Filter by search bar and gem type
    if search_bar:
        query += " AND h.name ILIKE %s"
        query_params.append(f'%{search_bar}%')
    if gem_type:
        query += " AND h.gem_type = %s"
        query_params.append(gem_type)

    # Add accessibility filters
    for key, value in [
        ('wheelchair_accessible', wheelchair_accessible),
        ('service_animal_friendly', service_animal_friendly),
        ('multilingual_support', multilingual_support),
        ('braille_signage', braille_signage),
        ('hearing_assistance', hearing_assistance),
        ('large_print_materials', large_print_materials),
        ('accessible_restrooms', accessible_restrooms)]:
        if value is not False:
            query += f" AND a.{key} = %s"
            query_params.append(value)

    # Filter by distance using ST_DWithin for geographic queries
    if distance > 0:
        query += " AND ST_DWithin(h.location, ST_MakePoint(%s, %s)::geography, %s)"
        query_params.extend([long, lat, distance * 1609.34])  # Convert miles to meters

    # Group by and order the query
    query += " GROUP BY h.gem_id, h.name, h.gem_type, h.location"

    # Filter by minimum rating
    if minimum_rating is not None:
        query += " HAVING COALESCE(AVG(r.rating::int), 0) >= %s"
        query_params.append(minimum_rating)

    query += " ORDER BY distance, average_rating DESC LIMIT 20 OFFSET %s;"
    query_params.append(off_set)

    # Execute the query
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, query_params)
            return _format_gem(cursor.fetchall())


def get_gems_created_by_user(user_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            gem_id,
            name,
            gem_type
        FROM
            hidden_gem
        WHERE
            user_id='{user_id}';''')
            return _format_gem(cursor.fetchall())


def is_not_uuid(input:str) -> bool:
    try:
        UUID(input)
    except ValueError:
        return True
    return False


def get_gem_header(gem_id:str) -> dict[str, Any] | None:
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
            'user_id': 67e5e90044-10b1-426f-9247-349054935f,
            
    '''
     
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            g.gem_id,
            g.name,
            g.user_id
        FROM
            hidden_gem g
        
        WHERE
            g.gem_id='{gem_id}';''')
            list = _format_gem(cursor.fetchall())
            
            return list


def get_basic_gem_info(gem_id:str) -> dict[str, Any] | None:
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
            'user_id': 67e5e90044-10b1-426f-9247-349054935f,
            
    '''
     
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            u.username,
            g.gem_id,
            g.name,
            g.gem_type,
            g.times_visited,
            g.user_created,
            g.avg_rat,
            g.user_id
            
            
        FROM
            hidden_gem g
        JOIN
            geo_user u
        ON
            g.user_id = u.user_id
        WHERE
            g.gem_id='{gem_id}';''')
            return cursor.fetchall()

def get_gem_distance_from_user(gem_id:str, latitude:float=0.0, longitude:float=0.0):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            g.gem_id,
            ST_X(g.location::geometry) AS longitude,
            ST_Y(g.location::geometry) AS latitude,
            ST_Distance(ST_MakePoint(%s, %s)::geography, location::geography) AS distance,    
        FROM
            hidden_gem g   
        WHERE
            g.gem_id='{gem_id}';''', (latitude, longitude))
            return _format_gem(cursor.fetchall())


def create_new_gem(name, gem_type,latitude:float , longitude:float, user_id) -> str:
    
    '''
    Creates a new hidden gem and adds it to the database.

    Parameters:
        name (str): The name of the gem. (max length: 127)
        gem_type (str): The type of the gem. (max length: 63)
        longitude (float): The location (E/W) of the gem.
        latitude (float): The location (N/S) of the gem.
        user_created (bool): Whether a user created the gem or not
        user_id (str): The ID of the user who created the gem.

    Returns:
        id (str): The id of the newly created gem

    NOTE: notice how not all the parameters for the hidden gem are present, this is on purpose.
        - when a gem is created it should have a default value for times_visited (0)
    '''
    #FAILSAFE IN CASE OF APOSTROPHES
    name = inflate_string(name, 127)
    gem_type = inflate_string(gem_type, 63)
    user_id = inflate_string(user_id)

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                INSERT INTO hidden_gem (name, gem_type, location, times_visited, user_id) VALUES (
                    '{name}',
                    '{gem_type}',
                    ST_SetSRID(ST_MakePoint({longitude}, {latitude}), 4326),
                    0,
                    '{user_id}')
                RETURNING
                    gem_id;''')
            
            #failsafe
            fetched_stuff = cursor.fetchone()
            if (fetched_stuff is not None and 'gem_id' in fetched_stuff):
                gem_id = str(fetched_stuff['gem_id'])
                cursor.execute(f"""
                    INSERT INTO accessibility (gem_id) VALUES (
                        '{gem_id}');""")
            return gem_id


def change_gem_name(gem_id:str, name:str):
    name = inflate_string(name, 127)
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''UPDATE hidden_gem
                                SET
                                    name = '{name}'
                                WHERE
                                    gem_id='{gem_id}';''')


def change_gem_type(gem_id:str, type:str):
    gem_type = inflate_string(gem_type, 63)
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


def _format_gem(gems:dict[str:Any]):
    if gems != None:
        for gem in gems:
            if ('distance' in gem): gem['distance'] = round(gem['distance']/1000, 4)
            gem['gem_id'] = str(gem['gem_id'])
    return gems


def get_gem_creator(gem_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
        SELECT
            gem_id,
            user_id
        FROM
            hidden_gem 
        WHERE
            gem_id='{gem_id}';''')
            return _format_gem(cursor.fetchall())
        