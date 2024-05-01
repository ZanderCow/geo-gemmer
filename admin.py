from psycopg.rows import dict_row
from repositories.db import get_pool
from repositories.s3 import get_s3_client
import boto3
import os
import pprint
from dotenv import load_dotenv

'''
These are pretty much Admin Commands that manage the database it's just easier for me to do this.
So if something breaks, we can just delete it
NOTE: We will delete this when we get to production
'''


def add_new_stuff():
    '''
    Adds the new stuff to the database that we already have done 
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                ALTER TABLE 
                    hidden_gem 
                ADD COLUMN 
                    user_id UUID REFERENCES geo_user(user_id) ON DELETE CASCADE
                '''
            )

def print_all_users():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM geo_user;
               
            ''')
            data = cursor.fetchall()
            print("users:")
            pprint.pprint(data)
            print()
            return

def print_all_hidden_gems():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM hidden_gem;
               
            ''')
            data = cursor.fetchall()
            print("hidden gems:")
            pprint.pprint(data)
            print()
            return

def print_all_reviews():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM review;
               
            ''')
            data = cursor.fetchall()
            print("reviews:")
            pprint.pprint(data)
            print()
            return

def print_all_accesibility_stuff():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM accessibility;
               
            ''')
            data = cursor.fetchall()
            print("accessibility:")
            pprint.pprint(data)
            print()
            return

def print_all_gems_visited():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM gems_visited;
               
            ''')
            data = cursor.fetchall()
            print("gems visited:")
            pprint.pprint(data)
            print()
            return

def print_all_gems_pinned():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM gems_pinned;
               
            ''')
            data = cursor.fetchall()
            print("gems pinned:")
            pprint.pprint(data)
            print()
            return

def delete_all_folder_contents():
    bucket_name = 'geo-gemmer-images'
    with get_s3_client() as s3:
        # Use a paginator to list all objects in the bucket by folders
        paginator = s3.get_paginator('list_objects_v2')
        result = paginator.paginate(Bucket=bucket_name, Delimiter='/')

        for prefix in result.search('CommonPrefixes'):
            if prefix:
                folder_name = prefix['Prefix']
                print(f"Deleting contents of folder: {folder_name}")
                # List all objects in the specified folder
                response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name)
                while response.get('Contents'):
                    # Delete the objects found
                    delete_keys = {'Objects': [{'Key': obj['Key']} for obj in response['Contents']]}
                    s3.delete_objects(Bucket=bucket_name, Delete=delete_keys)
                    if response['IsTruncated']:  # Check if there are more files to list
                        response = s3.list_objects_v2(Bucket=bucket_name, Prefix=folder_name, ContinuationToken=response['NextContinuationToken'])
                    else:
                        break

def print_all_images_for_all_gems():
    '''
    Prints everything in the database
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
               
                SELECT * FROM image_group;
               
            ''')
            data = cursor.fetchall()
            print("images for all gems:")
            pprint.pprint(data)
            print()
            return


def wipe_database():
    '''
    Keeps the tables, but wipes all the data
    '''
    print("Fetching connection pool...")
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            print("Executing TRUNCATE on all tables...")
            cursor.execute('''
                DO
                $$
                DECLARE
                    r RECORD;
                BEGIN
                    -- Loop through all tables in the 'geogemmer' schema
                    FOR r IN (SELECT tablename FROM pg_tables WHERE schemaname = 'geogemmer')
                    LOOP
                        -- Execute a TRUNCATE statement for each table
                        EXECUTE 'TRUNCATE TABLE geogemmer.' || quote_ident(r.tablename) || ' RESTART IDENTITY CASCADE';
                        RAISE NOTICE 'Truncated table: %', r.tablename;
                    END LOOP;
                END;
                $$;
            ''')
            print("Truncate operations completed.")
            
            return


def print_everything():
    '''
    Prints everything in the database
    '''
    print_all_users()
    print_all_hidden_gems()
    print_all_reviews()
    print_all_accesibility_stuff()
    print_all_gems_visited()
    print_all_gems_pinned()
    print_all_images_for_all_gems()
    return
# Call the function to test

'''
dotenv_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path)

print(os.getenv('AWS_ACCESS_KEY_ID'))
'''



