import sqlite3
from webcrawler.dbCreate_class import *
import pandas as pd
# Connect to Databases
# 1) Times
times = database('./webcrawler/timesDB')
times_cursor = times.cursor()
# 2) HQ
hq    = database('./webcrawler/hqDB')
hq_cursor = hq.cursor()

# 3) lpr
lpr   = database('./webcrawler/lprDB')
lpr_cursor = lpr.cursor()

# Create STATLookup Database
stat  = database('statDB')
stat_cursor = stat.cursor()

stat_cursor.executescript(
    '''
    DROP TABLE IF EXISTS header;
    DROP TABLE IF EXISTS subheader;
    DROP TABLE IF EXISTS variable;

    CREATE TABLE header (
        id   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        source TEXT,
        name  TEXT  
    );
    
   

    CREATE TABLE subheader (
        id INTEGER,
        header_id INTEGER,
        name TEXT,
        desc_da TEXT
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


# Merge Headers;

times_header = times_cursor.execute(
    '''
    SELECT * FROM header
    '''
).fetchall()

def fetch_data(cursor, source):
    times_header = cursor.execute(
        "SELECT * FROM header"
    ).fetchall()

    for row in times_header:
        id     = row[0]
        source = source
        name   = row[2]

        # Based on ID it should extract subheader Data
        subheader = cursor.execute(
            "SELECT * FROM subheader WHERE header_id = ?", (id,)
        ).fetchall()

    return subheader




print(
    fetch_data(times_cursor,"times")
)



# hq_header = hq_cursor.execute(
#     '''
#     SELECT * FROM header
#     '''
# ).fetchall()
#
# lpr_header = lpr_cursor.execute(
#     '''
#     SELECT * FROM header
#     '''
# ).fetchall()
#
#
# for row in times_header:
#     id = row[0]
#     source = 'Times'
#     name = row[2]
#
#     stat_cursor.execute(
#         '''
#         INSERT INTO header (source, name) VALUES (?, ?)
#         ''', (source, name)
#     )
#
# for row in hq_header:
#     id = row[0]
#     source = 'High Quality'
#     name = row[2]
#
#     stat_cursor.execute(
#         '''
#         INSERT INTO header (source, name) VALUES (?, ?)
#         ''', (source, name)
#     )
#
# for row in lpr_header:
#     id = row[0]
#     source = 'eHealth'
#     name = row[2]
#
#     stat_cursor.execute(
#         '''
#         INSERT INTO header (source, name) VALUES (?, ?)
#         ''', (source, name)
#     )
#
# stat.commit()
#
# # Merge Subheaders
#
# times_subheader = times_cursor.execute(
#     '''
#     SELECT * FROM subheader
#     '''
# ).fetchall()
#
# hq_subheader = hq_cursor.execute(
#     '''
#     SELECT * FROM subheader
#     '''
# ).fetchall()
#
# lpr_subheader = lpr_cursor.execute(
#     '''
#     SELECT * FROM subheader
#     '''
# ).fetchall()
