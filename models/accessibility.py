'''
CREATE TABLE IF NOT EXISTS accessibility (
    accessibility_id UUID PRIMARY KEY,
    gem_id UUID REFERENCES HiddenGem(gem_id) ON DELETE CASCADE,
    wheelchair_accessible BOOLEAN,
    service_animal_friendly BOOLEAN,
    multilingual_support BOOLEAN,
    braille_signage BOOLEAN,
    hearing_assistance BOOLEAN,
    large_print_materials BOOLEAN,
    accessible_restrooms BOOLEAN
);
'''