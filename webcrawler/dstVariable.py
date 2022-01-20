# Import Collector;
from dstCollector_class import dstCollector
from matplotlib.cbook import flatten
from bs4 import BeautifulSoup
import requests
import sqlite3
from bs4 import BeautifulSoup
import re



def get_html(url, selector):
    content = BeautifulSoup(
        requests.get(url).content,
        'html.parser'
    ).select(selector)

    return content


# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'dstTIMESraw.sqlite'
)

cursor = connection.cursor()

# 2) Create New table
cursor.executescript('''
    DROP TABLE IF EXISTS variable;

    CREATE TABLE variable (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        header_id       INTEGER,
        subheader_id   INTEGER,
        link TEXT UNIQUE,
        var TEXT,
        var_name TEXT,
        html TEXT
    )
''')


# Read subheader data;
subheader_data = cursor.execute(
    '''
    SELECT * FROM subheader
    '''
).fetchall()

iteration = 0
print("Extracting Variables:")
print("=====================")
for row in subheader_data:
    iteration += 1
    print("Iteration", iteration, "of", len(subheader_data))

    id  = row[0]
    header_id = row[1]
    url = row[2]

    # Generate Objects
    variable = dstCollector(
        url         = url,
        selector    = 'div.cludoContent',
        do_ul       = True,
        is_variable = True
    )

    # Get Names
    variable_names = variable.get_name()
    variable_url = variable.get_url()

    # Get additional variables
    # these are urls to the variables
    additional_url = variable.get_additional()


    if len(additional_url) != 0:
        for url in additional_url:
            additional_variable = dstCollector(
                url         = url,
                selector    = 'div.cludoContent',
                do_ul       = False,
                is_variable = False
            )

            additional_names = additional_variable.get_name()
            additional_url = additional_variable.get_url()

            variable_names = variable_names + additional_names
            variable_url   = variable_url + additional_url


    # Flatten the lists
    variable_names = list(
        flatten(variable_names)
    )

    variable_url = list(
        flatten(variable_url)
    )



    for index in range(len(variable_url)):


        # Split Variable Names
        # into var and var_name
        split = re.split(
            string= str(variable_names[index]),
            pattern=",",
            maxsplit=1
        )

        # This checks whether the
        # name in index 1, has letters.
        # If not, it must be empty.
        check_name = bool(
            re.match(
                string = split[1].lower().strip(),
                pattern= "[a-z]+"
            )
        )

        # If there is only one split,
        # it must be that the title is missing.
        if not check_name:
            split = list(flatten([split[0], split[0]]))


        var = split[0].lower().strip()
        var_name = split[1].title().strip()



        html_content = get_html(
            url = variable_url[index],
            selector='div.cludoContent'
        )



        cursor.execute(
            '''
            INSERT OR IGNORE INTO variable (header_id, subheader_id, link, var, var_name, html)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', (header_id, id, variable_url[index], var, var_name, str(html_content[0]))
        )

    connection.commit()

