from repositories.db import get_pool
from typing import Any


def get_images_for_a_hidden_gem(gem_id):
    '''
    Retrieve the images associated with a hidden gem from an Amazon S3 server.

    Parameters:
        gem_id (int): The ID of the hidden gem.

    Returns:
        str: The file location of the images on the Amazon S3 server.
    '''
    pass


def add_image_to_hidden_gem(gem_id, image_data):
    '''
    Adds an image to a hidden gem on an Amazon S3 server.

    Parameters:
        gem_id (int): The ID of the hidden gem.
        image_data (bytes): The image data to be uploaded.
        
    Returns:
        None
    '''
    pass