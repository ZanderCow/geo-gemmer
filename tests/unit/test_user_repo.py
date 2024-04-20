"""
write test code
"""
import pytest
from repositories import user_repository as repo
from repositories import gem_repository as gem_repo
from tests.unit.test_gem_respository import _reset_database


def test_making_user():
    _reset_database()
    newuser = repo.create_new_user("MyNameIs","FJEI@QOFEUWQ*O'FJEIWOQ")
    print(repo.get_user_settings_details(newuser))
    
    user = repo.get_user_by_id(newuser)
    assert isinstance(user, dict)
    #make sure the name is right at least
    assert user['username'] == "MyNameIs"
    