# This program collects the headers
# from LPR

# Import Collector;
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
    DROP TABLE IF EXISTS header;

    CREATE TABLE header (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        url TEXT UNIQUE,
        name  TEXT UNIQUE
        
    )
''')


# Collect all Registres
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE




registers = lprCollector(
    url = "https://www.esundhed.dk/Dokumentation",
    selector= "#list-tab-registers", ctx=ctx
)

names = registers.get_name()
urls = registers.get_url()

iteration = 0
for i in range(len(names)):
    iteration += 1
    print("Iteration", iteration, "of", len(names), "iterations!")

    cursor.execute(
        '''
        INSERT INTO header (url, name)
        VALUES (?, ?)
        ''', (urls[i], names[i])
    )

connection.commit()