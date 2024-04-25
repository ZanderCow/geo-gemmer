from repositories.db import get_pool
from typing import Any
from repositories.s3 import get_s3_client
import uuid
from psycopg.rows import dict_row


def get_images_for_a_hidden_gem(gem_id):
    '''
    Retrieve the images associated with a hidden gem from an Amazon S3 server.

    Parameters:
        gem_id (int): The ID of the hidden gem.

    Returns:
        str: The file location of the images on the Amazon S3 server.
    '''
    pass

def get_primary_image_for_a_hidden_gem(gem_id):
    '''
    Retrieve the primary image associated with a hidden gem from an Amazon S3 server.

    Parameters:
        gem_id (int): The ID of the hidden gem.

    Returns:
        str: The file location of the primary image on the Amazon S3 server.
    '''
    pass

def create_user_pfp(user_id,file_path):
    '''
    Upload an image to an Amazon S3 server for a user's profile picture.

    Parameters:
        file_path (str): The file path of the image to upload.

    Returns:
        str: The key of the file on the Amazon S3 server.
    '''
  

    unique_id = uuid.uuid4()
    full_file_key = f"profile-pictures/pfp_{unique_id}.png"
    with get_s3_client() as s3:
        s3.upload_fileobj(
            Fileobj=file_path,
            Bucket='geo-gemmer-images',
            Key=full_file_key
            )
        

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                UPDATE
                    geo_user
                SET
                    profile_picture = %s
                WHERE
                    user_id = %s;
            ''', (full_file_key, user_id))
    return full_file_key


def get_user_pfp(user_id):
    '''
    Retrieve the profile picture of a user from an Amazon S3 server.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        str: The file location of the profile picture on the Amazon S3 server.
    '''
    pfp_key = None
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    profile_picture
                FROM
                    geo_user
                WHERE
                    user_id = %s;
            ''', (user_id,))
            result = cursor.fetchone()
            pfp_key = str(result['profile_picture'])
    
    with get_s3_client() as s3:
        response = s3.get_object(
            Bucket="geo-gemmer-images",
            Key=pfp_key
            )
        image_data = response['Body'].read()
        return image_data

def update_user_pfp(user_id, file_path):
    """
    Updates the profile picture of a user.

    Args:
        user_id (int): The ID of the user whose profile picture needs to be updated.
        filepath (str): The file path of the new profile picture.

    Returns:
        None
    """
    pfp_key = None
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    profile_picture
                FROM
                    geo_user
                WHERE
                    user_id = %s;
            ''', (user_id,))
            result = cursor.fetchone()
            pfp_key = str(result['profile_picture'])

    full_file_key = pfp_key
    with get_s3_client() as s3:
        s3.upload_fileobj(
            Fileobj=file_path,
            Bucket='geo-gemmer-images',
            Key=full_file_key
            )
    pass


def get_database_pfp(user_id):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    profile_picture
                FROM
                    geo_user
                WHERE
                    user_id = %s;
            ''', (user_id,))
            result = cursor.fetchone()
            return result['profile_picture']