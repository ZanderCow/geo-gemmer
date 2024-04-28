from psycopg.rows import dict_row
from repositories.db import get_pool
import pprint

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
    keeps the tables, but wipes all the data
    '''
    pass

add_new_stuff()
print_all_users()
print_all_hidden_gems()
print_all_reviews()
print_all_accesibility_stuff()
print_all_gems_visited()
print_all_gems_pinned()
print_all_images_for_all_gems()

