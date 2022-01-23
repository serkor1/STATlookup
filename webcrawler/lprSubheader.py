# This program collects the headers
# from LPR

# Import Collector;
import time

from lprCollector_class import lprCollector
from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.parse, urllib.error
import ssl

# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'lprRAW.sqlite'
)

cursor = connection.cursor()

# 2) Create New table
cursor.executescript('''
    DROP TABLE IF EXISTS subheader;

    CREATE TABLE subheader (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        header_id INTEGER,
        url TEXT UNIQUE,
        name  TEXT

    )
''')



# Read Headerdata:
header_data = cursor.execute(
    '''
    SELECT * FROM header
    '''
).fetchall()



# Ignore Certification Errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

time.sleep(60)
iteration = 0
for row in header_data:
    iteration += 1
    print("Iteration", iteration, "of", len(header_data), "iterations!")

    # ID goes inside subheader as foreing key
    id = row[0]

    # Extract Register URL
    url = row[1]

    # Extract Main Content
    subheaders = lprCollector(
        url = url,
        selector="#list-tab-tables",
        ctx=ctx
    )

    names = subheaders.get_name()
    urls  = subheaders.get_url()

    for i in range(len(names)):

        cursor.execute(
            '''
            INSERT INTO subheader (header_id, url, name) VALUES (?, ?, ?)
            ''', (id, urls[i], names[i])
        )

    connection.commit()

    time.sleep(30)

