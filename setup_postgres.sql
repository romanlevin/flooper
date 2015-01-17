-- case-insensitive text for email
CREATE EXTENSION citext;

CREATE TABLE flooper_user (
  id INTEGER PRIMARY KEY,
  email CITEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT now(),
  modified_at TIMESTAMP
);

CREATE TABLE flooper_floop (
  id INTEGER PRIMARY KEY,
  content TEXT NOT NULL,
  user_id INTEGER,
  FOREIGN KEY(user_id) REFERENCES flooper_user(id),
  created_at TIMESTAMP DEFAULT now(),
  modified_at TIMESTAMP
);

CREATE TABLE flooper_user_relationship (
    follower_id INTEGER REFERENCES flooper_user(id),
    followed_id INTEGER REFERENCES flooper_user(id),
    PRIMARY KEY(follower_id, followed_id),
    created_at TIMESTAMP DEFAULT now(),
    modified_at TIMESTAMP
);

-- Function to update modified_at column to current time
CREATE OR REPLACE FUNCTION update_modified_at_column()	
RETURNS TRIGGER AS $$
BEGIN
    NEW.modified_at = now();
    RETURN NEW;	
END;
$$ language 'plpgsql';

-- Triggers to update the modified_at column
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_user FOR EACH ROW EXECUTE PROCEDURE  update_modified_at_column();
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_floop FOR EACH ROW EXECUTE PROCEDURE  update_modified_at_column();
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_user_relationship FOR EACH ROW EXECUTE PROCEDURE  update_modified_at_column();
