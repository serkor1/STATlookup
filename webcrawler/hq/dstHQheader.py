# Import Modules;
from webcrawler.modules import *



# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'dstHQraw.sqlite'
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




print("Collecting HQ Headers:")
print("----------------------")
headers = get_html(
    url = 'https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable',
    selector = 'a.accordion__header'
)
subheader = get_html(
    url = 'https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable',
    selector = 'div.accordion__body'
)

with alive_bar(len(subheader)) as bar:
    for i in range(len(subheader)):

        # Get names
        name = headers[i].text


        # Count occurrences
        count = len(re.findall(
            string=str(subheader[i]),
            pattern="<a href=\"(.+)\""
        ))

        cursor.execute(
            '''
            INSERT INTO header (count, name)
            VALUES (?, ?)
            ''', (count, name)
        )

        bar()

connection.commit()
