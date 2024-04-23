from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row


def get_all_gems_visited_by_user(user_id) -> list[dict[str, Any]]:
    '''
    Retrieves a list of all gems visited by a given user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        list[dict[str, Any]]: A list of dictionaries representing the visited gems. 
    
    Example: 
        >>> get_all_gems_visited_by_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        [
            {
                'gem_name': 'Rocky Mountian',
                'gem_type': 'Park',
                'date_visted': "2022-07-15"
            }, 
            {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'gem_name': 'Rocky Mountian',
                'date_visted': "2022-07-15"
            },
            {
                'gem_id': '67e55044-10b1-426f-9247-bb680e5fe0c8',
                'gem_name': 'Rocky Mountian',
                'date_visted': "2022-07-15"
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
                    gv.date_visited
                FROM
                    gems_visited gv
                JOIN
                    hidden_gem hg ON gv.gem_id = hg.gem_id
                WHERE
                    gv.user_id = %s;
            ''', (user_id,))
            return cursor.fetchall()

def add_gem_to_visited_list(user_id, gem_id, date_visited):
    '''
    Adds a gem to a user's visited list.

    Parameters:
        user_id (int): The ID of the user.
        gem_id (int): The ID of the gem.
        date_visited (str): The date the gem was visited.

    Returns:
        None
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                INSERT INTO gems_visited (user_id, gem_id, date_visited)
                VALUES (%s, %s, %s);
            ''', (user_id, gem_id, date_visited))

def get_distribution_of_hidden_gems_visited_by_a_user(user_id):
    '''
    Get the distribution of hidden gems visited by a user.

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict[str, int]: A dictionary with the distribution of hidden gems visited by a user.

    Example:
        >>> get_distribution_of_hidden_gems_visited_by_a_user(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            'Restaurant': 2,
            'Park': 1,
            'Museum': 1
        }  
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT hg.gem_type, COUNT(*) AS count
                FROM hidden_gem hg
                JOIN gems_visited gv ON hg.gem_id = gv.gem_id
                WHERE gv.user_id = %s
                GROUP BY hg.gem_type;
            ''', (user_id,))
            distribution = cursor.fetchall()
            return {row[0]: row[1] for row in distribution}

def get_hidden_gems_visited_by_month(user_id):
    '''
    Retrieves the number of hidden gems visited by a user for each month.

    This is for that table on the dashboard

    Parameters:
        user_id (int): The ID of the user.

    Returns:
        dict[str, int]: A dictionary with the number of hidden gems visited by month.

    Example:
        >>> get_hidden_gems_visited_by_month(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            'January': 3,
            'February': 2,
            'March': 1,
            ...
        }
    '''
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''
                SELECT EXTRACT(MONTH FROM date_visited) AS month, COUNT(*) AS count
                FROM gems_visited
                WHERE user_id = %s
                GROUP BY month;
            ''', (user_id,))
            monthly_visits = cursor.fetchall()
            months = {
                1: 'January',
                2: 'February',
                3: 'March',
                4: 'April',
                5: 'May',
                6: 'June',
                7: 'July',
                8: 'August',
                9: 'September',
                10: 'October',
                11: 'November',
                12: 'December'
            }
            return {months[row[0]]: row[1] for row in monthly_visits}