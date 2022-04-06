# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("hqDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()


# Load data; and extract HTML
var_data = cursor.execute(
    '''
    SELECT * FROM variable
    '''
).fetchall()


print("Collecting HQ Descriptions:")
print("---------------------------")
with alive_bar(len(var_data)) as bar:
    for row in var_data:

        # Extract ID to identify replacement
        # values
        id = row[0]
        content = row[6]

        # All the values inside
        # the html corpus are inside a div
        # where the divisor is H3
        desc = desc_collect(content, 'div')


        # Get the descriptions;
        # Index 0 is title, index 1 is the actual
        # content
        content = desc.get_description(tag='h3')
        titles  = content[0]
        content = content[1]

        cursor.execute(
            '''
            UPDATE variable SET desc_gen_da = ?, desc_det_da = ? WHERE ID = ?
            ''', (content[5], content[6], id)
        )

        connection.commit()

        bar()




