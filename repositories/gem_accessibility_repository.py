from repositories.db import get_pool
from typing import Any
from psycopg.rows import dict_row


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
                           wheelchair_accessible, 
                           service_animal_friendly,
                            multilingual_support, 
                            braille_signage, 
                           hearing_assistance, 
                           large_print_materials, 
                           accessible_restrooms 
                            
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
        accessibility_info (dict[str, Any]): A dictionary containing the accessibility information for the hidden gem.

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
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute('''UPDATE accessibility 
                           SET wheelchair_accessible = %s, 
                           service_animal_friendly = %s,
                            multilingual_support = %s, 
                            braille_signage = %s, 
                           hearing_assistance = %s, 
                           large_print_materials = %s, 
                           accessible_restrooms = %s 
                            
                           WHERE gem_id = %s;'''
            , (accessibility_info['wheelchair_accessible'], accessibility_info['service_animal_friendly'], accessibility_info['multilingual_support'], accessibility_info['braille_signage'], accessibility_info['hearing_assistance'], accessibility_info['large_print_materials'], accessibility_info['accessible_restrooms'], gem_id))

    # Add your code here


    