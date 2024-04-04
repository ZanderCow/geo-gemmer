create DATABASE geogemmer;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";


CREATE TABLE IF NOT EXISTS user (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255),
    password VARCHAR(255),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    profile_picture VARCHAR(255),
    gems_explored_count INT,
    reviews_made_count INT,
    gems_created_count INT,
    gems_saved_count INT
);

CREATE TABLE IF NOT EXISTS review (
    review_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user(user_id) ON DELETE CASCADE,
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    rating CHAR(1),
    review TEXT
);

CREATE TABLE IF NOT EXISTS accessibility (
    accessibility_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    wheelchair_accessible BOOLEAN,
    service_animal_friendly BOOLEAN,
    multilingual_support BOOLEAN,
    braille_signage BOOLEAN,
    hearing_assistance BOOLEAN,
    large_print_materials BOOLEAN,
    accessible_restrooms BOOLEAN
);

CREATE TABLE IF NOT EXISTS hidden_gem (
    gem_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    latitude FLOAT NOT NULL,
    longitude FLOAT NOT NULL,
    gem_type VARCHAR(50),
    times_visited INT,
    user_created BOOLEAN,
    website_link VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS gems_visited (
    gem_visited_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES user(user_id) ON DELETE CASCADE,
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    date_visited date NOT NULL
);

CREATE TABLE IF NOT EXISTS image_group (
    image_group_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    image_1 VARCHAR(255),
    image_2 VARCHAR(255),
    image_3 VARCHAR(255)
);



