from random import randint

from ..models.user import User, UserGemVisited, GemSaved, ReviewsLeft

_user_repo = None


def get_user_repository():
    global _user_repo

    class UserRepository:
        """In memory database which is a simple dict of users"""

        def __init__(self) -> None:
            self._db: dict[int, User] = {}

        def get_all_users(self) -> dict[int, User]:
            """Simply return all users from the in-memory database"""
            return {**self._db}  # Use the splat operator to make a clone of the dict

        def get_user_by_id(self, user_id: int) -> User | None:
            """Get a single user by its ID or None if it does not exist"""
            return self._db.get(user_id)

        
        def create_user(self, user_name: str, password: str) -> User:
            """Create a new user and returns it (assumes user is created with no gems visited, saved, or reviews left)"""

            new_id = randint(0, 100_000)  # Sufficiently unique ID for our purposes
            user = User(new_id)
            # Save the instance in our in-memory database
            self._db[new_id] = User(user_name, "John", "Doe", password, "https://www.google.com", 0, 0, 0, 0, [], [], [])
            # Return the user instance
            return User
        
        def get_username(self, user_id: int) -> str:
            """Get a username by its ID or None if it does not exist"""
            return self._db.get(user_id).username
        
        def update_username(self, user_id: int, user_name: str) -> User:
            """Update a users username and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.username = user_name
            return user
        
        def get_first_name(self, user_id: int) -> str:
            """Get a users first name by its ID or None if it does not exist"""
            return self._db.get(user_id).first_name
        
        def update_first_name(self, user_id: int, first_name: str) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.first_name = first_name
            return user
        
        def get_last_name(self, user_id: int) -> str:
            """Get a users last name by its ID or None if it does not exist"""
            return self._db.get(user_id).last_name
        
        def update_last_name(self, user_id: int, last_name: str) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.last_name = last_name
            return user
        
        def get_password(self, user_id: int) -> str:
            """Get a users password by its ID or None if it does not exist"""
            return self._db.get(user_id).password
        
        def update_password(self, user_id: int, password: str) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.password = password
            return user
        
        def get_profile_picture(self, user_id: int) -> str:
            """Get a users profile picture by its ID or None if it does not exist"""
            return self._db.get(user_id).profile_picture
        
        def update_profile_picture(self, user_id: int, profile_picture: str) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.profile_picture = profile_picture
            return user
        
        def get_gems_explored(self, user_id: int) -> int:
            """Get a users gems explored count by its ID or None if it does not exist"""
            return self._db.get(user_id).gems_explored
        
        def update_gems_explored(self, user_id: int, gems_explored: int) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.gems_explored = gems_explored
            return user
        
        def get_reviews_made(self, user_id: int) -> int:
            """Get a users reviews made count by its ID or None if it does not exist"""
            return self._db.get(user_id).reviews_made
        
        def update_reviews_made(self, user_id: int, reviews_made: int) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.reviews_made = reviews_made
            return user
        
        def get_gems_created(self, user_id: int) -> int:
            """Get a users gems created count by its ID or None if it does not exist"""
            return self._db.get(user_id).gems_created
    
        def update_gems_created(self, user_id: int, gems_created: int) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.gems_created = gems_created
            return user
        
        def get_gems_saved_count(self, user_id: int) -> int:
            """Get a users gems saved count by its ID or None if it does not exist"""
            return self._db.get(user_id).gems_saved_count
        
        def update_gems_saved_count(self, user_id: int, gems_saved_count: int) -> User:
            """Update a user and return it"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Update the user, which is the same object that is in the dict, so the changes stick
            user.gems_saved_count = gems_saved_count
            return user
        
        
        
        def get_gems_visited(self, user_id: int) -> list[UserGemVisited]:
            """Get a users gems visited by its ID or None if it does not exist"""
            return self._db.get(user_id).gems_visited
        
        def add_gem_visited(self, user_id: int, gem_name: str, gem_type: str, date_visited: str) -> User:
            """Add a hidden gem to a user and return the user"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Add the gem to the user
            user.gems_visited.append(UserGemVisited(gem_name, gem_type, date_visited))
            return user
        
        def get_gems_saved(self, user_id: int) -> list[GemSaved]:
            """Get a users gems saved by its ID or None if it does not exist"""
            return self._db.get(user_id).gems_saved
        
        def add_user_gem_saved(self, user_id: int, gem_name: str, gem_type: str, gem_location: str) -> User:
            """Add a hidden gem to a user and return the user"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Add the gem to the user
            user.gems_saved.append(GemSaved(gem_name, gem_type, gem_location))
            return user
        

        def get_reviews_left(self, user_id: int) -> list[ReviewsLeft]:
            """Get a users reviews left by its ID or None if it does not exist"""
            return self._db.get(user_id).left_reviews
        
        def add_review_left(self, user_id: int, rating: int, review: str) -> User:

            """Add a review to a user and return the user"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Add the review to the user
            user.left_reviews.append(ReviewsLeft(rating, review))
            return user


        
        def add_gem_visited(self, user_id: int, gem_name: str, gem_type: str, date_visited: str) -> User:
            """Add a hidden gem to a user and return the user"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Add the gem to the user
            user.gems_visited.append(UserGemVisited(gem_name, gem_type, date_visited))
            return user
        
        def add_user_gem_saved(self, user_id: int, gem_name: str, gem_type: str, gem_location: str) -> User:
            """Add a hidden gem to a user and return the user"""
            # Get a reference to the user in the dict
            user = self._db.get(user_id)
            # Complain if we did not find the user
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            # Add the gem to the user
            user.gems_saved.append(GemSaved(gem_name, gem_type, gem_location))
            return user
        

      

        def clear_db(self) -> None:
            """Clears all movies out of the database, only to be used in tests"""
            self._db = {}

    # Singleton to be used in other modules
    if _user_repo is None:
        _user_repo = UserRepository()

    return _user_repo
