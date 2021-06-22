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


def handle_values(msg):
    while True:
        try:
            # Prompt user for number input
            number = int(input(msg))
            if number >= 0:
                # Return input if positive
                return int(number)
            else:
                # Catches negative numbers
                print("Input must be positive. Please try again.")
        except (ValueError, TypeError):
            # Raise error if input is of wrong type
            print("Empty or invalid value. Please try again.")


def smart_truncate(content, length=75, suffix='...'):
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0] + suffix


def t8(db):
    """
    Find the host's name, rental price and most recent review
    for listing inputted by the user
    :param db: MongoDB database
    """
    coll = db["listings"]
    msg = "Please enter a listing ID: "
    id = handle_values(msg)
    pipeline = [
        {"$match": {"id": id}},
        {"$unwind": "$reviews"},
        {"$sort": {"reviews.date": -1}},
        {"$limit": 1}
    ]
    query_time = 0
    # Get time before executing query
    start = time()
    cursor = list(coll.aggregate(pipeline))
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    if not cursor:
        # Print message if no results were found
        print("\nListing cannot be found or does not exist.")
    else:
        for data in cursor:
            # Print host name
            print("\nHost name: " + data["host_name"])
            # Print price
            print("Price: %d" % data["price"])
            if not data["reviews"]["comments"]:
                # Change limit to 2
                pipeline[3] = {"$limit": 2}
                # Add skip to pipeline
                pipeline.append({"$skip": 1})
                # Get the date of next most recent review
                date = list(coll.aggregate(pipeline))
                # Print message if listing does not have a recent review
                print("No reviews since %s" % date[0]["reviews"]["date"])
            else:
                # Truncate and print review
                print("Review on %s: %s" % (data["reviews"]["date"], smart_truncate(data["reviews"]["comments"])))

    print("\nTask 8 query time in MongoDB: %.5f ms\n" % query_time)


if __name__ == "__main__":
    client = MongoClient()
    db = client["A5db"]
    loop = True
    # While loop which will keep going until loop = False
    while loop:
        # Displays menu
        option = display_menu()

        if option is 1:
            # Call option 1 function
            t8(db)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to client
    client.close()
