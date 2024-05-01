from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row

def create_accesibility_for_hidden_gem(gem_id, 
        wheelchair_accessible: bool=False,
        service_animal_friendly : bool=False, 
        multilingual_support : bool=False, 
        braille_signage : bool=False, 
        hearing_assistance : bool=False, 
        large_print_materials : bool=False, 
        accessible_restrooms : bool=False
        ):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO accessibility 
                (gem_id, 
                wheelchair_accessible, 
                service_animal_friendly, 
                multilingual_support, 
                braille_signage,
                hearing_assistance, 
                large_print_materials, accessible_restrooms
                ) 

                VALUES (%s, %s, %s, %s, %s, %s, %s, %s);'''
            , (gem_id,
               wheelchair_accessible, 
               service_animal_friendly, 
               multilingual_support, 
               braille_signage, 
               hearing_assistance, 
               large_print_materials, 
               accessible_restrooms
               )
            )
        return True
    

def get_accesibility_for_hidden_gem(gem_id):
    """
    Retrieves the accessibility information for a hidden gem.

    Args:
        gem_id (Any): The ID of the hidden gem.

    Returns:
        dict[str, Any]: A dictionary representing the accessibility information for the hidden gem.

    Example:
        >>> get_accesibility_for_hidden_gem(67e55044-10b1-426f-9247-bb680e5fe0c8)
        {
            'wheelchair_accessible': True,
            'service_animal_friendly': True,
            'multilingual_support': True,
            'braille_signage': True,
            'hearing_assistance': True,
            'large_print_materials': True,
            'accessible_restrooms': True
        }
    """
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor(row_factory=dict_row) as cursor:
            cursor.execute('''SELECT 
                           
                           *
                            
                           FROM accessibility 
                           
                           
                           WHERE gem_id = %s;'''
            , (gem_id,))
            return cursor.fetchone()

    # Add your code here

def set_accesibility_for_hidden_gem(gem_id, accessibility_info):
    """
    Updates the accessibility information for a hidden gem.

    Args:
        gem_id (Any): The ID of the hidden gem.
        accessibility_info (accessibility_class): A dictionary containing the accessibility information for the hidden gem.

    Returns:
        None

    Example:
        >>> set_accesibility_for_hidden_gem(67e55044-10b1-426f-9247-bb680e5fe0c8, {
            'wheelchair_accessible': True,
            'service_animal_friendly': True,
            'multilingual_support': True,
            'braille_signage': True,
            'hearing_assistance': True,
            'large_print_materials': True,
            'accessible_restrooms': True
        })
    """
    strin = accessibility_info.update_string()
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''UPDATE accessibility 
                           SET {strin}
                           WHERE gem_id = '{gem_id}';''')


def set_accesibility_for_gem(gem_id, 
        wheelchair_accessible: bool=False,
        service_animal_friendly : bool=False, 
        multilingual_support : bool=False, 
        braille_signage : bool=False, 
        hearing_assistance : bool=False, 
        large_print_materials : bool=False, 
        accessible_restrooms : bool=False
        ):
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''
            UPDATE accessibility 
                           
            SET 
            wheelchair_accessible = {wheelchair_accessible},
            service_animal_friendly = {service_animal_friendly},
            multilingual_support = {multilingual_support},
            braille_signage = {braille_signage},
            hearing_assistance = {hearing_assistance},
            large_print_materials = {large_print_materials},
            accessible_restrooms = {accessible_restrooms}
            WHERE gem_id = '{gem_id}';'''
            )
        return True
    
class accessibility_class:
    def __init__(self, wheelchair:bool=False, service_animal:bool=False, multilingual:bool=False, braille:bool=False, hearing_assistance:bool=False, large_print:bool=False, restrooms:bool=False):
        self.wheelchair_accessible = wheelchair
        self.service_animal_friendly = service_animal
        self.multilingual_support = multilingual
        self.braille_signage = braille
        self.hearing_assistance = hearing_assistance
        self.large_print_materials = large_print
        self.accessible_restrooms = restrooms
    
    def has_a_true(self):
        return self.wheelchair_accessible or self.service_animal_friendly or self.multilingual_support or self.braille_signage or self.hearing_assistance or self.large_print_materials or self.accessible_restrooms

    def to_string(self):
        stringy = ''
        if self.wheelchair_accessible:
            stringy += " AND wheelchair_accessible = true"
        if self.service_animal_friendly:
            stringy += " AND service_animal_friendly = true"
        if self.multilingual_support:
            stringy += " AND multilingual_support = true"
        if self.braille_signage:
            stringy += " AND braille_signage = true"
        if self.hearing_assistance:
            stringy += " AND hearing_assistance = true"
        if self.large_print_materials:
            stringy += " AND large_print_materials = true"
        if self.accessible_restrooms:
            stringy += " AND accessible_restrooms = true"
        return stringy
    
    def update_string(self):
        stringy = ' wheelchair_accessible = '+('true,' if self.wheelchair_accessible else 'false,')
        stringy +=  ' service_animal_friendly = '+('true,' if self.service_animal_friendly else 'false,')
        stringy +=  ' multilingual_support = '+('true,' if self.multilingual_support else 'false,')
        stringy +=  ' braille_signage = '+('true,' if self.braille_signage else 'false,')
        stringy +=  ' hearing_assistance = '+('true,' if self.hearing_assistance else 'false,')
        stringy +=  ' large_print_materials = '+('true,' if self.large_print_materials else 'false,')
        stringy +=  ' accessible_restrooms = '+('true,' if self.accessible_restrooms else 'false,')
        
        #remove the last comma
        if (len(stringy) > 0):
            stringy = stringy[0:-1]+' '

        return stringy
    
    def values(self):
        stringy += (' true,' if self.wheelchair_accessible else 'false,')
        stringy += (' true,' if self.service_animal_friendly else 'false,')
        stringy += (' true,' if self.multilingual_support else 'false,')
        stringy += (' true,' if self.braille_signage else 'false,')
        stringy += (' true,' if self.hearing_assistance else 'false,')
        stringy += (' true,' if self.large_print_materials else 'false,')
        stringy += (' true,' if self.accessible_restrooms else 'false,')