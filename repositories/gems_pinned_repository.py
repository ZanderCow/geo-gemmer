from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row
import datetime

def get_gems_pinned_by_user(user_id):
    '''
    Retrieves a list of all gems pinned by a given user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the visited gems. 
    
    Example: 
        >>> get_all_gems_pinned_by_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"
            }, 
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"        
            },
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_pinned': "2022-07-15"
                'gem_url': "/gem/67e55044-10b1-426f-9247-bb680e5fe0c8"      
            }         
        ]
    '''

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                SELECT
                    hg.name AS gem_name,
                    hg.gem_type,
                    hg.gem_id,
                    gp.date_pinned
                FROM
                    gems_pinned gp
                JOIN
                    hidden_gem hg ON gp.gem_id = hg.gem_id
                WHERE
                    gp.user_id = %s;
            ''', (user_id,))
            return cursor.fetchall()
        
def delete_pinned_gem_user(user_id, gem_pinned_id):
    '''
    Deletes a gem pinned by a user.

    Parameters:
        user_id (int): The ID of the user.
        gem_id (int): The ID of the gem.

    Returns:
        None
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
                DELETE FROM
                    gems_pinned
                WHERE
                    user_id = %s
                    AND gem_id = %s;
            ''', (user_id, gem_pinned_id))
            return True

def add_pinned_gem(user_id,gem_id, date_pinned):
    """
    Adds a gem to the pinned gems list of a user

    Parameters:
        user_id (String): The ID of the user.
        gem_id (String): The ID of the gem.

    Returns:
        True: If the gem was successfully added
    """
    current_date = datetime.date.today()

    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            
            # Check if the gem is already pinned
            cursor.execute('''
                    SELECT gem_pinned_id FROM gems_pinned
                    WHERE user_id = %s AND gem_id = %s;
                ''', (user_id, gem_id))
            
            existing_id = cursor.fetchone()
            
            if existing_id:
                return "gem already pinned"  # Return the existing gem_pinned_id if already pinned
            
            cursor.execute('''
                    INSERT INTO
                        gems_pinned(user_id, gem_id, date_pinned)
                    VALUES
                        (%s, %s, %s)
                    RETURNING gem_pinned_id;
                ''', (user_id, gem_id, date_pinned))
            return cursor.fetchone()
        

