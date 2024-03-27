"""
write test code
"""
import pytest
from repositories import gem_repository
from models.hidden_gem import HiddenGem


def test_making_gem():
    newgem = HiddenGem("nameo", 1234, 35.227085, 80.843124, "big place", 0, False, "https://www.youtube.com/watch?v=dQw4w9WgXcQ", False)
    
    #make sure the new gem has all the right stuff
    assert newgem.name is "nameo"
    assert newgem.id is 1234
    assert newgem.latitude is 35.227085
    assert newgem.longitude is 80.843124
    assert newgem.gem_type is "big place"
    assert newgem.times_visited is 0
    assert newgem.user_created is False
    assert newgem.website_link is "https://www.youtube.com/watch?v=dQw4w9WgXcQ"


def test_adding_gem():
    repo = gem_repository.get_gem_repository()
    newgem = repo.create_hidden_gem("nameo", 35.227085, 80.843124, "big place", 0, False, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    new_id = repo.get_gem_id_by_name("nameo")

    #make sure the data is right
    assert newgem.name is "nameo"
    assert newgem.id is new_id
    assert newgem.latitude is 35.227085
    assert newgem.longitude is 80.843124
    assert newgem.gem_type is "big place"
    assert newgem.times_visited is 0
    assert newgem.user_created is False
    assert newgem.website_link is "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

    #make sure its in the repo
    assert repo.get_hidden_gem_by_id(new_id) is newgem

    #see ALL gems
    all_gems = repo.get_all_hidden_gems()
    assert all_gems[new_id] is newgem

    #delet
    repo.delete_hidden_gem(new_id)
    assert repo.get_hidden_gem_by_id(new_id) is None

def test_modifying_gem():
    repo = gem_repository.get_gem_repository()
    newgem = repo.create_hidden_gem("nameo", 35.227085, 80.843124, "big place", 0, False, "https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    
    #modify name
    repo.update_name(newgem.id, "flameo")
    assert newgem.name is "flameo"
    assert repo.get_name(newgem.id) is "flameo"

    #modify coordinates
    repo.update_cordinates(newgem.id, 74.656, 74.205)
    assert newgem.latitude is 74.656
    assert newgem.longitude is 74.205
    assert repo.get_cordinates(newgem.id) == (74.656, 74.205)

    #modify gem type
    repo.update_gem_type(newgem.id, "uss lollipop")
    assert newgem.gem_type is "uss lollipop"
    assert repo.get_gem_type(newgem.id) is "uss lollipop"

    #make more people visit
    repo.update_times_visited(newgem.id, 5)
    assert newgem.times_visited is 5
    assert repo.get_times_visited(newgem.id) is 5

    repo.increment_times_visited(newgem.id)
    assert newgem.times_visited is 6
    assert repo.get_times_visited(newgem.id) is 6

    #gaslight the new gem into thinking its adopted
    repo.update_user_created(newgem.id, True)
    assert newgem.user_created is True
    assert repo.get_user_created(newgem.id) is True

    #give the link the master sword
    repo.update_website_link(newgem.id, "https://youtu.be/_stbdjS_fbs&t=156s")
    assert newgem.website_link is "https://youtu.be/_stbdjS_fbs&t=156s"
    assert repo.get_website_link(newgem.id) is "https://youtu.be/_stbdjS_fbs&t=156s"

    '''#keep this here for when we finish setting up accessibility
    repo.update_accessibility(newgem.id, False)
    assert newgem.accessibility is False
    assert repo.get_accessibility(newgem.id) is False
    '''

    '''#keep this here for when we finish setting up reviews
    repo.update_reviews(newgem.id, ('insert review'))
    assert newgem.reviews is ('insert review')
    assert repo.get_reviews(newgem.id) is ('insert review')
    '''

    #delet
    repo.delete_hidden_gem(newgem.id)
    assert repo.get_hidden_gem_by_id(newgem.id) is None

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
    repo.clear_db()