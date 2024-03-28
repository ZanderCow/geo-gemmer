import pytest
from repositories.user_repository import get_user_repository

def test_get_user_id_by_username():
    repository = get_user_repository()
    repository.create_user("john_doe", "password")
    repository.create_user("jane_smith", "password")
    
    assert repository.get_user_id_by_username("john_doe") == 0
    assert repository.get_user_id_by_username("jane_smith") == 1
    assert repository.get_user_id_by_username("nonexistent_user") is None

def test_get_all_users():
    repository = get_user_repository()
    repository.create_user("john_doe", "password")
    repository.create_user("jane_smith", "password")
    
    users = repository.get_all_users()
    assert len(users) == 2
    assert users[0].username == "john_doe"
    assert users[1].username == "jane_smith"

def test_get_user_by_id():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_user_by_id(0) == user
    assert repository.get_user_by_id(1) is None

def test_create_user():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert user.username == "john_doe"
    assert user.first_name == "John"
    assert user.last_name == "Doe"
    assert user.password == "password"
    assert user.profile_picture == "https://www.google.com"
    assert user.gems_explored == 0
    assert user.reviews_made == 0

def test_delete_user():
    repository = get_user_repository()
    repository.create_user("john_doe", "password")
    repository.create_user("jane_smith", "password")
    
    repository.delete_user(0)
    assert repository.get_user_by_id(0) is None
    assert repository.get_user_by_id(1) is not None

def test_get_username():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_username(0) == "john_doe"
    assert repository.get_username(1) is None

def test_update_username():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_username(0, "john_smith")
    assert updated_user.username == "john_smith"
    assert repository.get_username(0) == "john_smith"

def test_get_first_name():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_first_name(0) == "John"
    assert repository.get_first_name(1) is None

def test_update_first_name():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_first_name(0, "Johnathan")
    assert updated_user.first_name == "Johnathan"
    assert repository.get_first_name(0) == "Johnathan"

def test_get_last_name():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_last_name(0) == "Doe"
    assert repository.get_last_name(1) is None

def test_update_last_name():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_last_name(0, "Smith")
    assert updated_user.last_name == "Smith"
    assert repository.get_last_name(0) == "Smith"

def test_get_password():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_password(0) == "password"
    assert repository.get_password(1) is None

def test_update_password():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_password(0, "new_password")
    assert updated_user.password == "new_password"
    assert repository.get_password(0) == "new_password"

def test_get_num_gems_explored():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_num_gems_explored(0) == 0
    assert repository.get_num_gems_explored(1) is None

def test_update_num_gems_explored():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_num_gems_explored(0, 10)
    assert updated_user.gems_explored == 10
    assert repository.get_num_gems_explored(0) == 10

def test_get_num_reviews_made():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    assert repository.get_num_reviews_made(0) == 0
    assert repository.get_num_reviews_made(1) is None

def test_update_num_reviews_made():
    repository = get_user_repository()
    user = repository.create_user("john_doe", "password")
    
    updated_user = repository.update_num_reviews_made(0, 5)
    assert updated_user.reviews_made == 5
    assert repository.get_num_reviews_made(0) == 5