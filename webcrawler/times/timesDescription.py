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
from googletrans import Translator

translator = Translator()



# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'dstTIMESraw.sqlite'
)

cursor = connection.cursor()


# 2) Create New Colums
cursor.executescript(
    '''
    ALTER TABLE variable
    DROP COLUMN desc_da;
    
    ALTER TABLE variable
    DROP COLUMN desc_en;
    
    ALTER TABLE variable ADD desc_da TEXT;
    ALTER TABLE variable ADD desc_en TEXT;
    '''
)


subheader_data = cursor.execute(
    '''
    SELECT * FROM variable
    '''
).fetchall()


iterator = 0
desc = []
for row in subheader_data:
    iterator += 1
    print("Iteration", iterator, "of", len(subheader_data), "iterations!")

    # Extract HTML
    get_html = row[6]
    get_id   = row[0]

    # Get Soup
    soup = BeautifulSoup(
        get_html,
        'html.parser'
    )

    desc = []
    for line in soup.find_all('p'):


        text = " ".join(line.text.split())

        desc.append(text)



    description_da = desc[1]
    description_en = translator.translate(description_da, dest = 'en')

    cursor.execute(
        '''
        UPDATE variable SET desc_da = ?, desc_en = ? WHERE ID = ?
        ''', (description_da, description_en.text, get_id)
    )

    connection.commit()




