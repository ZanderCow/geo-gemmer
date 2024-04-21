from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row
import bcrypt


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
            
            # hashed password 
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt(12))
            

            cursor.execute('''
                INSERT INTO geo_user (username, password, first_name, last_name, profile_picture, gems_explored, reviews_made, gems_created, gems_saved)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                RETURNING user_id;
            ''', (username, hashed_password, None, None, None, 0, 0, 0, 0))
            user_id = cursor.fetchone()['user_id']
            return user_id

def get_password(username):
    """
    Gets the hashed user password from the database given their username.

    Args:
        username (str): The username of the user.

    Returns:
        dict: A dictionary containing the password or None if not found.
    """
    pool = get_pool()  # Assuming get_pool is defined elsewhere in your code
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute("SELECT password FROM geo_user WHERE username = %s", (username,))
            result = cursor.fetchone()  # Fetches the first row
    
            return result

        
def does_username_exist(username):
    """
    Check if a user with the given username exists in the database.

    Args:
        username (str): The username to check for.

    Returns:
        bool: True if the user exists, False otherwise.
    """
    if username is None:
        return False
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    user_id
                FROM
                    geo_user
                WHERE
                    username = %s;
            ''', (username,))
            return cursor.fetchone() is not None

def get_userid_by_username(username):
    """
    Get the user_id of a user by their username.

    Args:
        username (str): The username of the user to get the user_id for.

    Returns:
        str: The user_id of the user.

    Example:
        >>> get_userid_by_username('TheCowanPlayz')
        '67e55044-10b1-426f-9247-bb680e5fe0c8'
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    user_id
                FROM
                    geo_user
                WHERE
                    username = %s;
            ''', (username,))
            return cursor.fetchone()['user_id']

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
        
def get_username_by_id(user_id) -> dict[str, Any]:
    """
    Get a user from the database by their user_id.

    This would be used when a user logs in and they are at the dashboard 

    Args:
        user_id (str): The user_id of the user to get.

    Returns:
        dict[str, Any]: A dictionary representing the user.

    Example: 
        >>> get_user_by_id('67e55044-10b1-426f-9247-bb680e5fe0c8')
            {'username': 'TheCowanPlayz'}
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute(f'''
                SELECT
                    username
                FROM
                    geo_user
                WHERE
                    user_id = '{user_id}';
            ''')
            return cursor.fetchone()

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
                    username,
                    first_name,
                    last_name
                FROM
                    geo_user
                WHERE
                    user_id = %s;
            ''', (user_id,))
            return cursor.fetchone()

def change_user_settings(user_id, user_name, first_name, last_name, pfp):
    """
    Change the settings of a user.

    Args:
        user_id (str): The user_id of the user to change the settings for.
        first_name (str): The new first name of the user.
        last_name (str): The new last name of the user.
        pfp (str): The new profile picture url of the user.

    Returns:
        None

    """

    #connect to s3 bucket and upload the image
    #get the url of the image and save it to the database
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                UPDATE
                    geo_user
                SET
                    username = %s,
                    first_name = %s,
                    last_name = %s,
                    profile_picture = %s
                WHERE
                    user_id = %s;
            ''', (user_name, first_name, last_name, pfp, user_id))
            return True