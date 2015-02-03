-- case-insensitive text for email
CREATE EXTENSION citext;

CREATE TABLE flooper_user (
  id serial PRIMARY KEY,
  email CITEXT UNIQUE NOT NULL,
  name TEXT NOT NULL CHECK (name <> ''),
  -- password_hash TEXT NOT NULL CHECK (password_hash <> ''),
  created_at TIMESTAMPTZ DEFAULT now(),
  modified_at TIMESTAMPTZ
);

CREATE TABLE flooper_floop (
  id serial PRIMARY KEY,
  content TEXT NOT NULL,
  user_id INTEGER REFERENCES flooper_user,
  created_at TIMESTAMPTZ DEFAULT now(),
  modified_at TIMESTAMPTZ
);

CREATE INDEX flooper_floop_created_at_user_id_index ON flooper_floop (created_at, user_id);

CREATE TABLE flooper_user_relationship (
  follower_id INTEGER REFERENCES flooper_user,
  followed_id INTEGER REFERENCES flooper_user,
  PRIMARY KEY(follower_id, followed_id),
  created_at TIMESTAMPTZ DEFAULT now(),
  modified_at TIMESTAMPTZ
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
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_user FOR EACH ROW EXECUTE PROCEDURE update_modified_at_column();
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_floop FOR EACH ROW EXECUTE PROCEDURE update_modified_at_column();
CREATE TRIGGER update_customer_modtime BEFORE UPDATE ON flooper_user_relationship FOR EACH ROW EXECUTE PROCEDURE  update_modified_at_column();
