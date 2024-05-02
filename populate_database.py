import requests
import boto3
from io import BytesIO
from repositories.db import get_pool
from psycopg.rows import dict_row
import uuid
from repositories.gem_repository import create_new_gem_no_user, delete_gem
from repositories.gem_accessibility_repository import set_accesibility_for_gem
from repositories.images_repository import get_primary_image_for_hidden_gem
import random
from repositories.s3 import get_s3_client
import threading
from concurrent.futures import ThreadPoolExecutor

def download_image(image_url):
    """ Download image from a URL. """
    response = requests.get(image_url)
    if response.status_code == 200:
        return response.content
    return None

def create_hidden_gem_images(gem_id, image_url_1, image_url_2, image_url_3):
    '''
    Download images from URLs and upload them to an Amazon S3 server for a hidden gem.

    Parameters:
        gem_id (int): The ID of the hidden gem.
        image_url_1 (str): The URL for the first image to download and upload.
        image_url_2 (str): The URL for the second image to download and upload.
        image_url_3 (str): The URL for the third image to download and upload.
    '''
    # Generate unique file keys
    file_key_1 = f"gem-images/{uuid.uuid4()}.png"
    file_key_2 = f"gem-images/{uuid.uuid4()}.png"
    file_key_3 = f"gem-images/{uuid.uuid4()}.png"

    # Download images from URLs
    image_1 = download_image(image_url_1)
    image_2 = download_image(image_url_2)
    image_3 = download_image(image_url_3)

    if not all([image_1, image_2, image_3]):
        return False  # Return False if any image failed to download

    # Upload images to S3
    with get_s3_client() as s3:
        s3.put_object(Bucket='geo-gemmer-images', Key=file_key_1, Body=image_1)
        s3.put_object(Bucket='geo-gemmer-images', Key=file_key_2, Body=image_2)
        s3.put_object(Bucket='geo-gemmer-images', Key=file_key_3, Body=image_3)
    

    # Update database with new image keys
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


def create_and_populate_database_with_hidden_gems(
        gem_name,
        gem_type,
        latitude,
        longitude,
        image_1,
        image_2,
        image_3,
        ):
    """
    Create and populate the database with hidden gems.

    Args:
        gem_name (str): The name of the hidden gem.
        gem_type (str): The type or category of the hidden gem.
        latitude (float): The latitude coordinate of the hidden gem's location.
        longitude (float): The longitude coordinate of the hidden gem's location.
        image_1 (str): The path or URL of the first image of the hidden gem.
        image_2 (str): The path or URL of the second image of the hidden gem.
        image_3 (str): The path or URL of the third image of the hidden gem.
    """
    
    gem_id = create_new_gem_no_user(
        gem_name,
        gem_type,
        latitude,
        longitude
    )

    create_hidden_gem_images(
        gem_id,
        image_1,
        image_2,
        image_3
    )

    set_accesibility_for_gem(
        gem_id,
        wheelchair_accessible=bool(random.getrandbits(1)),
        service_animal_friendly=bool(random.getrandbits(1)),
        multilingual_support=bool(random.getrandbits(1)),
        braille_signage=bool(random.getrandbits(1)),
        hearing_assistance=bool(random.getrandbits(1)),
        large_print_materials=bool(random.getrandbits(1)),
        accessible_restrooms=bool(random.getrandbits(1))
    )

    try:
        get_primary_image_for_hidden_gem(gem_id)
    except:
        delete_gem(gem_id)  


    return

def parse_geogemmer_file(filename):
    # Types from the uploaded image
    types = ["Hiking Trail", "Restaurant", "Park", "Gym", "Museum", 
             "Beach", "Shopping Mall", "Movie Theater", "Zoo", "Aquarium"]
    
    gems = []

    with open(filename, 'r') as file:
        lines = file.readlines()

    gem_info = {}
    for line in lines:
        line = line.strip()
        if line and line[0].isdigit() and '. Name:' in line:  # Identifies the start of a new entry
            if gem_info:
                gems.append(gem_info)
                gem_info = {}
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            # Correctly format the key for images and strip number from name
            if key.startswith('Image'):
                key = 'Image ' + key.split()[-1]
            if 'Name' in key:
                key = 'Name'  # Standardize the key to "Name"
                value = value.split('. ', 1)[-1] if '. ' in value else value
            if 'Type' in key:
                value = random.choice(types)  # Assign a random type from the list

            gem_info[key] = value

    # Append the last entry if not empty
    if gem_info:
        gems.append(gem_info)

    return gems

# Example usage

filename = "geogemmer.txt"
geogemmer_data = parse_geogemmer_file(filename)
for file in geogemmer_data:
    create_and_populate_database_with_hidden_gems(
        file['Name'],
        file['Type'],
        float(file['Latitude']),
        float(file['Longitude']),
        file['Image 1'],
        file['Image 2'],
        file['Image 3']
    )