import random
from faker import Faker

# Create a Faker instance
fake = Faker()
# Define possible gem types
gem_types = ["Historical", "Natural", "Cultural", "Architectural", "Scenic"]

# Function to create a random gem
def create_random_gem():
    name = fake.company()  # Using company names as gem names
    gem_type = random.choice(gem_types)
    longitude = round(random.uniform(-180, 180), 6)
    latitude = round(random.uniform(-90, 90), 6)
    user_created = random.choice([True, False])
    # Randomly assign images or none
    image1 = fake.image_url() if random.choice([True, False]) else None
    image2 = fake.image_url() if random.choice([True, False]) else None
    image3 = fake.image_url() if random.choice([True, False]) else None
    return {
        "name": name,
        "gem_type": gem_type,
        "longitude": longitude,
        "latitude": latitude,
        "user_created": user_created,
        "image1": image1,
        "image2": image2,
        "image3": image3
    }

# Generate 30 random gems
random_gems = [create_random_gem() for _ in range(30)]

for gem in random_gems:
    print(gem)
    print()
