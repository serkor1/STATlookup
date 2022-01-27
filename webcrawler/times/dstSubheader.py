# Import Collector;
from webcrawler.modules import *

# Connect to SQL;
# 1) Establish Connection to the database
connection = sqlite3.connect(
    'dstTIMESraw.sqlite'
)

cursor = connection.cursor()

# 2) Create New table
cursor.executescript('''
    DROP TABLE IF EXISTS subheader;
    
    CREATE TABLE subheader (
        id     INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
        header_id INTEGER,
        link TEXT,
        name  TEXT,
        html  TEXT
    );
''')


# Get Header ID to use as
# as foreing keys
header_data = cursor.execute(
    '''
    SELECT * FROM header
    '''
).fetchall()

header_id = []
for row in header_data:

    # Get ID from
    # header
    id = row[0]

    # Gather number
    # of repeats
    number = row[1]

    header_id.append([id] * number)

header_id = list(flatten(header_id))

# Subheaders;

subheader = dstCollector(
    url     = "https://www.dst.dk/da/Statistik/dokumentation/Times",
    selector= 'div.cludoContent',
    do_ul   = False
)

subheader_names = subheader.get_name()

subheader_url   = subheader.get_url()

subheader_content = subheader.get_content(
    selector = 'div.cludoContent',
    url_list = subheader_url
)


print("Collecting TIMES Subheaders:")
print("----------------------------")
with alive_bar(len(subheader_names)) as bar:
    for i in range(len(subheader_names)):

        cursor.execute(
            '''
            INSERT INTO subheader (link, header_id, name, html)
            VALUES (?,?, ?, ?)
            ''', (subheader_url[i], header_id[i],subheader_names[i], str(subheader_content[i]))
        )

        connection.commit()

        bar()





