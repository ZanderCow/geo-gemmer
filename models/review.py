'''
CREATE TABLE IF NOT EXISTS review (
    review_id UUID PRIMARY KEY,
    user_id UUID REFERENCES Users(user_id) ON DELETE CASCADE,
    gem_id UUID REFERENCES HiddenGem(gem_id) ON DELETE CASCADE,
    rating CHAR(1),
    review TEXT
);
'''