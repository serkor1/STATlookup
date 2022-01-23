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

    # Create New Main Database;
    # -------------------------
    statDB = sqlite3.connect('statDB.sqlite')

    # Create Cursor for main DB;
    # --------------------------
    statDB_cursor = statDB.cursor()

    # Create Data for main DB;
    # --------------------------
    statDB_cursor.executescript(
        '''
        DROP TABLE IF EXISTS header;
        DROP TABLE IF EXISTS subheader;
        DROP TABLE IF EXISTS variable;

        CREATE TABLE header (
            id     INTEGER,
            name  TEXT  
        );
        
        CREATE TABLE subheader (
            id INTEGER,
            header_id INTEGER,
            name TEXT
        );
        
        CREATE TABLE variable (
            id     INTEGER UNIQUE,
            header_id INTEGER,
            subheader_id INTEGER,
            link  TEXT UNIQUE,
            var TEXT,
            var_name TEXT,
            html TEXT
        )
        
        '''
    )

    # Create DST Connection and Cursor;
    dst_db = sqlite3.connect(
        "webcrawler/dstTIMESraw.sqlite"
    )

    dstCursor = dst_db.cursor()

    # Create LPR Connection and Cursor;
    lpr_db = sqlite3.connect(
        "webcrawler/lprRAW.sqlite"
    )

    lprCursor = lpr_db.cursor()



    # Update HEADERS; #####
    dst_header = dstCursor.execute(
        '''
        SELECT * FROM header
        '''
    ).fetchall()

    lpr_header = lprCursor.execute(
        '''
        SELECT * FROM header
        '''
    )

    # headers;
    for row in dst_header:
        id = row[0]
        name = row[2]

        statDB_cursor.execute(
            '''
            INSERT INTO header (id ,name) VALUES (?, ?)
            ''', (id, name)
        )

    for row in lpr_header:
        id = row[0] + len(dst_header)
        name = row[2]

        statDB_cursor.execute(
            '''
            INSERT INTO header (id,name) VALUES (?, ?)
            ''', (id, name)
        )

    statDB.commit()



    # Update subheaders; #####
    dst_subheader = dstCursor.execute(
        '''
        SELECT * FROM subheader
        '''
    ).fetchall()

    lpr_subheader = lprCursor.execute(
        '''
        SELECT * FROM subheader
        '''
    )

    for row in dst_subheader:
        id = row[0]
        header_id = row[1]
        name = row[3]

        statDB_cursor.execute(
            '''
            INSERT INTO subheader (id, header_id ,name) VALUES (?, ?, ?)
            ''', (id, header_id, name)
        )

    for row in lpr_subheader:
        id = row[0] + len(dst_subheader)
        header_id = row[1] + len(dst_header)
        name = row[3]

        statDB_cursor.execute(
            '''
            INSERT INTO subheader (id, header_id, name) VALUES (?, ?, ?)
            ''', (id, header_id, name)
        )

    statDB.commit()



    # Variables;
    dst_variable = dstCursor.execute(
        '''
        SELECT * FROM variable
        '''
    ).fetchall()

    lpr_variable = lprCursor.execute(
        '''
        SELECT * FROM variable
        '''
    )

    for row in dst_variable:
        id = row[0]
        header_id = row[1]
        subheader_id = row[2]
        url = row[3]
        var = row[4]
        var_name = row[5]
        html = row[6]

        statDB_cursor.execute(
            '''
            INSERT INTO variable (id, header_id, subheader_id, link, var, var_name, html) VALUES (?, ?, ?, ?, ?, ?,?)
            ''', (id, header_id, subheader_id, url,var,var_name, html)
        )

    for row in lpr_variable:
        id = row[0] + len(dst_variable)
        header_id = row[1] + len(dst_header)
        subheader_id = row[2] + len(dst_subheader)
        url = row[3]
        var = row[4]
        var_name = row[5]
        html = row[6]

        statDB_cursor.execute(
            '''
            INSERT INTO variable (id, header_id, subheader_id, link, var, var_name, html) VALUES (?, ?, ?, ?, ?, ?,?)
            ''', (id, header_id, subheader_id, url, var, var_name, html)
        )

    statDB.commit()








    print("Done!")


elif do_copy == "no":
    print("Aborted!")


else:
    print("Invalid Input!")