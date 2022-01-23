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



# Read Headerdata:
variable_data = cursor.execute(
    '''
    SELECT * FROM variable
    '''
).fetchall()


# Ignore Certification Errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE


for row in variable_data:

    # Get HTML
    html = lprCollector(url = row[3], selector="div.col-md-4.col-12.result", ctx=ctx).get_base()

    id    = row[0]

    cursor.execute(
        '''
        UPDATE variable SET html = ? WHERE id = ?
        ''', (str(html), id)
    )

connection.commit()

