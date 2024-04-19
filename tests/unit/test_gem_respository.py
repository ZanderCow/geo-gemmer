"""
write test code
"""
import pytest
from repositories import gem_repository as repo
from repositories.db import get_pool, inflate_string
from repositories.gem_repository import accessibility_class
from repositories import review_repository as reviewpo
from repositories import user_repository as userrepo

#this is just a debug tool to reset the database
def reset_database():
    pool = get_pool()
    with pool.connection() as conn:
        with conn.cursor() as cursor:
            cursor.execute(f'''DELETE FROM hidden_gem;
                                DELETE FROM review;
                                DELETE FROM geo_user;''')


def test_making_gem():
    reset_database()
    newgemid = repo.create_new_gem("nameo", "big place", 80.843124, 35.227085, False)
    
    newgem = repo.get_hidden_gem_by_id(newgemid)
    #make sure the new gem has all the right stuff
    assert newgem['name'] == "nameo"
    assert newgem['latitude'] == 35.227085
    assert newgem['longitude'] == 80.843124
    assert newgem['gem_type'] == "big place"
    assert newgem['times_visited'] == 0
    assert newgem['user_created'] == False
    assert newgem['image_1'] == None


def test_adding_gems_to_repo():
    reset_database()
    newgemid = repo.create_new_gem("nameo", "big place", -80.843124, 35.227085, False, "/static/img/neckbeard.png", "no, u", "")
    newgem = repo.get_hidden_gem_by_id(newgemid)

    #make sure the data is right
    assert newgem['name'] == "nameo"
    assert newgem['longitude'] == -80.843124
    assert newgem['latitude'] == 35.227085
    assert newgem['gem_type'] == "big place"
    assert newgem['times_visited'] == 0
    assert newgem['user_created'] == False
    assert newgem['image_1'] == "/static/img/neckbeard.png"
    assert newgem['image_2'] == "no, u"
    assert newgem['image_3'] == None

    #see ALL gems
    all_gems = repo.get_all_gems()
    assert all_gems[0]['name'] == "nameo"
    assert all_gems[0]['longitude'] == -80.843124
    assert all_gems[0]['latitude'] == 35.227085
    assert all_gems[0]['gem_type'] == "big place"
    assert all_gems[0]['times_visited'] == 0
    assert all_gems[0]['user_created'] == False

    #add second gem
    repo.create_new_gem("name2", "bigger place", -80, 38, False)
    all_gems = repo.get_all_gems()
    assert all_gems[1]['name'] == "name2"
    assert all_gems[1]['longitude'] == -80
    assert all_gems[1]['latitude'] == 38
    assert all_gems[1]['gem_type'] == "bigger place"
    assert all_gems[1]['times_visited'] == 0
    assert all_gems[1]['user_created'] == False

    #test distance
    all_gems = repo.get_all_gems_ordered_by_nearest(-80, 38)
    assert all_gems[0]['name'] == "name2"
    assert all_gems[0]['longitude'] == -80
    assert all_gems[0]['latitude'] == 38
    assert all_gems[0]['gem_type'] == "bigger place"
    assert all_gems[0]['times_visited'] == 0
    assert all_gems[0]['user_created'] == False
    
    assert all_gems[1]['name'] == "nameo"
    assert all_gems[1]['longitude'] == -80.843124
    assert all_gems[1]['latitude'] == 35.227085
    assert all_gems[1]['gem_type'] == "big place"
    assert all_gems[1]['times_visited'] == 0
    assert all_gems[1]['user_created'] == False

    
    all_gems = repo.get_all_gems_within_a_certain_distance_from_the_user(-80, 38, 320)
    assert all_gems[0]['name'] == "name2"
    assert all_gems[0]['longitude'] == -80
    assert all_gems[0]['latitude'] == 38
    assert all_gems[0]['gem_type'] == "bigger place"
    assert all_gems[0]['times_visited'] == 0
    assert all_gems[0]['user_created'] == False
    
    assert all_gems[1]['name'] == "nameo"
    assert all_gems[1]['longitude'] == -80.843124
    assert all_gems[1]['latitude'] == 35.227085
    assert all_gems[1]['gem_type'] == "big place"
    assert all_gems[1]['times_visited'] == 0
    assert all_gems[1]['user_created'] == False

    all_gems = repo.get_all_gems_within_a_certain_distance_from_the_user(-80, 38, 320, 1)

    assert all_gems[0]['name'] == "nameo"
    assert all_gems[0]['longitude'] == -80.843124
    assert all_gems[0]['latitude'] == 35.227085
    assert all_gems[0]['gem_type'] == "big place"
    assert all_gems[0]['times_visited'] == 0
    assert all_gems[0]['user_created'] == False

    #delet
    reset_database()


def test_modifying_gem():
    reset_database()
    newgemid = repo.create_new_gem("nameo", "big place", -80.843124, 35.227085, False)
    
    #modify
    repo.change_gem_name(newgemid, "flameo")
    repo.change_gem_type(newgemid, "uss lollipop")
    repo.change_gem_location(newgemid, 74.656, 74.205)

    #data grab
    newgem = repo.get_hidden_gem_by_id(newgemid)

    #check if modified
    assert newgem['name'] == 'flameo'
    assert newgem['gem_type'] == 'uss lollipop'
    assert newgem['longitude'] == 74.656
    assert newgem['latitude'] == 74.205

    #make more people visit
    repo.increment_gem_times_visited(newgemid)
    newgem = repo.get_hidden_gem_by_id(newgemid)
    assert newgem['times_visited'] == 1

    #delet
    repo.delete_hidden_gem(newgemid)
    assert repo.get_hidden_gem_by_id(newgemid) is None

def test_accessibility():
    reset_database()
    newgemid = repo.create_new_gem("nameo", "big place", -80.843124, 35.227085, False)
    access = accessibility_class()
    access.braille_signage = True
    access.accessible_restrooms = True

    repo.change_accessibility(newgemid, access)
    newgem = repo.get_hidden_gem_by_id(newgemid)

    assert newgem['wheelchair_accessible'] == False
    assert newgem['service_animal_friendly'] ==  False
    assert newgem['multilingual_support'] ==  False
    assert newgem['braille_signage'] ==  True
    assert newgem['hearing_assistance'] ==  False
    assert newgem['large_print_materials'] ==  False
    assert newgem['accessible_restrooms'] == True

    access.accessible_restrooms = False
    listo = repo.filtered_get_all_gems_within_a_certain_distance_from_the_user(-80, 35, 100, "big place", access, 0)
    assert len(listo) == 1
    assert listo[0]['name'] == 'nameo'

    listo = repo.filtered_search_all_gems_within_a_certain_distance_from_the_user("name", -80, 35, 100, "big place", access, 0)
    assert len(listo) == 1

    
    listo = repo.filtered_search_all_gems_within_a_certain_distance_from_the_user("name", -80, 35, 100, None, access, 0)
    assert len(listo) == 1
    listo = repo.filtered_get_all_gems_within_a_certain_distance_from_the_user(-80, 35, 100, None, access, 0)
    assert len(listo) == 1

    access.service_animal_friendly = True
    listo = repo.filtered_search_all_gems_within_a_certain_distance_from_the_user("name", -80, 35, 100, "big place", access, 0)
    assert len(listo) == 0

    
    newgemid = repo.create_new_gem("DUNKIN' DONUTS", "DUNKIN'", -80.843124, 35.227085, False)
    newgem = repo.get_hidden_gem_by_id(newgemid)
    assert newgem['name'] == "DUNKIN' DONUTS"
    assert newgem['gem_type'] == "DUNKIN'"

def test_inflater():
    #test the apostrophes
    stringy = "'this' string's stringin'"
    stringy = inflate_string(stringy)
    assert stringy == "''this'' string''s stringin''"

    stringy = inflate_string("dunkin'")
    assert stringy == "dunkin''"

    #TEST THE LIMITS; MUST BE ROBUST OR ELSE
    stringy = inflate_string("this is a limited string", 9)
    assert stringy == "this is a"
    stringy = inflate_string("this is 'a limited string", 9)
    assert stringy == "this is "
    stringy = inflate_string("this i''''a funny string", 9)
    assert stringy == "this i''"
    stringy = inflate_string("this i '''a less funny string", 9)
    assert stringy == "this i ''"

def test_reviews():
    shrunk = reviewpo._shrink_rating(6)
    assert reviewpo._expand_rating(shrunk) is 5
    for i in range(5):
        shrunk = reviewpo._shrink_rating(i)
        assert reviewpo._expand_rating(shrunk) is i
    shrunk = reviewpo._shrink_rating(-1)
    assert reviewpo._expand_rating(shrunk) is 0

    newgemid = repo.create_new_gem("THIS IS A PLACE", "no'u", -80.843124, 35.227085, False)
    user_id = userrepo.create_new_user('nameo', 'nameom')
    reviewpo.add_review_to_hidden_gem(newgemid, user_id, 4, "This place's food is awful")
    reviewpo.add_review_to_hidden_gem(newgemid, user_id, 4, "This place's food is awful")
    reviewpo.add_review_to_hidden_gem(newgemid, user_id, 4, "This place's food is awful")
    reviewpo.add_review_to_hidden_gem(newgemid, user_id, 4, "This place's food is awful")
    reviewpo.add_review_to_hidden_gem(newgemid, user_id, 4, "This place's food is awful")

    print(newgemid, end='\n')
    reviews = reviewpo.get_all_reviews_for_a_hidden_gem(newgemid)
    print(len(reviews))
    review = reviews[0]
    assert review['user_id'] == str(user_id)
    assert review['gem_id'] == newgemid
    assert review['rating'] == 4
    assert review['review'] == "This place's food is awful"
    assert review['date'][2] == '/'
    assert review['date'][5] == '/'
    assert len(review['date']) == 10


'''
def test_adding_several_gems():
    repo = gem_repository.get_gem_repository()
    newgem = repo.create_hidden_gem("nameo", 32, 40, "big place", 0, False, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    newgem1 = repo.create_hidden_gem("flameo", 33, 50, "bigger place", 0, False, "https://youtu.be/_stbdjS_fbs&t=156s")
    newgem2 = repo.create_hidden_gem("moneo", 35, 70, "big palace", 0, False, "woolgathering")
    newgem3 = repo.create_hidden_gem("MONEO", 35.227085, 80.843124, "bigger palace", 0, False, "stop woolgathering moneo")
    newgem4 = repo.create_hidden_gem("ROMANS", 1, 2, "gross protuberance", 0, False, "beefswelling")
    newgem5 = repo.create_hidden_gem("Fiddlebert", 3, 4, "Lithuanian", 0, True, "https://www.reddit.com/r/Pikmin/comments/14kkxz1/im_really_curious_to_see_what_any_other_gamecube/")

    #test getting
    assert repo.get_gem_id_by_name("nameo") is newgem.id
    assert repo.get_hidden_gem_by_id(newgem.id) is newgem

    assert repo.get_gem_id_by_name("flameo") is newgem1.id
    assert repo.get_hidden_gem_by_id(newgem1.id) is newgem1

    assert repo.get_gem_id_by_name("moneo") is newgem2.id
    assert repo.get_hidden_gem_by_id(newgem2.id) is newgem2

    assert repo.get_gem_id_by_name("MONEO") is newgem3.id
    assert repo.get_hidden_gem_by_id(newgem3.id) is newgem3

    assert repo.get_gem_id_by_name("ROMANS") is newgem4.id
    assert repo.get_hidden_gem_by_id(newgem4.id) is newgem4

    assert repo.get_gem_id_by_name("Fiddlebert") is newgem5.id
    assert repo.get_hidden_gem_by_id(newgem5.id) is newgem5

    #test modifying name, make sure no others are affected
    repo.update_name(newgem.id, "nameO")
    assert repo.get_name(newgem.id) is "nameO"
    assert repo.get_name(newgem1.id) is "flameo"
    assert repo.get_name(newgem2.id) is "moneo"
    assert repo.get_name(newgem3.id) is "MONEO"
    assert repo.get_name(newgem4.id) is "ROMANS"
    assert repo.get_name(newgem5.id) is "Fiddlebert"

    #test modifying coordinates, make sure no others are affected
    repo.update_cordinates(newgem.id, 10, 4)
    assert repo.get_cordinates(newgem.id) == (10, 4)
    assert repo.get_cordinates(newgem1.id) == (33, 50)
    assert repo.get_cordinates(newgem2.id) == (35, 70)
    assert repo.get_cordinates(newgem3.id) == (35.227085, 80.843124)
    assert repo.get_cordinates(newgem4.id) == (1, 2)
    assert repo.get_cordinates(newgem5.id) == (3, 4)

    #test modifying coordinates, make sure no others are affected
    repo.update_gem_type(newgem.id, "newtype")
    assert repo.get_gem_type(newgem.id) is "newtype"
    assert repo.get_gem_type(newgem1.id) is "bigger place"
    assert repo.get_gem_type(newgem2.id) is "big palace"
    assert repo.get_gem_type(newgem3.id) is "bigger palace"
    assert repo.get_gem_type(newgem4.id) is "gross protuberance"
    assert repo.get_gem_type(newgem5.id) is "Lithuanian"
    
    #test modifying times visited, make sure no others are affected
    repo.update_times_visited(newgem.id, 4)
    assert repo.get_times_visited(newgem.id) is 4
    assert repo.get_times_visited(newgem1.id) is 0
    assert repo.get_times_visited(newgem2.id) is 0
    assert repo.get_times_visited(newgem3.id) is 0
    assert repo.get_times_visited(newgem4.id) is 0
    assert repo.get_times_visited(newgem5.id) is 0
    repo.increment_times_visited(newgem.id)
    assert repo.get_times_visited(newgem.id) is 5
    assert repo.get_times_visited(newgem1.id) is 0
    assert repo.get_times_visited(newgem2.id) is 0
    assert repo.get_times_visited(newgem3.id) is 0
    assert repo.get_times_visited(newgem4.id) is 0
    assert repo.get_times_visited(newgem5.id) is 0
    
    #test modifying user created, make sure no others are affected
    repo.update_user_created(newgem.id, True)
    assert repo.get_user_created(newgem.id) is True
    assert repo.get_user_created(newgem1.id) is False
    assert repo.get_user_created(newgem2.id) is False
    assert repo.get_user_created(newgem3.id) is False
    assert repo.get_user_created(newgem4.id) is False
    assert repo.get_user_created(newgem5.id) is True

    
    #test modifying link, make sure no others are affected
    repo.update_website_link(newgem4.id, "https://youtu.be/CnuaXR933mA")
    assert repo.get_website_link(newgem.id) is "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    assert repo.get_website_link(newgem1.id) is "https://youtu.be/_stbdjS_fbs&t=156s"
    assert repo.get_website_link(newgem2.id) is "woolgathering"
    assert repo.get_website_link(newgem3.id) is "stop woolgathering moneo"
    assert repo.get_website_link(newgem4.id) is "https://youtu.be/CnuaXR933mA"
    assert repo.get_website_link(newgem5.id) is "https://www.reddit.com/r/Pikmin/comments/14kkxz1/im_really_curious_to_see_what_any_other_gamecube/"

    #delete all
    repo.clear_db()'''