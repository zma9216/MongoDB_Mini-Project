from pymongo import MongoClient
from pprint import pprint
from time import time


def display_menu():
    # Print out numbered options
    print("Please select an option by entering a number:")
    print("1. Find average price of a neighbourhood")
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
        nbh = input(msg).strip()
        if not nbh:
            # Catches empty strings
            print("Input cannot be empty. Please try again.")
        else:
            # Regex pattern for matching character from beginning to end
            return "^" + nbh + "$"


def t5(db):
    coll = db["listings"]
    msg = "Please enter a neighbourhood: "
    nbh = handle_input(msg)
    # Create aggregation pipeline
    # Regex implementation based on solution
    # from https://stackoverflow.com/a/33971033 by Somnath Muluk
    pipeline = [
        {"$match": {"neighbourhood": {"$regex": nbh, "$options": "i"}}},
        {"$group": {"_id": "$neighbourhood", "price": {"$avg": "$price"}}}
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
        # Print message if no rows were found
        print("\nNeighbourhood does not exist.")
    else:
        for data in cursor:
            # Print neighbourhood
            print("\nNeighbourhood: " + data["_id"])
            # Print price
            print("Price: %.2f" % data["price"])
    print("\nTask 5 query time in MongoDB: %.5f ms\n" % query_time)


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
            t5(db)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to client
    client.close()
