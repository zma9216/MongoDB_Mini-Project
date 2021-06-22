import sqlite3
import csv


def read_file(file):
    """
    Function for reading CSV file and
    retrieving data in suitable format for SQLite
    :param str file: CSV filename
    :return: Returns a list of tuples from the data read
    :rtype: list
    """
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        # Skip header
        next(reader)
        # Get data as list of tuples
        data = [tuple(row) for row in reader]
    return data


def create_db(cursor):
    """
    Function for creating the SQLite database
    :param Cursor cursor: Cursor to the database
    """
    # Get listings
    listings = read_file("./YVR_Airbnb_listings_summary.csv")
    # Get reviews
    reviews = read_file("./YVR_Airbnb_reviews.csv")
    # Execute SQLite script
    # Drop listings table and reviews table if they exist
    # Create listings and reviews table
    cursor.executescript('''
    DROP TABLE IF EXISTS listings;
    DROP TABLE IF EXISTS reviews;
    
    CREATE TABLE listings (
    id INTEGER, 
    name TEXT, 
    host_id INTEGER, 
    host_name TEXT, 
    neighbourhood TEXT,
    room_type TEXT,
    price INTEGER,
    minimum_nights INTEGER,
    availability_365 INTEGER,
    PRIMARY KEY(id));
    
    CREATE TABLE reviews (
    listing_id INTEGER,
    id INTEGER, 
    date TEXT, 
    reviewer_id INTEGER, 
    reviewer_name TEXT,
    comments TEXT,
    PRIMARY KEY(id)
    );
    ''')

    # Insert listings into listings table
    cursor.executemany('''
    INSERT INTO listings
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);''', listings)

    # Insert reviews into reviews table
    cursor.executemany('''
    INSERT INTO reviews
    VALUES (?, ?, ?, ?, ?, ?);''', reviews)


if __name__ == "__main__":
    # Set database
    db = "./A5.db"
    # Connect to database
    conn = sqlite3.connect(db)
    # Set to Row factory mode
    conn.row_factory = sqlite3.Row
    # Get Cursor object
    cur = conn.cursor()
    # Create database
    create_db(cur)
    # Save changes to database
    conn.commit()
    # Close connection to database
    conn.close()
