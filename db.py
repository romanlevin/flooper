import sqlite3
import psycopg2

def connect():
    return sqlite3.connect('flooper.db')
    