from repositories.db import get_pool
from typing import Any
from repositories.s3 import get_s3_client
import uuid
from psycopg.rows import dict_row



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
        s3.upload_fileobj( Fileobj=file_path, Bucket='geo-gemmer-images', Key=full_file_key)
        

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
        
def create_hidden_gem_images(gem_id, image_1, image_2, image_3):
    '''
    Upload images to an Amazon S3 server for a hidden gem.

    Parameters:
        gem_id (int): The ID of the hidden gem.
        image_1 (FileStorage): The first image file to upload.
        image_2 (FileStorage): The second image file to upload.
        image_3 (FileStorage): The third image file to upload.
    '''
    file_key_1 = f"gem-images/{uuid.uuid4()}.png"
    file_key_2 = f"gem-images/{uuid.uuid4()}.png"
    file_key_3 = f"gem-images/{uuid.uuid4()}.png"

    with get_s3_client() as s3:
        s3.upload_fileobj(Fileobj=image_1.stream, Bucket='geo-gemmer-images', Key=file_key_1)
        s3.upload_fileobj(Fileobj=image_2.stream, Bucket='geo-gemmer-images', Key=file_key_2)
        s3.upload_fileobj(Fileobj=image_3.stream, Bucket='geo-gemmer-images', Key=file_key_3)

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                INSERT INTO
                    image_group (gem_id, image_1, image_2, image_3)
                VALUES
                    (%s, %s, %s, %s);
            ''', (gem_id, file_key_1, file_key_2, file_key_3))

    return True



def get_hidden_gem_images(gem_id):
    '''
    Retrieve images of a hidden gem from an Amazon S3 server.

    Parameters:
        gem_id (int): The ID of the hidden gem.

    Returns:
        list: A list of file locations of the images on the Amazon S3 server.
    '''
    image_keys = None
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    image_1, image_2, image_3
                FROM
                    image_group
                WHERE
                    gem_id = %s;
            ''', (gem_id,))
            result = cursor.fetchone()
            image_keys = [result['image_1'], result['image_2'], result['image_3']]
    image_data = []
    with get_s3_client() as s3:
        for key in image_keys:
            response = s3.get_object( Bucket="geo-gemmer-images", Key=key)
            image_data.append(response['Body'].read())
    return image_data



def get_primary_image_for_hidden_gem(gem_id):
    '''
    gets the primary images for a hidden gem. Used for search
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    image_1
                FROM
                    image_group
                WHERE
                    gem_id = %s;
            ''', (gem_id,))
            result = cursor.fetchone()
            img = result['image_1']
            with get_s3_client() as s3:
                response = s3.get_object( Bucket="geo-gemmer-images", Key=img)
                image_data = response['Body'].read()
                return image_data


def update_gem_images(gem_id, image_1, image_2, image_3):
    '''
    Update the images of a hidden gem.

    Parameters:
        gem_id (int): The ID of the hidden gem.
        image_1 (FileStorage): The first image file to upload.
        image_2 (FileStorage): The second image file to upload.
        image_3 (FileStorage): The third image file to upload.
    '''
    file_key_1 = None
    file_key_2 = None
    file_key_3 = None
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    image_1, image_2, image_3
                FROM
                    image_group
                WHERE
                    gem_id = %s;
            ''', (gem_id,))
            result = cursor.fetchone()
            file_key_1 = result['image_1']
            file_key_2 = result['image_2']
            file_key_3 = result['image_3']


    with get_s3_client() as s3:
        s3.upload_fileobj(Fileobj=image_1.stream, Bucket='geo-gemmer-images', Key=file_key_1)
        s3.upload_fileobj(Fileobj=image_2.stream, Bucket='geo-gemmer-images', Key=file_key_2)
        s3.upload_fileobj(Fileobj=image_3.stream, Bucket='geo-gemmer-images', Key=file_key_3)

    return True