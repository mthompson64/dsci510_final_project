import sqlite3

conn = sqlite3.connect('final_project.db')
cur = conn.cursor()

cur.execute("""CREATE TABLE IF NOT EXISTS zipcode_table (
    zip_id INTEGER PRIMARY KEY,
    zipcode INTEGER NOT NULL UNIQUE,
    zipcode_url TEXT,
    lat FLOAT,
    long FLOAT,
    current_pop INTEGER,
    median_income INTEGER
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS charging_locations_table (
    charger_id INTEGER PRIMARY KEY,
    zip_id INTEGER,
    name TEXT,
    address TEXT,
    city TEXT,
    FOREIGN KEY (zip_id) REFERENCES zipcode_table (zip_id)
)""")
cur.execute("""CREATE TABLE IF NOT EXISTS restaurant_locations_table (
    restaurant_id TEXT PRIMARY KEY,
    zip_id INTEGER,
    name TEXT,
    address TEXT,
    city TEXT,
    FOREIGN KEY (zip_id) REFERENCES zipcode_table (zip_id)
)""")

conn.commit()
conn.close()