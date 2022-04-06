# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("lprDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()


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

print("Collecting LPR html:")
print("--------------------")
with alive_bar(len(variable_data)) as bar:
    for row in variable_data:

        # Get HTML
        html = lprCollector(url = row[3], selector="div.col-md-4.col-12.result", ctx=ctx).get_base()

        id    = row[0]

        cursor.execute(
            '''
            UPDATE variable SET html = ? WHERE id = ?
            ''', (str(html), id)
        )

        bar()

connection.commit()

