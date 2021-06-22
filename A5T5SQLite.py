import sqlite3
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
    """
    Function for validating string inputs
    :param str msg: Message prompting user for input
    :return: Return user input
    :rtype: str
    """
    while True:
        # Prompt user for input (string)
        nbh = input(msg).strip()
        if not nbh:
            # Catches empty strings
            print("Input cannot be empty. Please try again.")
        else:
            return nbh


def t5(cursor):
    """
    Find average rental price for a given neighbourhood
    :param Cursor cursor: Cursor to the database
    """
    # Print message
    msg = "Please enter a neighborhood: "
    # Get neighbourhood string from user
    nbh = handle_input(msg)
    query_time = 0
    # Get time before executing query
    start = time()
    cursor.execute('''
    SELECT neighbourhood, AVG(price) as "price"
    FROM listings
    WHERE neighbourhood = ? COLLATE NOCASE
    AND neighbourhood IN (
    SELECT neighbourhood
    FROM listings);
    ''', (nbh,))
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    rows = cursor.fetchall()
    for row in rows:
        if not row[0]:
            # Print message if no rows were found
            print("\nNeighbourhood does not exist.")
        else:
            # Print neighbourhood
            print("\nNeighbourhood: " + row[0])
            # Print price
            print("Price: %.2f" % row[1])
    # Display query time
    print("\nTask 5 query time in SQLite: %.5f ms\n" % query_time)


if __name__ == "__main__":
    db = "./A5.db"
    conn = sqlite3.connect(db)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    loop = True
    # While loop which will keep going until loop = False
    while loop:
        # Displays menu
        option = display_menu()

        if option is 1:
            # Call option 1 function
            t5(cur)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to database
    conn.close()
