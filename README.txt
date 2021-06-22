Name: ZiQing Ma
CCID: zm1
Lab Section: H01
I, ZiQing Ma, declare that I did not collaborate with anyone in this assignment.

Files:
A5T1.py, A5T2.py,
A5T3MongoDB.py, A5T3SQLite.py,
A5T4MongoDB.py, A5T4SQLite.py,
A5T5MongoDB.py, A5T5SQLite.py,
A5T8MongoDB.py, A5T8SQLite.py,
A5T9MongoDB.py, README.txt

IMPORTANT: 
After running A5T2.py, the outputs for my MongoDB programs will be incorrect on the first run for some reason, but will fix itself if you re-run the program.
This error only occurred on the lab machines and I have not ran into this error on my own machine (tested with Python 3.5 and on Linux VM).
Honestly, I am really not sure why it is doing this on the lab machines. In addition, the outputs are fine when I dropped the MongoDB database
and create it again in the same PuTTY instance. So, please re-run the MongoDB program you first opened and the outputs will be fine. Thank you.

Notes:
Default port on localhost was used for MongoDB connection.
Lack of comments for some functionalities due to duplicate code.
Comments are added if there were significant differences,
so please refer to either SQLite or MongoDB version of the program for missing comments if none were found.

Instructions: 
1. Run A5T1.py and A5T2.py in terminal prefixed with "python3" to build databases.
2. Select options 1-2 by entering the corresponding number for all remaining programs.
    a. For option 1 if:
        i. A5T3*.py: Find how many listings each host own (sorted by host_id) # Alternative approach for task used
        ii. A5T4*.py: Find which listed properties that have not received any reviews (sorted by listing id)
        iii. A5T5*.py: Find the average rental price for a given neighbourhood
        iv. A5T8*.py: Find the host's name, rental price and most recent review for a given listing
        v. A5T9MongoDB.py: Find the top 3 listings which have reviews most similar to a given set of keywords
3. Once you are done, please enter 2 to exit the program.
