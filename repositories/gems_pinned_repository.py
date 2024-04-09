from repositories.db import get_pool
from typing import Any

def get_gems_pinned_by_user(user_id):
    '''
    Retrieves a list of all gems pinned by a given user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the visited gems. 
    
    Example: 
        >>> get_all_gems_pinned_by_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"
            }, 
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"        
            },
            {
               'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"      
            }         
        ]
    '''
    pass



    