# This program collects the headers
# from LPR

# Import Collector;
import time

from webcrawler.modules import *
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


print("Collecting Headers from LPR:")
print("----------------------------")
with alive_bar(len(names)) as bar:
    for i in range(len(names)):
        cursor.execute(
            '''
            INSERT INTO header (url, name)
            VALUES (?, ?)
            ''', (urls[i], names[i])
        )

        connection.commit()

        bar()