# This program collects the headers
# from LPR

# Import Collector;
import time

from lprCollector_class import lprCollector
from matplotlib.cbook import flatten
import requests
import sqlite3
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.parse, urllib.error
import ssl


def get_html(url, selector):
    content = BeautifulSoup(
        requests.get(url).content,
        'html.parser'
    ).select(selector)

    return content


# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'lprRAW.sqlite'
)

cursor = connection.cursor()

# 2) Create New table
cursor.executescript('''
    DROP TABLE IF EXISTS variable;

    CREATE TABLE variable (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        header_id INTEGER,
        subheader_id INTEGER,
        link  TEXT UNIQUE,
        var TEXT,
        var_name TEXT,
        html TEXT

    )
''')



# Read Headerdata:
subheader_data = cursor.execute(
    '''
    SELECT * FROM subheader
    '''
).fetchall()


# Ignore Certification Errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


iteration = 0
for row in subheader_data:
    iteration += 1



    # ID goes inside varaibles as foreing key
    id = row[0]
    header_id = row[1]

    # Extract Register URL
    url = row[2]

    # Extract Main Content
    variables = lprCollector(
        url = url,
        selector="#list-tab-variables",
        ctx=ctx
    )

    names = variables.get_name()
    urls  = variables.get_url()

    subiteration = 0
    for i in range(len(names)):
        subiteration += 1
        print("In Iteration", iteration, "doing subiteration", subiteration)
        print("of", len(names), "subiterations. Total of", len(subheader_data), "iterations.")

        # attempt = 0
        # tries   = 3
        # while attempt < tries:
        #     try:
        #         html = lprCollector(url = urls[i], selector="div.col-md-4.col-12.result", ctx=ctx).get_base()
        #     except:
        #         print("Retrying:", urls[i])
        #         attempt += 1
        #         html = "Failed"
        #
        #         #time.sleep(300)
        #     else:
        #         continue

        cursor.execute(
            '''
            INSERT INTO variable (subheader_id, header_id, link, var, var_name) VALUES (?, ?, ?, ?, ?)
            ''', (id, header_id,urls[i], names[i], names[i])
        )
        print("Waiting for next variable...")

    connection.commit()
