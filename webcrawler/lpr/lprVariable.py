# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("lprDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()

connection.create_variable()



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


