class User:
    """A user holds personal information and interactions with gems"""
   
    def __init__(self, username: str, first_name: str, last_name: str, password: str, profile_picture: str, gems_explored: int, reviews_made: int, gems_created: int, gems_saved_count: int) -> None:
        """
        Initialize a User object with the provided information 

        Args:
            username (str): The username of the user.
            first_name (str): The first name of the user.
            last_name (str): The last name of the user.
            password (str): The password of the user.
            profile_picture (str): The URL of the user's profile picture.
            gems_explored (int): The number of gems explored by the user.
            reviews_made (int): The number of reviews made by the user.
            gems_created (int): The number of gems created by the user.
            gems_saved_count (int): The number of gems saved by the user.

        Returns:
            None
        """
        
