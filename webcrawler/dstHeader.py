# This program collects the headers
# from DST TIMES

# Import Collector;
from dstCollector_class import dstCollector
from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re


# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'dstTIMESraw.sqlite'
)

cursor = connection.cursor()

# 2) Create New table
cursor.executescript('''
    DROP TABLE IF EXISTS header;

    CREATE TABLE header (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        count INTEGER,
        name  TEXT UNIQUE
    )
''')



def get_html(url, selector):
    content = BeautifulSoup(
        requests.get(url).content,
        'html.parser'
    ).select(selector)

    return content

print("Collecting HEADERS:")
print("===================")
headers = get_html(
    url = 'https://www.dst.dk/da/Statistik/dokumentation/Times',
    selector = 'a.accordion__header'
)
subheader = get_html(
    url = 'https://www.dst.dk/da/Statistik/dokumentation/Times',
    selector = 'div.accordion__body'
)

iteration = 0
for i in range(len(subheader)):
    iteration += 1
    print("Iteration", iteration, "of", len(subheader), "iterations!")

    # Get names
    name = headers[i].text


    # Count occurrences
    count = len(re.findall(
        string=str(subheader[i]),
        pattern="<li><a href=\"(.+)\""
    ))

    cursor.execute(
        '''
        INSERT INTO header (count, name)
        VALUES (?, ?)
        ''', (count, name)
    )

connection.commit()



