from psycopg.rows import dict_row
from repositories.db import get_pool
''''''
pool = get_pool()
with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''
            SELECT ST_Distance(
            'SRID=4326;POINT(-118.4079 33.9434)'::geography, -- Los Angeles (LAX)
            'SRID=4326;POINT(2.5559 49.0083)'::geography     -- Paris (CDG)
            );     
         ''')
            stuff = cursor.fetchall()
            print(stuff)

