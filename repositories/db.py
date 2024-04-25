import os
from psycopg_pool import ConnectionPool

pool = None

def get_pool():
    global pool
    if pool is None:
        pool = ConnectionPool(
            conninfo=os.getenv('DATABASE_URL', ''),
            open=True,
        )
    return pool

def inflate_string(input:str, max_length:int|None=None) -> str:
    '''
    Put string in PostgreSQL form in case of apostrophe catastrophe

    Parameters:
        input (str): The string to be inflated
        max_length (int): Maximum size of the string in len(). e.g. Counting index 0 as length 1, index 1 as 2, etc.

    Returns:
        string
    '''
    #force trim. its ur fault if you try to fill the whole char limit
    if (max_length != None):
        input = force_trim(input, max_length)
    
    skipper = 0
    # i know little about python but i hate these for loops and
    # don't have time to learn how to properly use them.
    for i in range(len(input)):
        i+=skipper
        if (input[i] == "'"):
            input = input[:i]+"'"+input[i:]
            skipper+=1
    
    return input

def force_trim(input:str, max_length:int) -> str:
    '''
    Limit the length of a string in case of middle school hackers

    Parameters:
        input (str): The string to be trimmed
        max_length (int): Maximum size of the string in len(). e.g. Counting index 0 as length 1, index 1 as 2, etc.

    Returns:
        string
    '''
    if (len(input) > max_length):
        input = input[:max_length]
    return input