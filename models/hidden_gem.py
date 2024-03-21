class HiddenGem: 
    '''
    Represents a hidden gem location.

    Attributes:
        name (str): The name of the hidden gem.
        gem_id (int): The unique identifier of the hidden gem.
        latitude (float): The latitude coordinate of the hidden gem.
        longitude (float): The longitude coordinate of the hidden gem.
        gem_type (str): The type or category of the hidden gem.
        times_visited (int): The number of times the hidden gem has been visited.
        user_created (boolean): Whether the hidden gem was created by a user.
        website_link (str): The URL of the hidden gem's website.
    '''
    def __init__(self, name, latitude, longitude, gem_type, times_visited, user_created, website_link, accessibility, gem_images, reviews):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.gem_type = gem_type
        self.times_visited = times_visited
        self.user_created = user_created
        self.website_link = website_link




    