import sqlite3
from time import time


def display_menu():
    # Print out numbered options
    print("Please select an option by entering a number:")
    print("1. Find host")
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
    """
    Function for validating number inputs
    :param str msg: Message to prompt user for input
    :return: Returns number inputted by user
    :rtype: int
    """
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
    """
    Function for truncating long strings without cutting off words
    :param str content: Long string to be truncated
    :param int length: Maximum length of string allowed
    :param str suffix: Ellipses for the end
    :return: Returns the truncated string
    :rtype: str
    """
    if len(content) <= length:
        return content
    else:
        return content[:length].rsplit(' ', 1)[0] + suffix


def t8(cursor):
    """
    Find the host's name, rental price and the most recent review
    for listing inputted by the user
    :param Cursor cursor: Cursor to the database
    """
    # Print prompt message
    msg = "Please enter a listing ID: "
    # Get listing id from user
    id = handle_values(msg)
    query_time = 0
    # Get time before executing query
    start = time()
    cursor.execute('''
    SELECT l.host_name, l.price, r.comments, r.date
    FROM reviews r, listings l
    WHERE l.id = ?
    AND l.id == r.listing_id
    ORDER BY r.date DESC
    LIMIT 1;
    ''', (id,))
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    rows = cursor.fetchall()
    if not rows:
        # Print message if no rows were found
        print("\nListing cannot be found or does not exist.")
    else:
        for row in rows:
            # Print host name
            print("\nHost name: " + row[0])
            # Print price
            print("Price: %d" % row[1])
            if not row[2]:
                # Get next most recent review
                cursor.execute('''
                        SELECT r.date
                        FROM reviews r, listings l
                        WHERE l.id = ?
                        AND l.id == r.listing_id
                        ORDER BY r.date DESC
                        LIMIT 1 OFFSET 1;
                        ''', (id,))
                date = cursor.fetchone()
                # Print message if listing does not have a recent review
                print("No reviews since %s" % date[0])
            else:
                # Truncate and print review
                print("Review on %s: %s" % (row[3], smart_truncate(row[2])))

    print("\nTask 8 query time in SQLite: %.5f ms\n" % query_time)


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
            t8(cur)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to database
    conn.close()
