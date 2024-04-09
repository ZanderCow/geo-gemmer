from repositories.db import get_pool
from typing import Any


def get_all_gems_visited_by_user(user_id) -> list[dict[str, Any]]:
    '''
    Retrieves a list of all gems visited by a given user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the visited gems. 
    
    Example: 
        >>> get_all_gems_visited_by_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_visted': "2022-07-15"
            }, 
            {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'gem_name': 'Rocky Mountian',
                'date_visted': "2022-07-15"
            },
            {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'gem_name': 'Rocky Mountian',
                'date_visted': "2022-07-15"
            }         
        ]
    '''
    pass

def add_gem_to_visited_list(user_id, gem_id, date_visited):
    '''
    Adds a gem to a user's visited list.

    Parameters:
        user_id (int): The ID of the user.
        gem_id (int): The ID of the gem.
        date_visited (str): The date the gem was visited.

    Returns:
        None
    '''
    pass

def get_distribution_of_hidden_gems_visited_by_a_user(user_id):
    '''
    Get the distribution of hidden gems visited by a user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict[str, int]: A dictionary with the distribution of hidden gems visited by a user.

    Example:
        >>> get_distribution_of_hidden_gems_visited_by_a_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            'Restaurant': 2,
            'Park': 1,
            'Museum': 1
        }  
    '''
    pass

    def get_hidden_gems_visited_by_month(user_id):
        '''
        Retrieves the number of hidden gems visited by a user for each month.

        This is for that table on the dashboard

        Parameters:
            user_id (int): The ID of the user.

        Returns:
            dict[str, int]: A dictionary with the number of hidden gems visited by month.

        Example:
            >>> get_hidden_gems_visited_by_month(67e55044-10b1-426f-9247-bb680e5fe0c8)
            {
                'January': 3,
                'February': 2,
                'March': 1,
                ...
            }
        '''
        pass
       