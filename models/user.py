class User:
    """A user holds personal information and interactions with gems"""
    username = "None"
    id = 1
    first_name = "None"
    last_name = "None"
    password = "None"
    profile_picture = "None"
    gems_explored = 0
    reviews_made = 0
    gems_created = 0
    gems_saved_count = 0 
    def __init__(self, username, new_id, first_name, last_name, password, profile_picture, gems_explored, reviews_made, gems_created, gems_saved_count):
        """
        Initialize a User object with the provided information 

        Args:
            username (str): The username of the user.
            id (int): The ID of the user
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
        self.username = username
        self.id = new_id
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.profile_picture = profile_picture
        self.gems_explored = gems_explored
        self.reviews_made = reviews_made
        self.gems_created = gems_created
        self.gems_saved_count = gems_saved_count        
