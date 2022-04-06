# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("lprDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_subheader()


# Read Headerdata:
header_data = cursor.execute(
    '''
    SELECT * FROM header
    '''
).fetchall()



# Ignore Certification Errors
ctx = ssl.create_default_context()
ctx.check_hostname = False
ctx.verify_mode = ssl.CERT_NONE

# time.sleep(60)
print("Collecting Subheaders from LPR:")
print("-------------------------------")
with alive_bar(len(header_data)) as bar:
    for row in header_data:

        # ID goes inside subheader as foreing key
        id = row[0]

        # Extract Register URL
        url = row[3]



        # Extract Main Content
        subheaders = lprCollector(
            url = url,
            selector="#list-tab-tables",
            ctx=ctx
        )

        names = subheaders.get_name()
        urls  = subheaders.get_url()

        for i in range(len(names)):

            cursor.execute(
                '''
                INSERT INTO subheader (header_id, link, name) VALUES (?, ?, ?)
                ''', (id, urls[i], names[i])
            )

        connection.commit()

        bar()


