import sqlite3
from time import time


def display_menu():
    # Print out numbered options
    print("Please select an option by entering a number:")
    print("1. Find unreviewed properties")
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


def t4(cursor):
    """
    Find which listed properties that have not
    received any reviews and sort by listing id (id)
    :param Cursor cursor: Cursor to the database
    """
    query_time = 0
    # Get time before executing query
    start = time()
    cursor.execute('''
    SELECT id as "Listing IDS"
    FROM listings
    WHERE id NOT IN (
    SELECT listing_id
    FROM reviews)
    ORDER BY id
    LIMIT 10;
        ''')
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    # Get header
    name = [i[0] for i in cursor.description]
    # Print header
    print("\n" + "".join(name))
    rows = cursor.fetchall()
    for row in rows:
        if not row[0]:
            # Print message if no rows were found
            print("No listings are found.")
        else:
            # Print each row of query result
            print(row["Listing IDS"])
    # Display query time
    print("\nTask 4 query time in SQLite: %.5f ms\n" % query_time)


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
            t4(cur)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to database
    conn.close()
