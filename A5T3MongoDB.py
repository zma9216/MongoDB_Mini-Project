from pymongo import MongoClient
from pprint import pprint
from time import time


def display_menu():
    # Print out numbered options
    print("Please select an option by entering a number:")
    print("1. Find number of properties owned by a host")
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


def t3(db):
    """
    Finds how many listings each host own and sort by host_id
    :param db: MongoDB database
    """
    # Get collection in the db
    coll = db["listings"]
    # Create aggregation pipeline
    pipeline = [
        {"$group": {"_id": {"host_id": "$host_id",
                            "host_name": "$host_name"},
                    "count": {"$sum": 1}}},
        # sort all the docs by host_id
        {"$sort": {"_id": 1}},
        # Take the first 10 rows
        {"$limit": 10}
    ]
    query_time = 0
    # Get time before executing query
    start = time()
    # Execute query and get Cursor instance
    cursor = list(coll.aggregate(pipeline))
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    if not cursor:
        # Print message if no data was found
        print("No listings are found.")
    else:
        # Print headers (hardcoded due to difficulty in retrieval)
        print("\n{:7s} {:13s} {:5s}".format("host_id", "host_name", "count"))
        for data in cursor:
            # Get values
            host_id = data["_id"]["host_id"]
            host_name = data["_id"]["host_name"]
            count = data["count"]
            # Print values
            print("{:7d} {:13s} {:5d}".format(host_id, host_name, count))
    # Display query time
    print("\nTask 3 query time in MongoDB: %.5f ms\n" % query_time)


if __name__ == "__main__":
    # Connect to MongoDB server
    client = MongoClient()
    # Open database on server
    db = client["A5db"]
    loop = True
    # While loop which will keep going until loop = False
    while loop:
        # Displays menu
        option = display_menu()

        if option is 1:
            # Call option 1 function
            t3(db)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to client
    client.close()
