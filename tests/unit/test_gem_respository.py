"""
write test code
"""
import pytest
from repositories import gem_repository as repo
from repositories import gem_accessibility_repository as accessirepo
from repositories.db import get_pool, inflate_string
from repositories.gem_accessibility_repository import accessibility_class
from repositories import review_repository as reviewpo
from repositories import user_repository as userrepo
from datetime import datetime

#this is just a debug tool to reset the database
def _reset_database():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''DELETE FROM hidden_gem;
                                DELETE FROM review;
                                DELETE FROM geo_user;''')


def test_distance():
    _reset_database()
    newuser = str(userrepo.create_new_user("namea", "hotman"))
    newgemid = str(repo.create_new_gem("nameo", "big place", 35.227085, -80.843124, newuser))

    #distance
    gemmy = repo.get_gem_distance_from_user(newgemid, 35.24, -80.85112)[0]
    assert gemmy['distance'] > 0.99 and gemmy['distance'] < 1.01


    #search
    gemmy = repo.search_for_gems('', 0, 35.24, -80.85112, '', None, None, None, None, None, None, None, 1000)

    assert len(gemmy) == 1
    gemmy = gemmy[0]
    assert gemmy['distance'] > 0.99 and gemmy['distance'] < 1.01
    
    newgemid = str(repo.create_new_gem("nameo", "big place", 35.227085, -80.843124, newuser))

    #distance
    gemmy = repo.get_gem_distance_from_user(newgemid, -35.24, 80.85112)[0]
    assert gemmy['distance'] == 11409.7602
    
    gemmy = repo.search_for_gems('', 0, -35.24, 80.85112, '', None, None, None, None, None, None, None, 100000000)[0]
    assert gemmy['distance'] == 11409.7602

def test_making_gem():
    _reset_database()
    newuser = str(userrepo.create_new_user("nameo", "hotman"))
    newgemid = str(repo.create_new_gem("nameo", "big place", 35.227085, 80.843124, newuser))
    
    
    newgem = repo.get_basic_gem_info(newgemid)[0]
    #make sure the new gem has all the right stuff
    assert newgem['user_id'] == newuser
    assert str(newgem['gem_id']) == newgemid
    assert newgem['name'] == "nameo"
    assert newgem['gem_type'] == "big place"
    assert newgem['times_visited'] == 0

def test_adding_gems_to_repo():
    _reset_database()
    newuser = str(userrepo.create_new_user("nameo", "hotman"))
    newgemid = str(repo.create_new_gem("nameo", "big place", 35.227085, -80.843124, newuser))
    newgem = repo.get_basic_gem_info(newgemid)[0]

    #make sure the data is right
    assert newgem['user_id'] == newuser
    assert newgem['gem_id'] == newgemid
    assert newgem['name'] == "nameo"
    assert newgem['gem_type'] == "big place"
    assert newgem['times_visited'] == 0

    #delet
    _reset_database()


def test_modifying_gem():
    _reset_database()
    newuser = str(userrepo.create_new_user("namea", "hotman"))
    newgemid = repo.create_new_gem("nameo", "big place", -80.843124, 35.227085, newuser)
    
    #modify
    repo.change_gem_name(newgemid, "flameo")
    repo.change_gem_type(newgemid, "uss lollipop")
    repo.change_gem_location(newgemid, 74.205, 74.656)

    #data grab
    newgem = repo.get_basic_gem_info(newgemid)[0]

    #check if modified
    assert newgem['name'] == 'flameo'
    assert newgem['gem_type'] == 'uss lollipop'
    assert newgem['longitude'] == 74.205
    assert newgem['latitude'] == 74.656

    #make more people visit
    repo.increment_gem_times_visited(newgemid)
    newgem = repo.get_basic_gem_info(newgemid)[0] # dang zanders rewrite removed the [0] so i have to do it its so annoying
    assert newgem['times_visited'] == 1

    #delet
    repo.delete_gem(newgemid)
    assert len(repo.get_basic_gem_info(newgemid)) == 0

def test_accessibility():
    _reset_database()
    newuser = str(userrepo.create_new_user("namea", "hotman"))
    newgemid = repo.create_new_gem("nameo", "big place", 35.227085, -80.843124, newuser)
    access = accessibility_class()
    access.braille_signage = True
    access.accessible_restrooms = True

    accessirepo.set_accesibility_for_hidden_gem(newgemid, access)
    newgem = accessirepo.get_accesibility_for_hidden_gem(newgemid)

    assert newgem['wheelchair_accessible'] == False
    assert newgem['service_animal_friendly'] ==  False
    assert newgem['multilingual_support'] ==  False
    assert newgem['braille_signage'] ==  True
    assert newgem['hearing_assistance'] ==  False
    assert newgem['large_print_materials'] ==  False
    assert newgem['accessible_restrooms'] == True

    listo = repo.search_for_gems('', 0, 35, -80, "big place", access.wheelchair_accessible, access.service_animal_friendly, access.multilingual_support, access.braille_signage, access.hearing_assistance, access.large_print_materials, access.accessible_restrooms, 51)
    access.accessible_restrooms = False
    assert len(listo) == 1
    assert listo[0]['name'] == 'nameo'

    listo = repo.search_for_gems('nameo', 0, 35, -80, '', access.wheelchair_accessible, access.service_animal_friendly, access.multilingual_support, access.braille_signage, access.hearing_assistance, access.large_print_materials, access.accessible_restrooms, 51)
    assert len(listo) == 1
    assert listo[0]['name'] == 'nameo'
