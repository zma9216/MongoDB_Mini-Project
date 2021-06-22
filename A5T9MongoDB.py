from pymongo import MongoClient
from pprint import pprint
from time import time


def display_menu():
    # Print out numbered options
    print("Please select an option by entering a number:")
    print("1. Find listings")
    print("2. Exit")
    while True:
        # While loop for prompting user again if input is invalid
        try:
            # Prompt user for an integer input
            number = int(input("Option: "))
            if 0 < number < 3:
                # Return integer if is between 1 and 5
                return number
            else:
                # Catches input if input is negative or outside of range
                print("Please select one of the options listed.")
        except(ValueError, TypeError):
            # Raise error if input is of wrong type
            print("Invalid selection. Please try again.")


def handle_input(msg):
    while True:
        # Prompt user for input (string)
        keywords = input(msg).strip()
        if not keywords:
            # Catches empty strings
            print("Input cannot be empty. Please try again.")
        else:
            return keywords


def create_coll_index(db):
    """
    Function for creating text index in collection
    :param db: MongoDB database
    """
    coll = db["listings"]
    # Drop all indexes
    coll.drop_indexes()
    # Create text index
    coll.create_index([("reviews.comments", "text")])


def t9(db):
    """
    Find the top 3 listings which have reviews most similar
    to the set of keywords inputted by the user
    :param db: MongoDB database
    """
    coll = db["listings"]
    msg = "Please enter your keywords: "
    keywords = handle_input(msg)
    # Create text search query
    query = {"$text": {"$search": keywords}}
    # Create projection
    project = {"score": {"$meta": "textScore"}}
    # Create sorting criteria
    criteria = [("score", {"$meta": "textScore"})]
    query_time = 0
    # Get time before executing query
    start = time()
    # Execute query and limit to 3 results, then get Cursor instance
    cursor = list(coll.find(query, project).sort(criteria).limit(3))
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    if not cursor:
        # Print message if not listings were found
        print("\nNo listings were found.")
    else:
        # Print header
        print("\nListing IDs:")
        for data in cursor:
            # Print values
            print(data["id"])
    print("\nTask 9 query time in MongoDB: %.5f ms\n" % query_time)


if __name__ == "__main__":
    client = MongoClient()
    db = client["A5db"]
    print("\nCreating index...\n")
    create_coll_index(db)
    loop = True
    # While loop which will keep going until loop = False
    while loop:
        # Displays menu
        option = display_menu()

        if option is 1:
            # Call option 1 function
            t9(db)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to client
    client.close()
