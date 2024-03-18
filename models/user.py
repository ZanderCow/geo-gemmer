class User:
    """A user holds personal information and interactions with gems"""
    def __init__(self, username: str, first_name: str, last_name: str, password: str, profile_picture: str, gems_explored: int, reviews_made: int, gems_created: int, gems_saved_count: int) -> None:
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.profile_picture = profile_picture
        self.gems_explored = gems_explored
        self.reviews_made = reviews_made
        self.gems_created = gems_created
        self.gems_saved_count = gems_saved_count
        self.gems_visited = []
        self.gems_saved = []
        self.left_reviews = []

class UserGemVisited:
    """Represents a gem that a user has visited"""
    def __init__(self, gem_name: str, gem_type: str, date_visited: str) -> None:
        self.gem_name = gem_name
        self.gem_type = gem_type
        self.date_visited = date_visited


class GemSaved:
    """Represents a gem that a user has saved"""
    def __init__(self, gem_name: str, gem_type: str, gem_location: str) -> None:
        self.gem_name = gem_name
        self.gem_type = gem_type
        self.gem_location = gem_location


class ReviewsLeft:
    """Represents a review made by a user"""
    def __init__(self, rating: int, review: str) -> None:
        self.rating = rating
        self.review = review