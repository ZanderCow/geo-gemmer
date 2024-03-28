from random import randint

from models.user import User

_user_repo = None


def get_user_repository():
    global _user_repo

    class UserRepository:
        """In memory database which is a simple dict of users"""

        def get_user_id_by_username(self, username: str) -> int | None:
            """
            Retrieve the ID of a user by their username.

            Args:
                username (str): The username of the user.

            Returns:
                int | None: The ID of the user if found, None otherwise.
            """
            for user_id, user in self._db.items():
                if user.username == username:
                    return user_id
            return None

        def __init__(self) -> None:
            self._db: dict[int, User] = {}

        
        def get_all_users(self) -> dict[int, User]:
            """
            Retrieve all users from the repository.

            Returns:
                dict[int, User]: A dictionary containing all users in the repository.
            """
            return {**self._db}  # Use the splat operator to make a clone of the dict

        def get_user_by_id(self, user_id: int) -> User | None:
            """
            Retrieve a user from the database by their ID.

            Args:
                user_id (int): The ID of the user to retrieve.

            Returns:
                User | None: The user object if found, None otherwise.
            """
            return self._db.get(user_id)

    
        def create_user(self, user_name: str, password: str) -> User:
            """
            Create a new user with the given username and password.

            Args:
                user_name (str): The username of the new user.
                password (str): The password of the new user.

            Returns:
                User: The newly created User instance.
            """

            new_id = randint(0, 100_000)  # Sufficiently unique ID for our purposes
            user = User(user_name, new_id, "John", "Doe", password, "https://www.google.com", 0, 0, 0, 0)
            # assumes that the user is new so they wont have any gems visited, saved, or reviews left
            self._db[new_id] = user
            
            return user
        

        def delete_user(self, user_id: int) -> None:
            """
            Delete a user from the repository by their ID.

            Args:
                user_id (int): The ID of the user to delete.

            Returns:
                None
            """
            self._db.pop(user_id, None)


        
        def get_username(self, user_id: int) -> str:
            """
            Retrieve the username associated with the given user ID.
            
            Args:
                user_id (int): The ID of the user.
            
            Returns:
                str: The username associated with the user ID.
            """
            return self._db.get(user_id).username
        
        def update_username(self, user_id: int, user_name: str) -> User:
            """
            Update the username of a user with the given user_id.

            Args:
                user_id (int): The ID of the user to update.
                user_name (str): The new username to set.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given user_id is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.username = user_name
            return user
        
        def get_first_name(self, user_id: int) -> str:
            """
            Retrieve the first name of a user based on their user ID.

            Args:
                user_id (int): The ID of the user.

            Returns:
                str: The first name of the user.
            """
            return self._db.get(user_id).first_name
        
        def update_first_name(self, user_id: int, first_name: str) -> User:
            """
            Update the first name of a user with the given user_id.

            Args:
                user_id (int): The ID of the user to update.
                first_name (str): The new first name for the user.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given user_id is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.first_name = first_name
            return user
        
        def get_last_name(self, user_id: int) -> str:
            """
            Retrieve the last name of a user based on their user ID.
            
            Args:
                user_id (int): The ID of the user.
            
            Returns:
                str: The last name of the user.
            """
            return self._db.get(user_id).last_name
        
        def update_last_name(self, user_id: int, last_name: str) -> User:
            """
            Update the last name of a user with the given user ID.

            Args:
                user_id (int): The ID of the user to update.
                last_name (str): The new last name for the user.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given ID is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.last_name = last_name
            return user
        
        def get_password(self, user_id: int) -> str:
            """
            Retrieves the password for the specified user ID.
            
            Args:
                user_id (int): The ID of the user.
            
            Returns:
                str: The password associated with the user ID.
            """
            return self._db.get(user_id).password
        
        def update_password(self, user_id: int, password: str) -> User:
            """
            Update the password of a user with the given user_id.

            Args:
                user_id (int): The ID of the user.
                password (str): The new password for the user.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given user_id is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.password = password
            return user
        
        def get_profile_picture(self, user_id: int) -> str:
            """
            Retrieve the profile picture of a user.

            Args:
                user_id (int): The ID of the user.

            Returns:
                str: The URL of the user's profile picture.
            """
            #Dont test this one, we need to connect to a cloud database to actually use this because we need to store the image
            pass
        
        def update_profile_picture(self, user_id: int, profile_picture: str) -> User:
            """
            Update the profile picture of a user.

            Args:
                user_id (int): The ID of the user.
                profile_picture (str): The URL or file path of the new profile picture.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given ID is not found.
            """
            #Dont test this one, we need to connect to a cloud database to actually use this because we need to store the image
            pass
            
        
        def get_num_gems_explored(self, user_id: int) -> int:
            """
            Retrieves the number of gems explored by the user with the given user_id.
            
            Parameters:
            - user_id (int): The ID of the user.
            
            Returns:
            - int: The number of gems explored by the user.
            """
            return self._db.get(user_id).gems_explored
        
        def update_num_gems_explored(self, user_id: int, gems_explored: int) -> User:
            """
            Update the number of gems explored for a user.

            Args:
                user_id (int): The ID of the user.
                gems_explored (int): The new number of gems explored.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given ID is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.gems_explored = gems_explored
            return user
        
        def get_num_reviews_made(self, user_id: int) -> int:
            """
            Retrieves the number of reviews made by a user.

            Args:
                user_id (int): The ID of the user.

            Returns:
                int: The number of reviews made by the user.
            """
            return self._db.get(user_id).reviews_made
        
        def update_num_reviews_made(self, user_id: int, reviews_made: int) -> User:
            """
            Update the number of reviews made by a user.

            Args:
                user_id (int): The ID of the user.
                reviews_made (int): The new number of reviews made by the user.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given ID is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.reviews_made = reviews_made
            return user
        
        def get_num_gems_created(self, user_id: int) -> int:
            """
            Retrieves the number of gems created by a user.

            Args:
                user_id (int): The ID of the user.

            Returns:
                int: The number of gems created by the user.
            """
            return self._db.get(user_id).gems_created
    
        def update_num_gems_created(self, user_id: int, gems_created: int) -> User:
            """
            Update the number of gems created by a user.

            Args:
                user_id (int): The ID of the user.
                gems_created (int): The new number of gems created.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the specified ID is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.gems_created = gems_created
            return user
        
        def get_num_gems_saved(self, user_id: int) -> int:
            """
            Retrieves the number of gems saved by a user.

            Args:
                user_id (int): The ID of the user.

            Returns:
                int: The number of gems saved by the user.
            """
            return self._db.get(user_id).gems_saved_count
        
        def update_num_gems_saved(self, user_id: int, gems_saved_count: int) -> User:
            """
            Update the number of gems saved for a user.

            Args:
                user_id (int): The ID of the user.
                gems_saved_count (int): The new number of gems saved for the user.

            Returns:
                User: The updated User object.

            Raises:
                ValueError: If the user with the given ID is not found.
            """
            user = self._db.get(user_id)
            if not user:
                raise ValueError(f'user with id {user_id} not found')
            user.gems_saved_count = gems_saved_count
            return user
        
        
        
        def get_gems_explored(self, user_id: int):
            '''
            Retrieves the list of gems recently visited by a user.
            '''
            #dont test this one.
            pass
        
        def add_gem_explored(self, user_id: int, gem_name: str, gem_type: str, date_visited: str) -> User:
            '''
            Adds a visited gem to the user's list of visited gems.
            '''
            #dont test this one
            pass
        
        def get_gems_saved(self, user_id: int):
            '''
            Retrieves the list of gems saved by a user.
            '''
            #dont test this one
            pass
            
        
        def add_user_gem_saved(self, user_id: int, gem_name: str, gem_type: str, gem_location: str) -> User:
            '''
            Adds a hidden gem to a user's list of saved gems.
            '''
            #dont test this one
            pass
        

        #def get_reviews_left(self, user_id: int) -> list[ReviewsLeft]:
        #    """
        #    Retrieves the list of reviews left by a user.
        #    """
        #    #dont test this one
        #    pass

        
        def add_gem_visited(self, user_id: int, gem_name: str, gem_type: str, date_visited: str) -> User:
            """
            Adds a visited gem to the user's list of visited gems.

            Args:
                user_id (int): The ID of the user.
                gem_name (str): The name of the visited gem.
                gem_type (str): The type of the visited gem.
                date_visited (str): The date when the gem was visited.

            Returns:
                User: The updated User object with the visited gem added.
            
            Raises:
                ValueError: If the user with the given ID is not found.
            """
            #dont test this one
            pass
        
        def clear_db(self) -> None:
            """Clears all movies out of the database, only to be used in tests"""
            self._db = {}

    # Singleton to be used in other modules
    if _user_repo is None:
        _user_repo = UserRepository()

    return _user_repo
