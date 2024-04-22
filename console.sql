create DATABASE geogemmer;
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS postgis;
CREATE EXTENSION IF NOT EXISTS pg_trgm;


CREATE TABLE IF NOT EXISTS geo_user (
    user_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username VARCHAR(255),
    password BYTEA,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    profile_picture VARCHAR(255),
    gems_explored INT,
    reviews_made INT,
    gems_created INT,
    gems_saved INT
);

CREATE TABLE IF NOT EXISTS hidden_gem (
    gem_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(128) NOT NULL,
    gem_type VARCHAR(50),
    location GEOGRAPHY(POINT,4326),
    times_visited INT,
    user_created BOOLEAN,
    avg_rat FLOAT DEFAULT 2.5
);

CREATE TABLE IF NOT EXISTS review (
    user_id UUID REFERENCES geo_user(user_id) ON DELETE CASCADE NOT NULL,
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE NOT NULL,
    rating CHAR NOT NULL,
    review VARCHAR(511),
    date INT NOT NULL
);

CREATE TABLE IF NOT EXISTS accessibility (
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    wheelchair_accessible BOOLEAN,
    service_animal_friendly BOOLEAN,
    multilingual_support BOOLEAN,
    braille_signage BOOLEAN,
    hearing_assistance BOOLEAN,
    large_print_materials BOOLEAN,
    accessible_restrooms BOOLEAN
);

CREATE TABLE IF NOT EXISTS gems_visited (
    gem_visited_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES geo_user(user_id) ON DELETE CASCADE,
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    date_visited date NOT NULL
);





CREATE TABLE IF NOT EXISTS gems_pinned (
    gem_pinned_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES geo_user(user_id) ON DELETE CASCADE,
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    date_pinned date NOT NULL
);

CREATE TABLE IF NOT EXISTS image_group (
    image_group_id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    gem_id UUID REFERENCES hidden_gem(gem_id) ON DELETE CASCADE,
    image_1 VARCHAR(255),
    image_2 VARCHAR(255),
    image_3 VARCHAR(255)
);



