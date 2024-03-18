from random import randint

from ..models.hidden_gem import HiddenGem, GemAcessibilty, GemImages, Reviews

_gemr_repo = None


def get_user_repository():
    global _gem_repo

    class GemRepository:
        """In memory database which is a simple dict of users"""

        def __init__(self) -> None:
            self._db: dict[int, HiddenGem] = {}

        def get_all_hidden_gems(self) -> dict[int, HiddenGem]:
            """Simply return all users from the in-memory database"""
            return {**self._db}  # Use the splat operator to make a clone of the dict

        def get_hidden_gem_by_id(self, hidden_gem_id: int) -> HiddenGem | None:
            """Get a single hidden gem by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id)

        def create_hidden_gem(self, name: str, latitude: float, longitude: float, gem_type: str, times_visited: int, user_created: str, website_link: str, accessibility: list[bool], gem_images: list[str], reviews: list[Reviews]) -> HiddenGem:
            """Create a new hidden gem and returns it (assumes hidden gem is created with no reviews)"""

            new_id = randint(0, 100_000)  # Sufficiently unique ID for our purposes
            hidden_gem = HiddenGem(name, new_id, latitude, longitude, gem_type, times_visited, user_created, website_link, accessibility, gem_images, reviews)
            # Save the instance in our in-memory database
            self._db[new_id] = hidden_gem
            # Return the hidden gem instance
            return hidden_gem
    

        def get_name(self, hidden_gem_id: int) -> str:
            """Get a hidden gem's name by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).name
        

        def update_name(self, hidden_gem_id: int, name: str) -> HiddenGem:
            """Update a hidden gem's name and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.name = name
            return hidden_gem
        

        def get_cordinates(self, hidden_gem_id: int) -> tuple[float, float]:
            """Get a hidden gem's cordinates by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).latitude, self._db.get(hidden_gem_id).longitude
        

        def update_cordinates(self, hidden_gem_id: int, latitude: float, longitude: float) -> HiddenGem:
            """Update a hidden gem's cordinates and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.latitude = latitude
            hidden_gem.longitude = longitude
            return hidden_gem
        
        def get_gem_type(self, hidden_gem_id: int) -> str:
            """Get a hidden gem's type by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).gem_type
        
        def update_gem_type(self, hidden_gem_id: int, gem_type: str) -> HiddenGem:
            """Update a hidden gem's type and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.gem_type = gem_type
            return hidden_gem
        
        def get_times_visited(self, hidden_gem_id: int) -> int:
            """Get a hidden gem's times visited by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).times_visited
        
        def update_times_visited(self, hidden_gem_id: int, times_visited: int) -> HiddenGem:
            """Update a hidden gem's times visited and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.times_visited = times_visited
            return hidden_gem
        
        def get_user_created(self, hidden_gem_id: int) -> str:
            """Get a hidden gem's creator by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).user_created
        
        def update_user_created(self, hidden_gem_id: int, user_created: str) -> HiddenGem:
            """Update a hidden gem's creator and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.user_created = user_created
            return hidden_gem
        

        def get_website_link(self, hidden_gem_id: int) -> str:
            """Get a hidden gem's website link by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).website_link
        
        def update_website_link(self, hidden_gem_id: int, website_link: str) -> HiddenGem:
            """Update a hidden gem's website link and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.website_link = website_link
            return hidden_gem
        
        def get_accessibility(self, hidden_gem_id: int) -> list[bool]:
            """Get a hidden gem's accessibility by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).accessibility
        
        def update_accessibility(self, hidden_gem_id: int, accessibility: list[bool]) -> HiddenGem:
            """Update a hidden gem's accessibility and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.accessibility = accessibility
            return hidden_gem
        
        def get_gem_images(self, hidden_gem_id: int) -> list[str]:
            """Get a hidden gem's images by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).gem_images
        
        def update_gem_images(self, hidden_gem_id: int, gem_images: list[str]) -> HiddenGem:
            """Update a hidden gem's images and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.gem_images = gem_images
            return hidden_gem
        
        def get_reviews(self, hidden_gem_id: int) -> list[Reviews]:
            """Get a hidden gem's reviews by its ID or None if it does not exist"""
            return self._db.get(hidden_gem_id).reviews
        
        def update_reviews(self, hidden_gem_id: int, reviews: list[Reviews]) -> HiddenGem:
            """Update a hidden gem's reviews and return it"""
            # Get a reference to the hidden gem in the dict
            hidden_gem = self._db.get(hidden_gem_id)
            # Complain if we did not find the hidden gem
            if not hidden_gem:
                raise ValueError(f'hidden gem with id {hidden_gem_id} not found')
            # Update the hidden gem, which is the same object that is in the dict, so the changes stick
            hidden_gem.reviews = reviews
            return hidden_gem
    


        def clear_db(self) -> None:
            """Clears all movies out of the database, only to be used in tests"""
            self._db = {}

    # Singleton to be used in other modules
    if _user_repo is None:
        _user_repo = GemRepository()

    return _user_repo
