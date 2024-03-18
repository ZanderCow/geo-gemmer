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
        user_created (str): The username of the user who created the hidden gem.
        website_link (str): The website link associated with the hidden gem.
        accessibility (list): A list of accessibility features for the hidden gem.
        gem_images (list): A list of images associated with the hidden gem.
        reviews (list): A list of reviews for the hidden gem.
    '''
    def __init__(self, name, latitude, longitude, gem_type, times_visited, user_created, website_link, accessibility, gem_images, reviews):
        self.name = name
        self.latitude = latitude
        self.longitude = longitude
        self.gem_type = gem_type
        self.times_visited = times_visited
        self.user_created = user_created
        self.website_link = website_link
        self.accessibility = accessibility
        self.gem_images = gem_images
        self.reviews = reviews



class GemAcessibilty: 
    """
    A class to represent the accessibility of a gem.

    Attributes:
        elderly_friendly (bool): Indicates if the gem is elderly-friendly.
        wheelchair_friendly (bool): Indicates if the gem is wheelchair-friendly.
        austic_friendly (bool): Indicates if the gem is austic-friendly.
        blind_friendly (bool): Indicates if the gem is blind-friendly.
        deaf_friendly (bool): Indicates if the gem is deaf-friendly.
        allergen_friendly (bool): Indicates if the gem is allergen-friendly.
        sensory_friendly (bool): Indicates if the gem is sensory-friendly.
        kids_friendly (bool): Indicates if the gem is kids-friendly.
        pet_friendly (bool): Indicates if the gem is pet-friendly.
    """
    def __init__(self, elderly_friendly, wheelchair_friendly, austic_friendly, blind_friendly, deaf_friendly, allergen_friendly, sensory_friendly, kids_friendly, pet_friendly):
        self.elderly_friendly = elderly_friendly
        self.wheelchair_friendly = wheelchair_friendly
        self.austic_friendly = austic_friendly
        self.blind_friendly = blind_friendly
        self.deaf_friendly = deaf_friendly
        self.allergen_friendly = allergen_friendly
        self.sensory_friendly = sensory_friendly
        self.kids_friendly = kids_friendly
        self.pet_friendly = pet_friendly


class GemImages: 
    '''
    A class representing a set of gem images.
    
    Attributes:
        image_1 (str): The path or URL of the first gem image.
        image_2 (str): The path or URL of the second gem image.
        image_3 (str): The path or URL of the third gem image.
    '''
    def __init__(self, image_1, image_2, image_3):
        self.image_1 = image_1
        self.image_2 = image_2
        self.image_3 = image_3


class GemReview: 
    def __init__(self, username, rating, review):
        self.username = username
        self.rating = rating
        self.review = review

    