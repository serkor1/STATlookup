# Import Modules;
from webcrawler.modules import *


# Create Database Connection
connection = database("timesDB")

# Create Cursor and
# initialise Header Data
cursor = connection.cursor()




# Read subheader data;
variable_data = cursor.execute(
    '''
    SELECT * FROM variable
    '''
).fetchall()


with alive_bar(len(variable_data)) as bar:
    for row in variable_data:
        # Extract ID
        id = row[0]
        html = row[6]


        # Extract Soup:
        desc = desc_collect(html, 'div')
        desc = BeautifulSoup(str(desc.get_base()), 'html.parser')

        desc = desc.find_all('p')


        # General Description
        gen_desc = desc[1]
        det_desc = desc[2]

        cursor.execute(
            '''
            UPDATE variable SET desc_gen_da = ?, desc_det_da = ? WHERE ID = ?
            ''', (str(gen_desc), str(det_desc), id)
        )

        connection.commit()

        bar()



