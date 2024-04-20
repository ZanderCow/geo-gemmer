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
    skipper = 0
    # i know little about python but i hate these for loops and
    # don't have time to learn how to properly use them.
    for i in range(len(input)):
        i+=skipper
        if (input[i] == "'"):
            input = input[:i]+"'"+input[i:]
            skipper+=1
    
    #force trim. its ur fault if you fill your name with apostrophes anyway
    if (max_length != None and len(input) > max_length):
        input = input[:max_length]
        #just in case i cut off a double single quote
        if (max_length > 1 and input[max_length-1] == "'"):
            apostropheCounter = 0
            for i in range(len(input)):
                if input[i] == "'": apostropheCounter += 1
            if (apostropheCounter % 2 == 1):
                input = input[:max_length-1]
    
    return input