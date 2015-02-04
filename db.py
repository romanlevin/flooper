from psycopg2.extras import RealDictCursor
from psycopg2 import connect as pgconnect
import contextlib
import os
from flask import g


def connect():
    conn = pgconnect(os.getenv('DATABASE_URL'))
    return conn


@contextlib.contextmanager
def transaction(cursor_name=None):
    cursor = g.get('db_cursor')
    # If a cursor is open, we are inside a transaction already. Continue using the cursor.
    if cursor and not cursor.closed:
        yield cursor
    # If there is not cursor or it closed, we are outside a transaction and must create a new cursor.
    else:
        # Maintain a connection object in the app context, and reuse it.
        db_connection = g.get('db_connection')
        if not db_connection or db_connection.closed:
            db_url = os.getenv('DATABASE_URL')
            g.db_connection = db_connection = pgconnect(db_url, cursor_factory=RealDictCursor)
        with db_connection as conn:
            cursor = conn.cursor(cursor_name) if cursor_name else conn.cursor()
            with cursor as cursor:
                yield cursor
