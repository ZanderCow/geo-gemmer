
from repositories.db import get_pool, inflate_string
from psycopg.rows import dict_row
from typing import Any, Dict, List

from uuid import UUID
'''
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
                    distance: int = 0) -> List[Dict[str, Any]]:
    
    searches for 20 gem based on the search bar and the filters
    
    Parameters:
        search_bar (str): the search bar
        off_set (int): the off set for the search (if its 20, the next 20 gems will be returned, still based on the search bar and filters)
        lat (float): the latitude of the users location
        long (float): the longitude of the users location
        gem_type (str): the type of gem
        wheelchair_accessible (bool): if the gem is wheelchair accessible
        service_animal_friendly (bool): if the gem is service animal friendly
        multilingual_support (bool): if the gem has multilingual support
        braille_signage (bool): if the gem has braille signage
        hearing_assistance (bool): if the gem has hearing assistance
        large_print_materials (bool): if the gem has large print materials
        accessible_restrooms (bool): if the gem has accessible restrooms
        distance (int): how far the user is willing to travel

    Returns:
        list[dict
            {
            gem_id (str): the id of the gem
            name (str): the name of the gem
            type (str): the type of the gem
            distance (float): the distance from the user
            average_rating (float): the average rating of the gem
            }
            ]
        if there are no gems that match the search bar and filters, an empty list will be returned
        if there are no filters, the first 20 gems will be returned, based on the search bar
        if no parameters are given, the first 20 gems will be returned reguardless 
        if the query isnt 20, it will return the amount of gems that match the query
    Examples:
        search_for_gems(search_bar='test', off_set=0, lat=0.0, long=0.0, gem_type='test', wheelchair_accessible=false, service_animal_friendly=false, multilingual_support=True, braille_signage=True, hearing_assistance=True, large_print_materials=True, accessible_restrooms=True, distance=0)
        >>> [
            {'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c', 'name': 'Rocky Mountian', 'type': 'Restaurant', 'distance': 394.5, 'average_rating': 0.0},
            {'gem_id': '46e5942-23b3-485g-5838-584jf49f0f', 'name': 'fsjkl', 'type': 'beach', 'distance': 34344.4, 'average_rating': 3.4}
            ]
        search_for_gems()
            
        >>> [
            {'gem_id': '', 'name': 'test', 'type': 'test', 'distance': 0, 'average_rating': 0.0},
            {'gem_id': 'test2', 'name': 'fsjkl', 'type': 'beach', 'distance': 34344.4, 'average_rating': 3.4}
            ]
    
        # Start building the query
    query = """
    SELECT h.gem_id, h.name, h.gem_type,
        ST_Distance(ST_MakePoint({longitude}, {latitude})::geography, location::geography) AS distance,
        (ST_Distance(h.location, ST_MakePoint(%s, %s)::geography) / 1609.34) AS distance,
        COALESCE(AVG(r.rating::int), 0)::float AS average_rating
    FROM hidden_gem h
    LEFT JOIN review r ON h.gem_id = r.gem_id
    LEFT JOIN accessibility a ON h.gem_id = a.gem_id
    WHERE 1=1
    """
    query_params = [long, lat]  # Ensure long, lat order is maintained here

    # Rest of your existing code for adding conditions...

    # Add distance filter condition properly
    if distance > 0:
        query += " AND (ST_Distance(h.location, ST_MakePoint(%s, %s)::geography) / 1609.34) <= %s"
        query_params.extend([long, lat, distance])  # Ensure parameters are correctly extended

    # Group by, order, and pagination controls
    query += """
    GROUP BY h.gem_id, h.name, h.gem_type, h.location
    ORDER BY distance
    LIMIT 20 OFFSET %s;
    """
    query_params.append(off_set)

    # Execute the query
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, query_params)
            return cursor.fetchall()
'''
def _format_gem(gems:dict[str:Any]):
    if gems != None:
        for gem in gems:
            if ('distance' in gem): gem['distance'] = round(gem['distance']/1000, 4)
            gem['gem_id'] = str(gem['gem_id'])
    return gems


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
                    distance: int = 0) -> List[Dict[str, Any]]:
    '''
    Searches for 20 gems based on the search bar and the filters, including distance criteria.

    Parameters:
        search_bar (str): the search bar
        off_set (int): the offset for the search (if its 20, the next 20 gems will be returned, still based on the search bar and filters)
        lat (float): the latitude of the users location
        long (float): the longitude of the users location
        gem_type (str): the type of gem
        wheelchair_accessible (bool): if the gem is wheelchair accessible
        service_animal_friendly (bool): if the gem is service animal friendly
        multilingual_support (bool): if the gem has multilingual support
        braille_signage (bool): if the gem has braille signage
        hearing_assistance (bool): if the gem has hearing assistance
        large_print_materials (bool): if the gem has large print materials
        accessible_restrooms (bool): if the gem has accessible restrooms
        distance (int): how far the user is willing to travel in miles

    Returns:
        list[dict]: A list of gems matching the criteria.
    '''
    
    # Start building the query
    query = """
    SELECT h.gem_id, h.name, h.gem_type,
            
           (ST_Distance(h.location, ST_MakePoint(%s, %s)::geography)) AS distance,
           COALESCE(AVG(r.rating::int), 0)::float AS average_rating
    FROM hidden_gem h
    LEFT JOIN review r ON h.gem_id = r.gem_id
    LEFT JOIN accessibility a ON h.gem_id = a.gem_id
    WHERE 1=1
    """
    query_params = [long, lat]

    # Filter by search bar and gem type
    if search_bar:
        query += " AND h.name ILIKE %s"
        query_params.append(f'%{search_bar}%')
    if gem_type:
        query += " AND h.gem_type = %s"
        query_params.append(gem_type)

    # Add accessibility filters
    accessibility_conditions = {
        'wheelchair_accessible': wheelchair_accessible,
        'service_animal_friendly': service_animal_friendly,
        'multilingual_support': multilingual_support,
        'braille_signage': braille_signage,
        'hearing_assistance': hearing_assistance,
        'large_print_materials': large_print_materials,
        'accessible_restrooms': accessible_restrooms
    }
    for key, value in accessibility_conditions.items():
        if value is not None:
            query += f" AND a.{key} = %s"
            query_params.append(value)

    # Filter by distance using ST_DWithin for geographic queries
    if distance > 0:
        query += " AND ST_DWithin(h.location, ST_MakePoint(%s, %s)::geography, %s)"
        query_params.extend([long, lat])

    # Group by and order the query
    query += """
    GROUP BY h.gem_id, h.name, h.gem_type, h.location
    ORDER BY distance, average_rating DESC
    LIMIT 20 OFFSET %s;
    """
    query_params.append(off_set)

    # Execute the query
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(query, query_params)
            return _format_gem(cursor.fetchall())


# Example usage
if __name__ == "__main__":
    # This will return the first 20 gems with no filters.
    gems = search_for_gems(long=-80.8020089, lat=35.0248724)
    print(gems)

    