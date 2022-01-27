# This program collects the headers
# from LPR

# Import Collector;
from webcrawler.modules import *

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

print("Collecting Variables from LPR:")
print("------------------------------")
with alive_bar(len(subheader_data)) as bar:
    for row in subheader_data:

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

        for i in range(len(names)):

            cursor.execute(
                '''
                INSERT INTO variable (subheader_id, header_id, link, var, var_name) VALUES (?, ?, ?, ?, ?)
                ''', (id, header_id,urls[i], names[i], names[i])
            )

        connection.commit()

        bar()


