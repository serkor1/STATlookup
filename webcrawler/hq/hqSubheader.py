# Import Modules;
from webcrawler.modules import *

# Create Database Connection
connection = database("hqDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_subheader()


# Get Header ID to use as
# as foreing keys
header_data = cursor.execute(
    '''
    SELECT * FROM header
    '''
).fetchall()

header_id = []
print("Collecting HQ subheaders:")
print("-------------------------")

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
subheader = timesCollector(
    url="https://www.dst.dk/da/TilSalg/Forskningsservice/Dokumentation/hoejkvalitetsvariable",
    selector='div.cludoContent',
    do_ul=False
)

subheader_names = subheader.get_name()
subheader_url = subheader.get_url()

subheader_content = subheader.get_content(
    selector='div.cludoContent',
    url_list=subheader_url
)

with alive_bar(len(subheader_names)) as bar:
    for i in range(len(subheader_names)):
        cursor.execute(
            '''
            INSERT INTO subheader (link, header_id, name, html)
            VALUES (?,?, ?, ?)
            ''', (subheader_url[i], header_id[i], subheader_names[i], str(subheader_content[i]))
        )

        bar()

# Commit Connection
connection.commit()







