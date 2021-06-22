import sqlite3
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


def format_output(cursor, rows):
    """
    Function for formatting the SQLite output to a table
    Implementation based on solution https://stackoverflow.com/a/48138561 from Hai Vu
    :param Cursor cursor: Cursor to the database
    :param list rows: List of rows of a query result
    """
    # Get list of headers from Cursor object
    headers = [i[0] for i in cursor.description]
    # Get list of lengths from headers
    widths = [len(cell) for cell in headers]
    # Determine the maximum width for each column
    for row in rows:
        for i, cell in enumerate(row):
            widths[i] = max(len(str(cell)), widths[i])
    # Join headers
    formatted_row = " ".join("{:%d}" % width for width in widths)
    # Print headers
    print("\n" + formatted_row.format(*headers))
    # Unpack the query results and print data
    for row in rows:
        print(formatted_row.format(*row))


def t3(cursor):
    """
    Finds how many listings each host own and sort by host_id
    :param Cursor cursor: Cursor to the database
    """
    query_time = 0
    # Get time before executing query
    start = time()
    cursor.execute('''
    SELECT host_id, host_name, COUNT(id) as "count"
    FROM listings
    GROUP BY host_id, host_name
    ORDER BY host_id
    LIMIT 10;
    ''')
    # Get time after executing query
    end = time()
    # Add difference to total and convert to ms
    query_time += (end - start) * 1000
    rows = cursor.fetchall()
    for row in rows:
        if not row[0]:
            # Print message if no rows were found
            print("\nHosts nor listings exist.")
        else:
            # Format and print output
            format_output(cursor, rows)
    # Display query time
    print("\nTask 3 query time in SQLite: %.5f ms\n" % query_time)


if __name__ == "__main__":
    # Set database
    db = "./A5.db"
    # Connect to database
    conn = sqlite3.connect(db)
    # Set to Row factory mode
    conn.row_factory = sqlite3.Row
    # Get Cursor object
    cur = conn.cursor()
    loop = True
    # While loop which will keep going until loop = False
    while loop:
        # Displays menu
        option = display_menu()

        if option is 1:
            # Call option 1 function
            t3(cur)

        elif option is 2:
            # Print message for closing program
            print("Ending program...")
            # Set loop flag to false
            loop = False

    # Close connection to database
    conn.close()
