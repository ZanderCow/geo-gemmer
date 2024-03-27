"""
write test code
"""
import pytest
from repositories import gem_repository
from models.hidden_gem import HiddenGem


def test_making_gem():
    newgem = HiddenGem("nameo", 1234, 35.227085, 80.843124, "big place", 0, False, "https://www.youtube.com/watch?v=dQw4w9WgXcQ", False)
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

    repo.delete_hidden_gem(new_id)
    assert repo.get_hidden_gem_by_id(new_id) is None
