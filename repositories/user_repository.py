from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row


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
        - profile_picture (None)
        - gems_explored (0)
        - reviews_made (0)
        - gems_created (0)
        - gems_saved (0)
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                INSERT INTO geo_user (username, password, first_name, last_name, profile_picture, gems_explored, reviews_made, gems_created, gems_saved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s);
            ''', (username, password, None, None, None, 0, 0, 0, 0))


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
            'username': 'TheCowanPlayz', 
            'first_name': 'Zander', 
            'last_name': 'Cowan',
            'profile_picture': 'amazons3.com/thisisapicture.jpg',
            'gems_explored': 'Restaurant',
            'reviews_made': 2,
            'gems_created': 3,
            'gems_saved': '3'
        }
    '''
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                SELECT
                    username,
                    first_name,
                    last_name,
                    profile_picture,
                    gems_explored,
                    reviews_made,
                    gems_created,
                    gems_saved
                FROM
                    geo_user
                WHERE
                    user_id = '{user_id}';
            ''')
            return cursor.fetchall()

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
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                DELETE FROM
                    geo_user
                WHERE
                    user_id = '{user_id}';
            ''')
            return cursor.fetchall()


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
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    first_name,
                    last_name
                FROM
                    geo_user
                WHERE
                    user_id = %s;
            ''', (user_id,))
            return cursor.fetchone()

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
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            try:
                cursor.execute('''
                    UPDATE
                        geo_user
                    SET
                        first_name = %s,
                        last_name = %s
                    WHERE
                        user_id = %s;
                ''', (first_name, last_name, user_id))
            except psycopg.Error as e:
                print("Error occurred:", e)