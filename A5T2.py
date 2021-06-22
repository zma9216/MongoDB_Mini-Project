from pymongo import MongoClient
import csv


def read_file(file):
    """
    Function for reading CSV file and
    retrieving data in suitable format for MongoDB
    :param str file: CSV filename
    :return: Returns a list of dictionaries from the data read
    :rtype: list
    """
    with open(file, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        # Create list
        data = list(reader)
        # Convert all digit strings to integers
        for item in data:
            for key, value in item.items():
                try:
                    # Check if string is all digits
                    if item[key].isdigit():
                        # Convert string to int
                        item[key] = int(value)
                # Skip if ValueError, e.g. all alphabet letters
                except ValueError:
                    pass
    return data


def populate_coll(db):
    """
    Function to populate listings collection in database
    where all the reviews associated to one given listing
    are to be embedded within that one listing
    :param db: MongoDB database
    """
    # Create/open listings collection in db
    coll = db["listings"]
    # Delete all previous entries in collection
    coll.delete_many({})

    # Get listings and reviews
    listings = read_file("./YVR_Airbnb_listings_summary.csv")
    reviews = read_file("./YVR_Airbnb_reviews.csv")

    for l in listings:
        # Create reviews array in listings
        l["reviews"] = []
        for r in reviews:
            # Add review to array if both listing ids match
            if l["id"] == r["listing_id"]:
                l["reviews"].append(r)

    # Insert data into listings collection
    coll.insert_many(listings)


if __name__ == "__main__":
    # Connect to MongoDB server
    client = MongoClient()
    # Create/open the A5db database on server
    db = client["A5db"]
    # Create and populate listings collection
    populate_coll(db)
    # Close connection to client
    client.close()
