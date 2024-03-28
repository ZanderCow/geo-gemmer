import pytest
from repositories.user_repository import get_user_repository

@pytest.fixture
def user_repo():
    """Fixture to provide a user repository instance"""
    return get_user_repository()

def test_get_user_id_by_username(user_repo):
    # Add test user
    user_repo.create_user("test_user", "password")
    
    # Test for existing username
    assert user_repo.get_user_id_by_username("test_user") is not None
    
    # Test for non-existing username
    assert user_repo.get_user_id_by_username("non_existing_user") is None

    #reset db
    user_repo.clear_db()

def test_get_all_users(user_repo):
    # Add test users
    user_repo.create_user("user1", "password1")
    user_repo.create_user("user2", "password2")
    
    # Test if all users are retrieved
    all_users = user_repo.get_all_users()
    assert len(all_users) == 2

    #reset db
    user_repo.clear_db()

def test_get_user_by_id(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test retrieving user by ID
    retrieved_user = user_repo.get_user_by_id(user.id)
    assert retrieved_user is not None
    assert retrieved_user.username == "test_user"

    #reset db
    user_repo.clear_db()

def test_create_user(user_repo):
    # Create a new user
    new_user = user_repo.create_user("new_user", "password")
    
    # Test if user is created
    assert new_user is not None
    assert new_user.username == "new_user"

    #reset db
    user_repo.clear_db()

def test_delete_user(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Delete user
    user_repo.delete_user(user.id)
    
    # Test if user is deleted
    assert user_repo.get_user_by_id(user.id) is None

def test_get_username(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting username by ID
    assert user_repo.get_username(user.id) == "test_user"

    #reset db
    user_repo.clear_db()

def test_update_username(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update username
    updated_user = user_repo.update_username(user.id, "new_username")
    
    # Test if username is updated
    assert updated_user.username == "new_username"

    #reset db
    user_repo.clear_db()

def test_get_first_name(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting first name by ID
    assert user_repo.get_first_name(user.id) == "John"

    #reset db
    user_repo.clear_db()

def test_update_first_name(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update first name
    updated_user = user_repo.update_first_name(user.id, "Jane")
    
    # Test if first name is updated
    assert updated_user.first_name == "Jane"

    #reset db
    user_repo.clear_db()

def test_get_last_name(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting last name by ID
    assert user_repo.get_last_name(user.id) == "Doe"

    #reset db
    user_repo.clear_db()

def test_update_last_name(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update last name
    updated_user = user_repo.update_last_name(user.id, "Smith")
    
    # Test if last name is updated
    assert updated_user.last_name == "Smith"

    #reset db
    user_repo.clear_db()

def test_get_password(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting password by ID
    assert user_repo.get_password(user.id) == "password"

    #reset db
    user_repo.clear_db()

def test_update_password(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update password
    updated_user = user_repo.update_password(user.id, "new_password")
    
    # Test if password is updated
    assert updated_user.password == "new_password"

    #reset db
    user_repo.clear_db()

def test_get_num_gems_explored(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting number of gems explored by ID
    assert user_repo.get_num_gems_explored(user.id) == 0

    #reset db
    user_repo.clear_db()

def test_update_num_gems_explored(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update number of gems explored
    updated_user = user_repo.update_num_gems_explored(user.id, 5)
    
    # Test if number of gems explored is updated
    assert updated_user.gems_explored == 5

    #reset db
    user_repo.clear_db()

def test_get_num_reviews_made(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting number of reviews made by ID
    assert user_repo.get_num_reviews_made(user.id) == 0

    #reset db
    user_repo.clear_db()

def test_update_num_reviews_made(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update number of reviews made
    updated_user = user_repo.update_num_reviews_made(user.id, 3)
    
    # Test if number of reviews made is updated
    assert updated_user.reviews_made == 3

    #reset db
    user_repo.clear_db()

def test_get_num_gems_created(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting number of gems created by ID
    assert user_repo.get_num_gems_created(user.id) == 0

    #reset db
    user_repo.clear_db()

def test_update_num_gems_created(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update number of gems created
    updated_user = user_repo.update_num_gems_created(user.id, 2)
    
    # Test if number of gems created is updated
    assert updated_user.gems_created == 2

    #reset db
    user_repo.clear_db()

def test_get_num_gems_saved(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Test getting number of gems saved by ID
    assert user_repo.get_num_gems_saved(user.id) == 0

    #reset db
    user_repo.clear_db()

def test_update_num_gems_saved(user_repo):
    # Add test user
    user = user_repo.create_user("test_user", "password")
    
    # Update number of gems saved
    updated_user = user_repo.update_num_gems_saved(user.id, 4)
    
    # Test if number of gems saved is updated
    assert updated_user.gems_saved_count == 4

    #reset db
    user_repo.clear_db()