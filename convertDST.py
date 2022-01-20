# This script extracts the raw Database
# and has to be used with caution.
# If the original crawler fails, and you
# copy without knowing these fails
# you might break your database

import sqlite3
import os
import shutil

# Generate Disclaimer statement for the program
print(
    '''
    ==========================================================================================
    | This program updates the local database(s), by doing a simple copy of the raw          |
    | database(s) inside the webcrawler.                                                     |
    |                                                                                        |
    | NOTE: Before you update the database(s), please make sure that it is (all) up-to-date. |
    | Otherwise it will break you program!                                                   |
    ==========================================================================================
    '''
)

# Create prompt, and input
print(
    '''
    Are you sure you want to continue? [Yes/No]
    '''
)
do_copy = str(input(
    '''
    '''
)).lower()


# Start program conditional on the
# input
if do_copy == "yes":
    print("Starting Update!")

    # Create Copy of Database as dstTIMES.sqlite
    # directly into the main folder
    shutil.copyfile(
        src= "webcrawler/dstTIMESraw.sqlite",
        dst= "dstTIMES.sqlite"
    )

    # # Create new database:
    # # This is called dstDB.sqlite
    # # TODO: Make robust - for more DBs
    # connection = sqlite3.connect(
    #     'dstDB.sqlite'
    # )
    #
    # # Create Cursor:
    # cursor = connection.cursor(
    #
    # )


    print("Done!")


elif do_copy == "no":
    print("Aborted!")


else:
    print("Invalid Input!")