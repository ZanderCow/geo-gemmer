from random import randint

from models.hidden_gem import HiddenGem, Reviews#, GemAcessibilty, GemImages

_gemr_repo = None


def get_gem_repository():
    global _gem_repo

    class GemRepository:
        """In memory database which is a simple dict of users"""

        def __init__(self) -> None:
            self._db: dict[int, HiddenGem] = {}

  
        def get_all_hidden_gems(self) -> dict[int, HiddenGem]:
            """
            Retrieve all hidden gems from the repository.

            Returns:
                A dictionary containing all hidden gems, where the keys are the gem IDs and the values are the HiddenGem objects.
            """
            return {**self._db}

     
        def get_hidden_gem_by_id(self, hidden_gem_id: int) -> HiddenGem | None:
            """
            Retrieves a hidden gem from the database based on its ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to retrieve.

            Returns:
                HiddenGem | None: The hidden gem object if found, None otherwise.
            """
            return self._db.get(hidden_gem_id)
        
        def get_gem_id_by_name(self, name: str) -> int | None:
                """
                Retrieves the ID of a gem based on its name.

                Args:
                    name (str): The name of the gem.

                Returns:
                    int | None: The ID of the gem if found, None otherwise.
                """
                for gem_id, gem in self._db.items():
                    if gem.name == name:
                        return gem_id
                return None

        def create_hidden_gem(self, name, latitude, longitude, gem_type, times_visited, user_created, website_link) -> HiddenGem:
            """
            Creates a new hidden gem instance and saves it in the in-memory database.

            Args:
                name (str): The name of the hidden gem.
                latitude (float): The latitude coordinate of the hidden gem's location.
                longitude (float): The longitude coordinate of the hidden gem's location.
                gem_type (str): The type or category of the hidden gem.
                times_visited (int): The number of times the hidden gem has been visited.
                user_created (str): The username of the user who created the hidden gem.
                website_link (str): The website link associated with the hidden gem.
  
            Returns:
                HiddenGem: The newly created hidden gem instance.

            """
            new_id = randint(0, 100_000)  
            hidden_gem = HiddenGem(name, new_id, latitude, longitude, gem_type, times_visited, user_created, website_link, False)
            self._db[new_id] = hidden_gem
            return hidden_gem
        

        def delete_hidden_gem(self, hidden_gem_id: int) -> None:
            """
            Deletes a hidden gem from the in-memory database.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to delete.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            if hidden_gem_id not in self._db:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            del self._db[hidden_gem_id]
    


        def get_name(self, hidden_gem_id: int) -> str:
            """
            Retrieve the name of a hidden gem based on its ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                str: The name of the hidden gem.
            """
            return self._db.get(hidden_gem_id).name
        

        def update_name(self, hidden_gem_id: int, name: str) -> HiddenGem:
            """
            Updates the name of a hidden gem with the given ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                name (str): The new name for the hidden gem.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.name = name
            return hidden_gem
        


        def get_cordinates(self, hidden_gem_id: int) -> tuple[float, float]:
            """
            Retrieves the coordinates (latitude and longitude) of a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                tuple[float, float]: A tuple containing the latitude and longitude of the hidden gem.
            """
            return self._db.get(hidden_gem_id).latitude, self._db.get(hidden_gem_id).longitude
    

        def update_cordinates(self, hidden_gem_id: int, latitude: float, longitude: float) -> HiddenGem:
            """
            Update the coordinates of a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                latitude (float): The new latitude value.
                longitude (float): The new longitude value.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the specified ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.latitude = latitude
            hidden_gem.longitude = longitude
            return hidden_gem
        
        def get_gem_type(self, hidden_gem_id: int) -> str:
            """
            Retrieves the gem type for a given hidden gem ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                str: The gem type associated with the hidden gem ID.
            """
            return self._db.get(hidden_gem_id).gem_type
        
        def update_gem_type(self, hidden_gem_id: int, gem_type: str) -> HiddenGem:
            """
            Update the gem type of a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                gem_type (str): The new gem type.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.gem_type = gem_type
            return hidden_gem
        
        def get_times_visited(self, hidden_gem_id: int) -> int:
            """
            Retrieves the number of times a hidden gem has been visited.

            Parameters:
            hidden_gem_id (int): The ID of the hidden gem.

            Returns:
            int: The number of times the hidden gem has been visited.
            """
            return self._db.get(hidden_gem_id).times_visited
        
        def update_times_visited(self, hidden_gem_id: int, times_visited: int) -> HiddenGem:
            """
            Update the number of times a hidden gem has been visited.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                times_visited (int): The new number of times visited.

            Returns:
                HiddenGem: The updated HiddenGem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.times_visited = times_visited
            return hidden_gem
        
        def get_user_created(self, hidden_gem_id: int) -> str:
            """
            Retrieves the username of the user who created the hidden gem with the given ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                str: The username of the user who created the hidden gem.
            """
            return self._db.get(hidden_gem_id).user_created
        
        def update_user_created(self, hidden_gem_id: int, user_created: str) -> HiddenGem:
            """
            Updates the 'user_created' attribute of a hidden gem with the given ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                user_created (str): The new value for the 'user_created' attribute.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.user_created = user_created
            return hidden_gem
        

        def get_website_link(self, hidden_gem_id: int) -> str:
            """
            Retrieves the website link for a hidden gem with the given ID.
            
            Args:
                hidden_gem_id (int): The ID of the hidden gem.
            
            Returns:
                str: The website link of the hidden gem.
            """
            return self._db.get(hidden_gem_id).website_link
        
        def update_website_link(self, hidden_gem_id: int, website_link: str) -> HiddenGem:
            """
            Updates the website link of a hidden gem with the given ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                website_link (str): The new website link to assign to the hidden gem.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            hidden_gem = self._db.get(hidden_gem_id)
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            hidden_gem.website_link = website_link
            return hidden_gem
        
        def get_accessibility(self, hidden_gem_id: int) -> list[bool]:
            """
            Retrieve the accessibility information for a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                list[bool]: A list of boolean values representing the accessibility of the hidden gem.
            """
            #dont test this one.
            pass
        
        def update_accessibility(self, hidden_gem_id: int, accessibility: list[bool]) -> HiddenGem:
            """
            Update the accessibility of a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem to update.
                accessibility (list[bool]): The new accessibility values for the hidden gem.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the specified ID is not found.
            """
            #dont test this one.
            pass
        
        def get_gem_images(self, hidden_gem_id: int) -> list[str]:
            """
            Retrieve the gem images associated with a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                list[str]: A list of gem images.

            """
            #dont test this one.
            pass
        
        def update_gem_images(self, hidden_gem_id: int, gem_images: list[str]) -> HiddenGem:
            """
            Update the gem images of a hidden gem.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.
                gem_images (list[str]): The list of gem images to update.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            #dont test this one.
            pass
        
      
        def get_reviews(self, hidden_gem_id: int) -> list[Reviews]:
            """
            Retrieves the reviews for a hidden gem with the specified ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.

            Returns:
                list[Reviews]: A list of reviews for the hidden gem.
            """
            #dont test this one
            pass
        
        def update_reviews(self, hidden_gem_id: int, reviews: list[Reviews]) -> HiddenGem:
            """
            Updates the reviews of a hidden gem with the given ID.

            Args:
                hidden_gem_id (int): The ID of the hidden gem.
                reviews (list[Reviews]): The list of reviews to update.

            Returns:
                HiddenGem: The updated hidden gem object.

            Raises:
                ValueError: If the hidden gem with the given ID is not found.
            """
            #dont test this one.
            pass
    


        def clear_db(self) -> None:
            """Clears all movies out of the database, only to be used in tests"""
            self._db = {}

    # Singleton to be used in other modules
    global _gemr_repo
    if _gemr_repo is None:
        _gemr_repo = GemRepository()

    return _gemr_repo
