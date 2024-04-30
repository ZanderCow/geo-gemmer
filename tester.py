from typing import Any


def search_for_gems(search_bar:str='',
                    off_set:int=0, 
                    lat:float=0.0, 
                    long:float=0.0, 
                    gem_type:str='', 
                    wheelchair_accessible:bool=None, 
                    service_animal_friendly:bool=None, 
                    multilingual_support:bool=None, 
                    braille_signage:bool=None, 
                    hearing_assistance:bool=None, 
                    large_print_materials:bool=None, 
                    accessible_restrooms:bool=None, 
                    distance:int=0, 
                    )-> list[dict[str, Any]]:
    '''
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
    '''
    pass