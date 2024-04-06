from repositories.db import get_pool
from typing import Any


def create_new_user(username, password):
    """
    Create a new user in the database with the given username and password.

    Args:
        username (str): The username of the new user.
        password (str): The password of the new user.

    Returns:
        None

    NOTE: when a user is created it should have a default value for the following:
        - first_name (None)
        - last_name (None)
        - email_address (None)
        - profile_picture (None)
        - gems_explored_count (0)
        - reviews_made_count (0)
        - gems_created_count (0)
        - gems_saved_count (0)
    """
    pass


def get_user_by_id(user_id) -> dict[str, Any]:
    """
    Get a user from the database by their user_id.

    This would be used when a user logs in and they are at the dashboard 

    Args:
        user_id (str): The user_id of the user to get.

    Returns:
        dict[str, Any]: A dictionary representing the user.

    Example: 
        >>> get_user_by_id('67e55044-10b1-426f-9247-bb680e5fe0c8')
        {
            'user_name': 'TheCowanPlayz', 
            'first_name': 'Zander', 
            'last_name': 'Cowan',
            'profile_picture': 'amazons3.com/thisisapicture.jpg',
            'gems_explored_count': 'Restaurant',
            'reviews_made_count': 2,
            'gems_created_count': 3,
            'gems_saved_count': '3',
        }
    '''
    """
    pass

def delete_user_by_id(user_id):
    """
    Delete a user from the database by their user_id.

    Args:
        user_id (str): The user_id of the user to delete.

    Returns:
        None

    NOTE: when a user is deleted it should
        - make all the gems created by the user user_created = False 
        - delete their user saved gems from the database
        - delete their reviews from the database  
    """
    pass


def get_user_settings_details(user_id) -> dict[str, Any]:
    """
    Get the settings details of a user.

    Args:
        user_id (str): The user_id of the user to get the settings details for.

    Returns:
        dict[str, Any]: A dictionary representing the settings details of the user.

    Example:
        >>> get_user_settings_details('67e55044-10b1-426f-9247-bb680e5fe0c8')
        {
            'first_name': 'Zander',
            'last_name': 'Cowan',
            'email_address': 'zandercowan3424@gmail.com',
        }
    """
    pass

def change_user_settings(user_id, first_name, last_name, email_address):
    """
    Change the settings of a user.

    Args:
        user_id (str): The user_id of the user to change the settings for.
        first_name (str): The new first name of the user.
        last_name (str): The new last name of the user.
        email_address (str): The new email address of the user.

    Returns:
        None

    """
    pass

