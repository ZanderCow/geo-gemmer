from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row

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
                    gem_name,
                    gem_type,
                    date_pinned,
                    gem_url
                FROM
                    gems_pinned
                WHERE
                    user_id = %s;
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

