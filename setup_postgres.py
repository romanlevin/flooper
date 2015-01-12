CREATE_USER_TABLE = """
CREATE EXTENSION citext;

CREATE TABLE IF NOT EXISTS user (
  id INTEGER PRIMARY KEY,
  email CITEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created TIMESTAMP DEFAULT now,
  modified TIMESTAMP
);
"""


CREATE_FLOOP_TABLE = """
CREATE TABLE IF NOT EXISTS floop (
  id INTEGER PRIMARY KEY,
  content TEXT NOT NULL,
  user_id INTEGER,
  FOREIGN KEY(user_id) REFERENCES user(id) NOT NULL,
  created TIMESTAMP DEFAULT now,
  modified TIMESTAMP
)
"""


CREATE_RELATIONSHIP_TABLE = """
CREATE TABLE IF NOT EXISTS relationship (
    id INTEGER PRIMARY KEY,
    follower_id INTEGER REFERENCES user(id),
    followed_id INTEGER REFERENCES user(id),
    PRIMARY KEY(follower_id, followed_id),
    created TIMESTAMP DEFAULT now,
    modified TIMESTAMP
)
"""


TRIGGERS = """
CREATE OR REPLACE FUNCTION update_modified_column()	
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified = now();
    RETURN NEW;	
END;
$$ language 'plpgsql';

CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON user FOR EACH ROW EXECUTE PROCEDURE  update_modified_column();
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON floop FOR EACH ROW EXECUTE PROCEDURE  update_modified_column();
"""