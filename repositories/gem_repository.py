from repositories.db import get_pool
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
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
                'name': 'Rocky Mountian', 
                'latitude': '40.7128',
                'longitude': '74.0060',
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
                'website_link': 'https://www.penis.com', 
                }           
        ]
    """
    pass

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
    pass
    
def get_hidden_gem_by_id(gem_id) -> dict[str, Any]:
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
    pass

def get_all_hidden_gems_with_a_specific_type(gem_type):
    '''
    Gets all hidden gems based on a specific type. Used for filter search

    Returns:
        list[dict[str, Any]]: A list of all gems in the database with the specified type.
            
    Example: 
        >>> get_all_hidden_gems_with_a_specific_type("hiking_trail")
        [
            {
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8', 
                'name': 'Rocky Mountian', 
                'latitude': '40.7128',
                'longitude': '74.0060',
                'type': 'hiking_trail',
                'times_visited': 2,
                'user_created': True,
                'website_link': 'https://www.ruby-lang.org/en/',
                
                }, 
                {
                'user_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'name': 'Rocky Mountian',
                'latitude': '84.2315',
                'longitude': '31.3151',
                'type': 'hiking_trail',
                'times_visited': 2,
                'user_created': True,
                'website_link': 'https://www.penis.com', 
                }           
        ]
    '''
    pass

def get_all_gems_within_a_certain_distance_from_the_user(geo_location, distance):
    '''
    Retrieves all gems within a certain distance from the user's location.

    Args:
        geo_location (tuple[float, float]): The latitude and longitude of the user's location.
        distance (float): The maximum distance in kilometers from the user's location.

    Returns:
        list[dict[str, Any]]: A list of all gems in the database that are within the specified distance from the user.
    '''
    pass


def get_all_gems_with_a_specific_assesiblity(assesiblity):
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
                'latitude': '40.7128',
                'longitude': '74.0060',
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
                'website_link': 'https://www.penis.com', 
            }           
        ]
    """
    pass


